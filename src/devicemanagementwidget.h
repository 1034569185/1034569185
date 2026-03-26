#pragma once

#include <QWidget>
#include "database/dbmanager.h"

QT_BEGIN_NAMESPACE
namespace Ui { class DeviceManagementWidget; }
QT_END_NAMESPACE

class DeviceManagementWidget : public QWidget
{
    Q_OBJECT
public:
    explicit DeviceManagementWidget(DbManager *db, QWidget *parent = nullptr);
    ~DeviceManagementWidget();

signals:
    void devicesChanged();

private slots:
    void onDeviceSelected(int row, int col);
    void onAddDeviceClicked();
    void onDeleteDeviceClicked();
    void onSaveClicked();
    void onWriteConfigClicked();
    void onReadConfigClicked();

private:
    void loadDevices();
    void showDeviceDetail(const DeviceInfo &device);
    DeviceInfo currentDeviceFromUI();

    Ui::DeviceManagementWidget *ui;
    DbManager *m_db;
    int m_selectedDeviceId;
};
