#include "devicemanagementwidget.h"
#include "ui_devicemanagementwidget.h"

#include <algorithm>
#include <QComboBox>
#include <QHeaderView>
#include <QListWidgetItem>
#include <QMessageBox>
#include <QSet>
#include <QSignalBlocker>
#include <QTreeWidgetItem>

DeviceManagementWidget::DeviceManagementWidget(DbManager *db, QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::DeviceManagementWidget)
    , m_db(db)
    , m_selectedDeviceId(-1)
{
    ui->setupUi(this);

    connect(ui->treeAreas, &QTreeWidget::itemClicked,
            this, &DeviceManagementWidget::onAreaTreeItemClicked);
    connect(ui->listDevices, &QListWidget::currentRowChanged,
            this, &DeviceManagementWidget::onDeviceListRowChanged);
    connect(ui->btnAddDevice, &QPushButton::clicked,
            this, &DeviceManagementWidget::onAddDeviceClicked);
    connect(ui->btnDeleteDevice, &QPushButton::clicked,
            this, &DeviceManagementWidget::onDeleteDeviceClicked);
    connect(ui->btnSave, &QPushButton::clicked,
            this, &DeviceManagementWidget::onSaveClicked);
    connect(ui->btnWriteConfig, &QPushButton::clicked,
            this, &DeviceManagementWidget::onWriteConfigClicked);
    connect(ui->btnReadConfig, &QPushButton::clicked,
            this, &DeviceManagementWidget::onReadConfigClicked);

    setupVariableTable();
    loadDevices();
}

DeviceManagementWidget::~DeviceManagementWidget()
{
    delete ui;
}

void DeviceManagementWidget::setupVariableTable()
{
    ui->tableVariables->setColumnCount(7);
    ui->tableVariables->setRowCount(2);
    ui->tableVariables->setHorizontalHeaderLabels(
        {tr("变量名"), tr("是否启用"), tr("是否报警"), tr("报警下限"), tr("报警上限"), tr("单位"), tr("选择报警策略")});
    ui->tableVariables->verticalHeader()->setVisible(false);
    ui->tableVariables->horizontalHeader()->setStretchLastSection(true);
    ui->tableVariables->setSelectionBehavior(QAbstractItemView::SelectRows);
    ui->tableVariables->setEditTriggers(QAbstractItemView::AllEditTriggers);

    const QStringList names{tr("温度"), tr("湿度")};
    const QStringList units{QStringLiteral("℃"), QStringLiteral("%RH")};
    for (int row = 0; row < 2; ++row) {
        auto *nameItem = new QTableWidgetItem(names.at(row));
        nameItem->setFlags(nameItem->flags() & ~Qt::ItemIsEditable);
        ui->tableVariables->setItem(row, 0, nameItem);

        auto *enabledItem = new QTableWidgetItem;
        enabledItem->setCheckState(Qt::Checked);
        ui->tableVariables->setItem(row, 1, enabledItem);

        auto *alarmItem = new QTableWidgetItem;
        alarmItem->setCheckState(Qt::Checked);
        ui->tableVariables->setItem(row, 2, alarmItem);

        auto *lowItem = new QTableWidgetItem(row == 0 ? QStringLiteral("0.00") : QStringLiteral("35.00"));
        ui->tableVariables->setItem(row, 3, lowItem);

        auto *highItem = new QTableWidgetItem(row == 0 ? QStringLiteral("30.00") : QStringLiteral("75.00"));
        ui->tableVariables->setItem(row, 4, highItem);

        auto *unitItem = new QTableWidgetItem(units.at(row));
        unitItem->setFlags(unitItem->flags() & ~Qt::ItemIsEditable);
        ui->tableVariables->setItem(row, 5, unitItem);

        auto *policy = new QComboBox(ui->tableVariables);
        policy->addItems({tr(""), tr("声光报警"), tr("短信报警"), tr("声光+短信")});
        ui->tableVariables->setCellWidget(row, 6, policy);
    }
}

DeviceInfo DeviceManagementWidget::findDeviceById(int deviceId) const
{
    for (const DeviceInfo &dev : m_cachedDevices) {
        if (dev.id == deviceId) {
            return dev;
        }
    }
    return DeviceInfo{};
}

void DeviceManagementWidget::loadDevices()
{
    m_cachedDevices = m_db->getAllDevices();

    QSignalBlocker blocker(ui->treeAreas);
    ui->treeAreas->clear();

    auto *allItem = new QTreeWidgetItem(QStringList() << tr("全部"));
    allItem->setData(0, Qt::UserRole, QStringLiteral("__ALL__"));
    ui->treeAreas->addTopLevelItem(allItem);

    QSet<QString> uniqueAreas;
    for (const DeviceInfo &dev : m_cachedDevices) {
        const QString area = dev.area.trimmed().isEmpty() ? tr("未分区") : dev.area.trimmed();
        uniqueAreas.insert(area);
    }

    QList<QString> areaList = uniqueAreas.values();
    std::sort(areaList.begin(), areaList.end(), [](const QString &a, const QString &b) {
        return QString::localeAwareCompare(a, b) < 0;
    });

    for (const QString &area : areaList) {
        auto *areaItem = new QTreeWidgetItem(QStringList() << area);
        areaItem->setData(0, Qt::UserRole, area);
        ui->treeAreas->addTopLevelItem(areaItem);
    }

    ui->treeAreas->expandAll();
    ui->treeAreas->setCurrentItem(allItem);
    blocker.unblock();

    m_selectedArea = QStringLiteral("__ALL__");
    loadAreaDeviceList();
}

