#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "logindialog.h"
#include "sensorwidget.h"
#include "dataquerywidget.h"
#include "alarmwidget.h"
#include "floorplanwidget.h"
#include "devicemanagementwidget.h"
#include "usermanagementwidget.h"
#include "paramconfigwidget.h"
#include "sitemanagementwidget.h"
#include "logquerywidget.h"

#include <QDialog>
#include <QVBoxLayout>
#include <QGridLayout>
#include <QMessageBox>
#include <QMenuBar>
#include <QMenu>
#include <QAction>
#include <QApplication>
#include <QDateTime>
#include <QDebug>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , m_db(new DbManager(this))
    , m_serial(new SerialManager(this))
    , m_clockTimer(new QTimer(this))
    , m_autoLockTimer(new QTimer(this))
    , m_dataRefreshTimer(new QTimer(this))
    , m_currentPermissions(0)
    , m_autoLockSeconds(600)
    , m_currentAreaIndex(0)
{
    ui->setupUi(this);

    // Open database
    if (!m_db->open()) {
        QMessageBox::critical(this, tr("数据库错误"),
            tr("无法打开数据库：%1").arg(m_db->lastError()));
    }

    // Set window title from config
    QString title = m_db->getConfig("software_title", "鸿软温湿度监测系统");
    setWindowTitle(title);
    ui->titleLabel->setText(title);

    setupConnections();
    loadDevices();

    // Clock timer
    m_clockTimer->setInterval(1000);
    connect(m_clockTimer, &QTimer::timeout, this, &MainWindow::onUpdateDateTime);
    m_clockTimer->start();
    onUpdateDateTime();

    // Auto lock timer (check every 30s)
    m_autoLockTimer->setInterval(30000);
    connect(m_autoLockTimer, &QTimer::timeout, this, &MainWindow::onAutoLockTimer);
    m_autoLockTimer->start();

    // Serial data polling
    connect(m_serial, &SerialManager::dataReceived, this, &MainWindow::onSensorDataReceived);

    // Show login dialog on startup
    if (!showLoginDialog()) {
        // If cancelled, still show UI but locked
    }
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::setCurrentUser(const QString &username, int permissions)
{
    m_currentUser = username;
    m_currentPermissions = permissions;
    if (username.isEmpty()) {
        ui->lblCurrentUser->setText(tr("当前用户: -"));
    } else {
        ui->lblCurrentUser->setText(tr("当前用户: %1").arg(username));
        m_db->insertLog("ui", username, "登录", "用户登录系统");
    }
}

void MainWindow::setupConnections()
{
    connect(ui->btnDataQuery, &QPushButton::clicked, this, &MainWindow::onDataQueryClicked);
    connect(ui->btnAlarm, &QPushButton::clicked, this, &MainWindow::onAlarmClicked);
    connect(ui->btnFloorPlan, &QPushButton::clicked, this, &MainWindow::onFloorPlanClicked);
    connect(ui->btnSettings, &QPushButton::clicked, this, &MainWindow::onSettingsClicked);
    connect(ui->btnSwitchSite, &QPushButton::clicked, this, &MainWindow::onSwitchSiteClicked);
    connect(ui->btnLogQuery, &QPushButton::clicked, this, &MainWindow::onLogQueryClicked);
    connect(ui->btnHelp, &QPushButton::clicked, this, &MainWindow::onHelpClicked);
    connect(ui->btnLogin, &QPushButton::clicked, this, &MainWindow::onLoginClicked);
    connect(ui->btnLogout, &QPushButton::clicked, this, &MainWindow::onLogoutClicked);
    connect(ui->areaTabBar, &QTabBar::currentChanged, this, &MainWindow::onAreaTabChanged);
}

void MainWindow::loadDevices()
{
    QList<DeviceInfo> devices = m_db->getAllDevices();

    m_areaDeviceMap.clear();
    m_sensorWidgets.clear();
    m_areas.clear();

    // Clear existing sensor widgets
    QLayoutItem *child;
    while ((child = ui->sensorGridLayout->takeAt(0)) != nullptr) {
        if (child->widget()) child->widget()->deleteLater();
        delete child;
    }

    // Group devices by area
    QString allAreaName = m_db->getConfig("all_area_name", "全部");
    m_areaDeviceMap[allAreaName] = QList<int>();

    for (const DeviceInfo &dev : devices) {
        if (!dev.enabled) continue;
        QString area = dev.area.isEmpty() ? tr("默认区域") : dev.area;
        if (!m_areaDeviceMap.contains(area)) {
            m_areaDeviceMap[area] = QList<int>();
        }
        m_areaDeviceMap[area].append(dev.id);
        m_areaDeviceMap[allAreaName].append(dev.id);

        // Create sensor widget
        SensorWidget *w = new SensorWidget(this);
        w->setDeviceInfo(dev);
        m_sensorWidgets[dev.id] = w;
    }

    // Build area list (all areas first, then sorted)
    m_areas << allAreaName;
    QStringList otherAreas = m_areaDeviceMap.keys();
    otherAreas.removeAll(allAreaName);
    otherAreas.sort();
    m_areas << otherAreas;

    setupAreaTabs();
    onAreaTabChanged(0);

    // Start serial polling for enabled devices
    QList<int> addresses;
    for (const DeviceInfo &dev : devices) {
        if (dev.enabled) addresses << dev.address;
    }
    if (!addresses.isEmpty() && m_serial->isOpen()) {
        m_serial->startPolling(addresses);
    }
}

void MainWindow::setupAreaTabs()
{
    // Remove all existing tabs
    while (ui->areaTabBar->count() > 0) {
        ui->areaTabBar->removeTab(0);
    }
    for (const QString &area : m_areas) {
        ui->areaTabBar->addTab(area);
    }
}

void MainWindow::onAreaTabChanged(int index)
{
    if (index < 0 || index >= m_areas.size()) return;
    m_currentAreaIndex = index;

    // Clear grid
    QLayoutItem *child;
    while ((child = ui->sensorGridLayout->takeAt(0)) != nullptr) {
        if (child->widget()) child->widget()->setVisible(false);
        delete child;
    }

    QString areaName = m_areas.at(index);
    QList<int> deviceIds = m_areaDeviceMap.value(areaName);

    int cols = 5;
    int row = 0, col = 0;
    for (int devId : deviceIds) {
        SensorWidget *w = m_sensorWidgets.value(devId);
        if (w) {
            w->setVisible(true);
            ui->sensorGridLayout->addWidget(w, row, col);
            ++col;
            if (col >= cols) { col = 0; ++row; }
        }
    }
}

void MainWindow::onSensorDataReceived(const SensorReading &reading)
{
    // Find device by address
    QList<DeviceInfo> devices = m_db->getAllDevices();
    for (const DeviceInfo &dev : devices) {
        if (dev.address == reading.deviceAddress) {
            if (reading.valid) {
                // Update display
                SensorWidget *w = m_sensorWidgets.value(dev.id);
                if (w) {
                    SensorData sd;
                    sd.deviceId = dev.id;
                    sd.deviceName = dev.name;
                    sd.temperature = reading.temperature;
                    sd.humidity = reading.humidity;
                    sd.tempAlarm = reading.temperature > dev.tempHigh || reading.temperature < dev.tempLow;
                    sd.humidAlarm = reading.humidity > dev.humidHigh || reading.humidity < dev.humidLow;
                    sd.recordTime = QDateTime::currentDateTime();
                    w->updateReading(reading.temperature, reading.humidity,
                                     sd.tempAlarm, sd.humidAlarm);

                    // Save to database (throttle based on record interval)
                    m_db->insertSensorData(sd);

                    // Handle alarm
                    if (sd.tempAlarm || sd.humidAlarm) {
                        AlarmRecord alarm;
                        alarm.deviceId = dev.id;
                        alarm.deviceName = dev.name;
                        alarm.alarmTime = sd.recordTime;
                        if (sd.tempAlarm) {
                            alarm.alarmType = reading.temperature > dev.tempHigh ? "温度超上限" : "温度低于下限";
                            alarm.alarmValue = reading.temperature;
                            alarm.limitValue = reading.temperature > dev.tempHigh ? dev.tempHigh : dev.tempLow;
                        } else {
                            alarm.alarmType = reading.humidity > dev.humidHigh ? "湿度超上限" : "湿度低于下限";
                            alarm.alarmValue = reading.humidity;
                            alarm.limitValue = reading.humidity > dev.humidHigh ? dev.humidHigh : dev.humidLow;
                        }
                        m_db->insertAlarmRecord(alarm);
                        ui->lblAlarmStatus->setText(tr("最新报警: %1 %2").arg(dev.name).arg(alarm.alarmType));
                        ui->lblAlarmStatus->setStyleSheet("QLabel { color: #e74c3c; font-size: 12px; }");
                    }
                }
            }
            break;
        }
    }
}

void MainWindow::onUpdateDateTime()
{
    ui->lblDateTime->setText(QDateTime::currentDateTime().toString("yyyy-MM-dd HH:mm:ss"));
}

void MainWindow::onAutoLockTimer()
{
    // Auto lock is tracked via user inactivity - simplified implementation
    // A full implementation would track last input event time
}

void MainWindow::lockScreen()
{
    setCurrentUser(QString(), 0);
    showLoginDialog();
}

bool MainWindow::showLoginDialog()
{
    LoginDialog dlg(m_db, this);
    if (dlg.exec() == QDialog::Accepted) {
        setCurrentUser(dlg.username(), dlg.permissions());
        return true;
    }
    return false;
}

void MainWindow::showSubWidget(QWidget *widget, const QString &title)
{
    QDialog *dlg = new QDialog(this);
    dlg->setWindowTitle(title);
    dlg->setMinimumSize(900, 650);
    QVBoxLayout *layout = new QVBoxLayout(dlg);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->addWidget(widget);
    dlg->exec();
    delete dlg;
}

void MainWindow::onDataQueryClicked()
{
    DataQueryWidget *w = new DataQueryWidget(m_db, this);
    showSubWidget(w, tr("数据查询"));
}

void MainWindow::onAlarmClicked()
{
    AlarmWidget *w = new AlarmWidget(m_db, this);
    showSubWidget(w, tr("系统报警"));
}

void MainWindow::onFloorPlanClicked()
{
    FloorPlanWidget *w = new FloorPlanWidget(m_db, this);
    showSubWidget(w, tr("设置平面图"));
}

void MainWindow::onSettingsClicked()
{
    // Show settings menu
    QMenu menu(this);
    QAction *actDevice = menu.addAction(tr("设备管理"));
    QAction *actUser = menu.addAction(tr("用户管理"));
    QAction *actParam = menu.addAction(tr("参数配置"));

    QAction *selected = menu.exec(ui->btnSettings->mapToGlobal(ui->btnSettings->rect().bottomLeft()));
    if (selected == actDevice) {
        DeviceManagementWidget *w = new DeviceManagementWidget(m_db, this);
        connect(w, &DeviceManagementWidget::devicesChanged, this, &MainWindow::loadDevices);
        showSubWidget(w, tr("设备管理"));
    } else if (selected == actUser) {
        UserManagementWidget *w = new UserManagementWidget(m_db, this);
        showSubWidget(w, tr("用户管理"));
    } else if (selected == actParam) {
        ParamConfigWidget *w = new ParamConfigWidget(m_db, this);
        connect(w, &ParamConfigWidget::configSaved, [this](){
            QString title = m_db->getConfig("software_title", "鸿软温湿度监测系统");
            setWindowTitle(title);
            ui->titleLabel->setText(title);
        });
        showSubWidget(w, tr("参数配置"));
    }
}

void MainWindow::onSwitchSiteClicked()
{
    SiteManagementWidget *w = new SiteManagementWidget(m_db, this);
    showSubWidget(w, tr("切换站点"));
}

void MainWindow::onLogQueryClicked()
{
    LogQueryWidget *w = new LogQueryWidget(m_db, this);
    showSubWidget(w, tr("日志查询"));
}

void MainWindow::onHelpClicked()
{
    QMessageBox::information(this, tr("帮助"),
        tr("鸿软温湿度监测系统\n"
           "版本: V2022.0516.3.1 (Qt版)\n\n"
           "广州鸿软信息科技有限公司\n"
           "Guangzhou hongruan Information technology Co.,Ltd\n\n"
           "如有问题，请联系技术支持。"));
}

void MainWindow::onLoginClicked()
{
    showLoginDialog();
}

void MainWindow::onLogoutClicked()
{
    if (!m_currentUser.isEmpty()) {
        m_db->insertLog("ui", m_currentUser, "退出登录", "用户退出登录");
    }
    lockScreen();
}
