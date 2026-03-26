#include "usermanagementwidget.h"
#include "ui_usermanagementwidget.h"
#include <QMessageBox>
#include <QCryptographicHash>

UserManagementWidget::UserManagementWidget(DbManager *db, QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::UserManagementWidget)
    , m_db(db)
    , m_selectedUserId(-1)
{
    ui->setupUi(this);
    connect(ui->lstUsers, &QListWidget::currentTextChanged, this, &UserManagementWidget::onUserSelected);
    connect(ui->btnAddUser, &QPushButton::clicked, this, &UserManagementWidget::onAddUserClicked);
    connect(ui->btnDeleteUser, &QPushButton::clicked, this, &UserManagementWidget::onDeleteUserClicked);
    connect(ui->btnSave, &QPushButton::clicked, this, &UserManagementWidget::onSaveClicked);
    connect(ui->btnAddPhone, &QPushButton::clicked, this, &UserManagementWidget::onAddPhoneClicked);
    connect(ui->btnRemovePhone, &QPushButton::clicked, this, &UserManagementWidget::onRemovePhoneClicked);
    loadUsers();
}

UserManagementWidget::~UserManagementWidget()
{
    delete ui;
}

void UserManagementWidget::loadUsers()
{
    ui->lstUsers->clear();
    QList<UserInfo> users = m_db->getAllUsers();
    for (const UserInfo &u : users) {
        QListWidgetItem *item = new QListWidgetItem(u.username);
        item->setData(Qt::UserRole, u.id);
        ui->lstUsers->addItem(item);
    }
}

void UserManagementWidget::onUserSelected(const QString &username)
{
    if (username.isEmpty()) return;
    UserInfo user = m_db->getUserByName(username);
    if (user.id < 0) return;
    m_selectedUserId = user.id;
    showUserDetail(user);
}

void UserManagementWidget::showUserDetail(const UserInfo &user)
{
    ui->txtUsername->setText(user.username);
    ui->txtRealName->setText(user.realName);
    ui->txtPhone->setText(user.phone);
    ui->txtEmail->setText(user.email);
    ui->txtPassword->clear();
    ui->txtConfirmPwd->clear();

    // Permissions
    int perms = user.permissions;
    ui->chkDataQuery->setChecked(perms < 0 || (perms & 0x01));
    ui->chkAlarmQuery->setChecked(perms < 0 || (perms & 0x02));
    ui->chkFloorPlan->setChecked(perms < 0 || (perms & 0x04));
    ui->chkDeviceMgmt->setChecked(perms < 0 || (perms & 0x08));
    ui->chkUserMgmt->setChecked(perms < 0 || (perms & 0x10));
    ui->chkParamConfig->setChecked(perms < 0 || (perms & 0x20));
    ui->chkLogQuery->setChecked(perms < 0 || (perms & 0x40));
    ui->chkExportPDF->setChecked(perms < 0 || (perms & 0x80));
}

void UserManagementWidget::onAddUserClicked()
{
    m_selectedUserId = -1;
    UserInfo emptyUser;
    emptyUser.id = -1;
    emptyUser.permissions = 0x03; // data query + alarm query by default
    showUserDetail(emptyUser);
    ui->txtUsername->setFocus();
}

void UserManagementWidget::onDeleteUserClicked()
{
    if (m_selectedUserId < 0) {
        QMessageBox::warning(this, tr("提示"), tr("请先选择一个用户"));
        return;
    }
    if (QMessageBox::question(this, tr("确认删除"),
            tr("确认删除该用户？"),
            QMessageBox::Yes | QMessageBox::No) == QMessageBox::Yes) {
        m_db->deleteUser(m_selectedUserId);
        loadUsers();
        m_selectedUserId = -1;
    }
}

void UserManagementWidget::onSaveClicked()
{
    QString username = ui->txtUsername->text().trimmed();
    if (username.isEmpty()) {
        QMessageBox::warning(this, tr("提示"), tr("请输入用户名"));
        return;
    }

    QString pwd = ui->txtPassword->text();
    QString confirmPwd = ui->txtConfirmPwd->text();
    if (m_selectedUserId < 0 && pwd.isEmpty()) {
        QMessageBox::warning(this, tr("提示"), tr("请输入密码"));
        return;
    }
    if (!pwd.isEmpty() && pwd != confirmPwd) {
        QMessageBox::warning(this, tr("提示"), tr("两次输入的密码不一致"));
        return;
    }

    // Calculate permissions
    int perms = 0;
    if (ui->chkDataQuery->isChecked()) perms |= 0x01;
    if (ui->chkAlarmQuery->isChecked()) perms |= 0x02;
    if (ui->chkFloorPlan->isChecked()) perms |= 0x04;
    if (ui->chkDeviceMgmt->isChecked()) perms |= 0x08;
    if (ui->chkUserMgmt->isChecked()) perms |= 0x10;
    if (ui->chkParamConfig->isChecked()) perms |= 0x20;
    if (ui->chkLogQuery->isChecked()) perms |= 0x40;
    if (ui->chkExportPDF->isChecked()) perms |= 0x80;

    UserInfo user;
    user.id = m_selectedUserId;
    user.username = username;
    user.realName = ui->txtRealName->text().trimmed();
    user.phone = ui->txtPhone->text().trimmed();
    user.email = ui->txtEmail->text().trimmed();
    user.permissions = perms;
    user.active = true;

    bool ok;
    if (m_selectedUserId < 0) {
        user.passwordHash = QCryptographicHash::hash(pwd.toUtf8(), QCryptographicHash::Sha256).toHex();
        ok = m_db->addUser(user);
    } else {
        ok = m_db->updateUser(user);
        if (ok && !pwd.isEmpty()) {
            m_db->changePassword(username, pwd);
        }
    }

    if (ok) {
        QMessageBox::information(this, tr("成功"), tr("用户信息已保存"));
        loadUsers();
    } else {
        QMessageBox::critical(this, tr("错误"), tr("保存失败：%1").arg(m_db->lastError()));
    }
}

void UserManagementWidget::onAddPhoneClicked()
{
    QString phone = ui->txtAlarmPhone->text().trimmed();
    if (phone.isEmpty()) return;
    ui->lstAlarmPhones->addItem(phone);
    ui->txtAlarmPhone->clear();
}

void UserManagementWidget::onRemovePhoneClicked()
{
    QListWidgetItem *item = ui->lstAlarmPhones->currentItem();
    if (item) delete item;
}