void DeviceManagementWidget::loadAreaDeviceList()
{
    QSignalBlocker blocker(ui->listDevices);
    ui->listDevices->clear();

    int count = 0;
    for (const DeviceInfo &dev : m_cachedDevices) {
        const QString area = dev.area.trimmed().isEmpty() ? tr("未分区") : dev.area.trimmed();
        if (m_selectedArea != QStringLiteral("__ALL__") && area != m_selectedArea) {
            continue;
        }

        auto *item = new QListWidgetItem(dev.name);
        item->setData(Qt::UserRole, dev.id);
        ui->listDevices->addItem(item);
        ++count;
    }

    const QString areaText = (m_selectedArea == QStringLiteral("__ALL__")) ? tr("全部") : m_selectedArea;
    ui->lblAreaDeviceTitle->setText(tr("区域[%1]  仪表数%2").arg(areaText).arg(count));

    if (count > 0) {
        ui->listDevices->setCurrentRow(0);
    } else {
        m_selectedDeviceId = -1;
        onAddDeviceClicked();
    }
}

void DeviceManagementWidget::onAreaTreeItemClicked(QTreeWidgetItem *item, int /*column*/)
{
    if (!item) {
        return;
    }
    m_selectedArea = item->data(0, Qt::UserRole).toString();
    if (m_selectedArea.isEmpty()) {
        m_selectedArea = item->text(0);
    }
    loadAreaDeviceList();
}

void DeviceManagementWidget::onDeviceListRowChanged(int row)
{
    if (row < 0) {
        return;
    }

    QListWidgetItem *item = ui->listDevices->item(row);
    if (!item) {
        return;
    }

    m_selectedDeviceId = item->data(Qt::UserRole).toInt();
    const DeviceInfo dev = findDeviceById(m_selectedDeviceId);
    if (dev.id < 0) {
        return;
    }
    showDeviceDetail(dev);
}

void DeviceManagementWidget::showDeviceDetail(const DeviceInfo &device)
{
    ui->txtDeviceName->setText(device.name);
    ui->spinAddress->setValue(device.address > 0 ? device.address : 1);
    ui->chkEnabled->setChecked(device.enabled);
    ui->txtArea->setText(device.area);

    if (ui->tableVariables->rowCount() >= 2) {
        if (QTableWidgetItem *tempLow = ui->tableVariables->item(0, 3)) {
            tempLow->setText(QString::number(device.tempLow, 'f', 2));
        }
        if (QTableWidgetItem *tempHigh = ui->tableVariables->item(0, 4)) {
            tempHigh->setText(QString::number(device.tempHigh, 'f', 2));
        }
        if (QTableWidgetItem *humidLow = ui->tableVariables->item(1, 3)) {
            humidLow->setText(QString::number(device.humidLow, 'f', 2));
        }
        if (QTableWidgetItem *humidHigh = ui->tableVariables->item(1, 4)) {
            humidHigh->setText(QString::number(device.humidHigh, 'f', 2));
        }
    }
}

DeviceInfo DeviceManagementWidget::currentDeviceFromUI()
{
    DeviceInfo dev;
    dev.id = m_selectedDeviceId;
    dev.name = ui->txtDeviceName->text().trimmed();
    dev.address = ui->spinAddress->value();
    dev.enabled = ui->chkEnabled->isChecked();
    dev.area = ui->txtArea->text().trimmed();

    bool ok = false;
    dev.tempLow = ui->tableVariables->item(0, 3) ? ui->tableVariables->item(0, 3)->text().toDouble(&ok) : 0.0;
    if (!ok) dev.tempLow = 0.0;
    dev.tempHigh = ui->tableVariables->item(0, 4) ? ui->tableVariables->item(0, 4)->text().toDouble(&ok) : 30.0;
    if (!ok) dev.tempHigh = 30.0;
    dev.humidLow = ui->tableVariables->item(1, 3) ? ui->tableVariables->item(1, 3)->text().toDouble(&ok) : 20.0;
    if (!ok) dev.humidLow = 20.0;
    dev.humidHigh = ui->tableVariables->item(1, 4) ? ui->tableVariables->item(1, 4)->text().toDouble(&ok) : 80.0;
    if (!ok) dev.humidHigh = 80.0;

    return dev;
}

void DeviceManagementWidget::onAddDeviceClicked()
{
    m_selectedDeviceId = -1;
    ui->txtDeviceName->setText(tr("新记录仪"));
    ui->spinAddress->setValue(1);
    ui->chkEnabled->setChecked(true);
    if (m_selectedArea != QStringLiteral("__ALL__")) {
        ui->txtArea->setText(m_selectedArea);
    } else {
        ui->txtArea->clear();
    }

    if (ui->tableVariables->item(0, 3)) ui->tableVariables->item(0, 3)->setText(QStringLiteral("0.00"));
    if (ui->tableVariables->item(0, 4)) ui->tableVariables->item(0, 4)->setText(QStringLiteral("30.00"));
    if (ui->tableVariables->item(1, 3)) ui->tableVariables->item(1, 3)->setText(QStringLiteral("20.00"));
    if (ui->tableVariables->item(1, 4)) ui->tableVariables->item(1, 4)->setText(QStringLiteral("80.00"));
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

    bool ok = false;
    if (m_selectedDeviceId < 0) {
        ok = m_db->addDevice(dev);
    } else {
        ok = m_db->updateDevice(dev);
    }

    if (ok) {
        QMessageBox::information(this, tr("成功"), tr("设备信息已保存"));
        m_selectedArea = dev.area.isEmpty() ? QStringLiteral("__ALL__") : dev.area;
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
