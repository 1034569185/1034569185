#include "logindialog.h"
#include "ui_logindialog.h"
#include <QMessageBox>

LoginDialog::LoginDialog(DbManager *db, QWidget *parent)
    : QDialog(parent)
    , ui(new Ui::LoginDialog)
    , m_db(db)
    , m_permissions(0)
{
    ui->setupUi(this);
    setWindowFlags(windowFlags() & ~Qt::WindowContextHelpButtonHint);
    connect(ui->btnLogin, &QPushButton::clicked, this, &LoginDialog::onLoginClicked);
    connect(ui->txtPassword, &QLineEdit::returnPressed, this, &LoginDialog::onLoginClicked);
}

LoginDialog::~LoginDialog()
{
    delete ui;
}

QString LoginDialog::username() const
{
    return m_username;
}

int LoginDialog::permissions() const
{
    return m_permissions;
}

void LoginDialog::onLoginClicked()
{
    QString user = ui->txtUsername->text().trimmed();
    QString pass = ui->txtPassword->text();

    if (user.isEmpty() || pass.isEmpty()) {
        ui->lblError->setText(tr("请输入用户名和密码"));
        return;
    }

    if (!m_db->verifyPassword(user, pass)) {
        ui->lblError->setText(tr("用户名或密码错误"));
        ui->txtPassword->clear();
        ui->txtPassword->setFocus();
        return;
    }

    UserInfo info = m_db->getUserByName(user);
    if (!info.active) {
        ui->lblError->setText(tr("该账号已被禁用"));
        return;
    }

    // Check password expiry
    if (info.passwordExpiry.isValid() && info.passwordExpiry < QDateTime::currentDateTime()) {
        ui->lblError->setText(tr("密码已过期，请联系管理员"));
        return;
    }

    m_username = user;
    m_permissions = info.permissions;
    accept();
}
