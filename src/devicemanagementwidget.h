#pragma once

#include <QWidget>
#include "database/dbmanager.h"

QT_BEGIN_NAMESPACE
namespace Ui { class DeviceManagementWidget; }
QT_END_NAMESPACE

class QTreeWidgetItem;

class DeviceManagementWidget : public QWidget
{
    Q_OBJECT
public:
    explicit DeviceManagementWidget(DbManager *db, QWidget *parent = nullptr);
    ~DeviceManagementWidget();

signals:
    void devicesChanged();

private slots:
    void onAreaTreeItemClicked(QTreeWidgetItem *item, int column);
    void onDeviceListRowChanged(int row);
    void onAddDeviceClicked();
    void onDeleteDeviceClicked();
    void onSaveClicked();
    void onWriteConfigClicked();
    void onReadConfigClicked();

private:
    void loadDevices();
    void loadAreaDeviceList();
    void showDeviceDetail(const DeviceInfo &device);
    DeviceInfo currentDeviceFromUI();
    DeviceInfo findDeviceById(int deviceId) const;
    void setupVariableTable();

    Ui::DeviceManagementWidget *ui;
    DbManager *m_db;
    int m_selectedDeviceId;
    QString m_selectedArea;
    QList<DeviceInfo> m_cachedDevices;
};
