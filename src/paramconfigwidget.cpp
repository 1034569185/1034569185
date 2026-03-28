#include "paramconfigwidget.h"
#include "ui_paramconfigwidget.h"
#include <QFileDialog>
#include <QMessageBox>

ParamConfigWidget::ParamConfigWidget(DbManager *db, QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::ParamConfigWidget)
    , m_db(db)
{
    ui->setupUi(this);
    connect(ui->btnSave, &QPushButton::clicked, this, &ParamConfigWidget::onSaveClicked);
    connect(ui->btnBrowseBackupDir, &QPushButton::clicked, this, &ParamConfigWidget::onBrowseBackupDirClicked);
    loadConfig();
}

ParamConfigWidget::~ParamConfigWidget()
{
    delete ui;
}

void ParamConfigWidget::loadConfig()
{
    ui->txtWarehouseName->setText(m_db->getConfig("warehouse_name"));
    ui->spinRecordInterval->setValue(m_db->getConfig("record_interval", "5").toInt());
    ui->spinAlarmVolume->setValue(m_db->getConfig("alarm_volume", "10").toInt());
    ui->txtAllAreaName->setText(m_db->getConfig("all_area_name", "全部"));
    ui->txtSoftwareTitle->setText(m_db->getConfig("software_title", "鸿软温湿度监测系统"));
    ui->chkSendSmsOnRecover->setChecked(m_db->getConfig("send_sms_on_recover", "0") == "1");
    ui->chkSendSmsOnAlarm->setChecked(m_db->getConfig("send_sms_on_alarm", "1") == "1");
    ui->txtTargetIP->setText(m_db->getConfig("target_ip"));
    ui->spinTargetPort->setValue(m_db->getConfig("target_port", "8080").toInt());
    ui->txtBackupDir->setText(m_db->getConfig("backup_dir"));
    ui->spinPwdExpireDays->setValue(m_db->getConfig("pwd_expire_days", "90").toInt());
    ui->chkEnableEmail->setChecked(m_db->getConfig("enable_email", "0") == "1");
    ui->txtEmailAccount->setText(m_db->getConfig("email_account"));
    ui->txtEmailAuthCode->setText(m_db->getConfig("email_auth_code"));

    // Read-only fields
    ui->txtHistoryDB->setText(tr("按月归档 (SQLite)"));
    ui->txtCurrentDB->setText(tr("每日备份"));
    ui->timeBackup->setTime(QTime(0, 11));
}

void ParamConfigWidget::onSaveClicked()
{
    m_db->setConfig("warehouse_name", ui->txtWarehouseName->text());
    m_db->setConfig("record_interval", QString::number(ui->spinRecordInterval->value()));
    m_db->setConfig("alarm_volume", QString::number(ui->spinAlarmVolume->value()));
    m_db->setConfig("all_area_name", ui->txtAllAreaName->text());
    m_db->setConfig("software_title", ui->txtSoftwareTitle->text());
    m_db->setConfig("send_sms_on_recover", ui->chkSendSmsOnRecover->isChecked() ? "1" : "0");
    m_db->setConfig("send_sms_on_alarm", ui->chkSendSmsOnAlarm->isChecked() ? "1" : "0");
    m_db->setConfig("target_ip", ui->txtTargetIP->text());
    m_db->setConfig("target_port", QString::number(ui->spinTargetPort->value()));
    m_db->setConfig("backup_dir", ui->txtBackupDir->text());
    m_db->setConfig("pwd_expire_days", QString::number(ui->spinPwdExpireDays->value()));
    m_db->setConfig("enable_email", ui->chkEnableEmail->isChecked() ? "1" : "0");
    m_db->setConfig("email_account", ui->txtEmailAccount->text());
    m_db->setConfig("email_auth_code", ui->txtEmailAuthCode->text());

    QMessageBox::information(this, tr("成功"), tr("参数配置已保存"));
    emit configSaved();
}

void ParamConfigWidget::onBrowseBackupDirClicked()
{
    QString dir = QFileDialog::getExistingDirectory(this, tr("选择备份目录"),
        QDir::homePath());
    if (!dir.isEmpty()) {
        QString current = ui->txtBackupDir->text();
        if (current.isEmpty()) {
            ui->txtBackupDir->setText(dir);
        } else {
            ui->txtBackupDir->setText(current + "|" + dir);
        }
    }
}
