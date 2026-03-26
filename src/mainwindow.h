#pragma once

#include <QMainWindow>
#include <QTimer>
#include <QTabBar>
#include <QLabel>
#include <QMap>
#include "database/dbmanager.h"
#include "serialcomm/serialmanager.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class SensorWidget;

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    void setCurrentUser(const QString &username, int permissions);

private slots:
    void onDataQueryClicked();
    void onAlarmClicked();
    void onFloorPlanClicked();
    void onSettingsClicked();
    void onSwitchSiteClicked();
    void onLogQueryClicked();
    void onHelpClicked();
    void onLoginClicked();
    void onLogoutClicked();
    void onAreaTabChanged(int index);
    void onUpdateDateTime();
    void onSensorDataReceived(const SensorReading &reading);
    void onAutoLockTimer();

private:
    void setupConnections();
    void loadDevices();
    void setupAreaTabs();
    void updateSensorDisplay(const SensorReading &reading);
    void checkAutoLock();
    void lockScreen();
    bool showLoginDialog();
    void showSubWidget(QWidget *widget, const QString &title);

    Ui::MainWindow *ui;
    DbManager *m_db;
    SerialManager *m_serial;
    QTimer *m_clockTimer;
    QTimer *m_autoLockTimer;
    QTimer *m_dataRefreshTimer;

    QString m_currentUser;
    int m_currentPermissions;
    int m_autoLockSeconds;

    QMap<int, SensorWidget*> m_sensorWidgets; // deviceId -> widget
    QMap<QString, QList<int>> m_areaDeviceMap; // area -> deviceIds
    QStringList m_areas;
    int m_currentAreaIndex;
};
