#include "devicemanagementwidget.h"
#include "ui_devicemanagementwidget.h"
#include <QMessageBox>

DeviceManagementWidget::DeviceManagementWidget(DbManager *db, QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::DeviceManagementWidget)
    , m_db(db)
    , m_selectedDeviceId(-1)
{
    ui->setupUi(this);
    connect(ui->tableDevices, &QTableWidget::cellClicked, this, &DeviceManagementWidget::onDeviceSelected);
    connect(ui->btnAddDevice, &QPushButton::clicked, this, &DeviceManagementWidget::onAddDeviceClicked);
    connect(ui->btnDeleteDevice, &QPushButton::clicked, this, &DeviceManagementWidget::onDeleteDeviceClicked);
    connect(ui->btnSave, &QPushButton::clicked, this, &DeviceManagementWidget::onSaveClicked);
    connect(ui->btnWriteConfig, &QPushButton::clicked, this, &DeviceManagementWidget::onWriteConfigClicked);
    connect(ui->btnReadConfig, &QPushButton::clicked, this, &DeviceManagementWidget::onReadConfigClicked);
    loadDevices();
}

DeviceManagementWidget::~DeviceManagementWidget()
{
    delete ui;
}

void DeviceManagementWidget::loadDevices()
{
    ui->tableDevices->setRowCount(0);
    QList<DeviceInfo> devices = m_db->getAllDevices();
    for (const DeviceInfo &dev : devices) {
        int row = ui->tableDevices->rowCount();
        ui->tableDevices->insertRow(row);
        QTableWidgetItem *nameItem = new QTableWidgetItem(dev.name);
        nameItem->setData(Qt::UserRole, dev.id);
        ui->tableDevices->setItem(row, 0, nameItem);
        ui->tableDevices->setItem(row, 1, new QTableWidgetItem(QString::number(dev.address)));
        ui->tableDevices->setItem(row, 2, new QTableWidgetItem(dev.enabled ? tr("启用") : tr("禁用")));
    }
}

void DeviceManagementWidget::onDeviceSelected(int row, int /*col*/)
{
    QTableWidgetItem *item = ui->tableDevices->item(row, 0);
    if (!item) return;
    m_selectedDeviceId = item->data(Qt::UserRole).toInt();
    DeviceInfo dev = m_db->getDevice(m_selectedDeviceId);
    showDeviceDetail(dev);
}

void DeviceManagementWidget::showDeviceDetail(const DeviceInfo &device)
{
    ui->txtDeviceName->setText(device.name);
    ui->spinAddress->setValue(device.address);
    ui->chkEnabled->setChecked(device.enabled);
    ui->txtArea->setText(device.area);
    ui->spinTempHigh->setValue(device.tempHigh);
    ui->spinTempLow->setValue(device.tempLow);
    ui->spinHumidHigh->setValue(device.humidHigh);
    ui->spinHumidLow->setValue(device.humidLow);
}

DeviceInfo DeviceManagementWidget::currentDeviceFromUI()
{
    DeviceInfo dev;
    dev.id = m_selectedDeviceId;
    dev.name = ui->txtDeviceName->text().trimmed();
    dev.address = ui->spinAddress->value();
    dev.enabled = ui->chkEnabled->isChecked();
    dev.area = ui->txtArea->text().trimmed();
    dev.tempHigh = ui->spinTempHigh->value();
    dev.tempLow = ui->spinTempLow->value();
    dev.humidHigh = ui->spinHumidHigh->value();
    dev.humidLow = ui->spinHumidLow->value();
    return dev;
}

void DeviceManagementWidget::onAddDeviceClicked()
{
    DeviceInfo dev;
    dev.id = -1;
    dev.name = tr("新记录仪");
    dev.address = 1;
    dev.enabled = true;
    dev.tempHigh = 30.0;
    dev.tempLow = 0.0;
    dev.humidHigh = 80.0;
    dev.humidLow = 20.0;
    showDeviceDetail(dev);
    m_selectedDeviceId = -1;
}

void DeviceManagementWidget::onDeleteDeviceClicked()
{
    if (m_selectedDeviceId < 0) {
        QMessageBox::warning(this, tr("提示"), tr("请先选择一个设备"));
        return;
    }
    if (QMessageBox::question(this, tr("确认删除"),
            tr("确认删除该设备？此操作不可撤销。"),
            QMessageBox::Yes | QMessageBox::No) == QMessageBox::Yes) {
        m_db->deleteDevice(m_selectedDeviceId);
        loadDevices();
        m_selectedDeviceId = -1;
        emit devicesChanged();
    }
}

void DeviceManagementWidget::onSaveClicked()
{
    DeviceInfo dev = currentDeviceFromUI();
    if (dev.name.isEmpty()) {
        QMessageBox::warning(this, tr("提示"), tr("请输入设备名称"));
        return;
    }
    bool ok;
    if (m_selectedDeviceId < 0) {
        ok = m_db->addDevice(dev);
    } else {
        ok = m_db->updateDevice(dev);
    }
    if (ok) {
        QMessageBox::information(this, tr("成功"), tr("设备信息已保存"));
        loadDevices();
        emit devicesChanged();
    } else {
        QMessageBox::critical(this, tr("错误"), tr("保存失败：%1").arg(m_db->lastError()));
    }
}

void DeviceManagementWidget::onWriteConfigClicked()
{
    QMessageBox::information(this, tr("提示"),
        tr("写配置功能需要串口连接。\n请确保已连接串口设备后再使用此功能。"));
}

void DeviceManagementWidget::onReadConfigClicked()
{
    QMessageBox::information(this, tr("提示"),
        tr("读配置功能需要串口连接。\n请确保已连接串口设备后再使用此功能。"));
}
