#include "dataquerywidget.h"
#include "ui_dataquerywidget.h"

#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>
#include <QtCharts/QChart>
#include <QtCharts/QDateTimeAxis>
#include <QtCharts/QValueAxis>
#include <QPrinter>
#include <QPainter>
#include <QFileDialog>
#include <QMessageBox>
#include <QDateTime>
#include <QVBoxLayout>
#include <QDir>
#include <QRegularExpression>
#include <QSignalBlocker>
#include <QHeaderView>
#include <QMap>
#include <limits>

#include <QtGlobal>
#if QT_VERSION < QT_VERSION_CHECK(6, 0, 0)
QT_CHARTS_USE_NAMESPACE
#endif

DataQueryWidget::DataQueryWidget(DbManager *db, QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::DataQueryWidget)
    , m_db(db)
    , m_tempChartView(nullptr)
    , m_humidChartView(nullptr)
{
    ui->setupUi(this);

    // Set default time range: last 24 hours
    QDateTime now = QDateTime::currentDateTime();
    ui->dtEndTime->setDateTime(now);
    ui->dtStartTime->setDateTime(now.addDays(-1));

    populateDeviceList();

    connect(ui->btnQuery, &QPushButton::clicked, this, &DataQueryWidget::onQueryClicked);
    connect(ui->btnExportPDF, &QPushButton::clicked, this, &DataQueryWidget::onExportPDFClicked);
    connect(ui->treeDevices, &QTreeWidget::itemChanged, this, &DataQueryWidget::onTreeItemChanged);

    // Setup chart placeholders
    m_tempChartView = new QChartView(new QChart());
    m_tempChartView->chart()->setTitle(tr("温度曲线"));
    m_tempChartView->setRenderHint(QPainter::Antialiasing);
    QVBoxLayout *tempLayout = qobject_cast<QVBoxLayout*>(ui->tempChartLayout);
    if (tempLayout) {
        tempLayout->addWidget(m_tempChartView);
    }

    m_humidChartView = new QChartView(new QChart());
    m_humidChartView->chart()->setTitle(tr("湿度曲线"));
    m_humidChartView->setRenderHint(QPainter::Antialiasing);
    QVBoxLayout *humidLayout = qobject_cast<QVBoxLayout*>(ui->humidChartLayout);
    if (humidLayout) {
        humidLayout->addWidget(m_humidChartView);
    }

    QHeaderView *header = ui->tableData->horizontalHeader();
    if (header) {
        header->setStretchLastSection(false);
        header->setSectionResizeMode(0, QHeaderView::Fixed);
        header->setSectionResizeMode(1, QHeaderView::Fixed);
        header->setSectionResizeMode(2, QHeaderView::Fixed);
        header->setSectionResizeMode(3, QHeaderView::Fixed);
        header->setSectionResizeMode(4, QHeaderView::Fixed);
        header->setSectionResizeMode(5, QHeaderView::Fixed);
        header->setSectionResizeMode(6, QHeaderView::Stretch);
        ui->tableData->setColumnWidth(0, 165);
        ui->tableData->setColumnWidth(1, 130);
        ui->tableData->setColumnWidth(2, 90);
        ui->tableData->setColumnWidth(3, 90);
        ui->tableData->setColumnWidth(4, 100);
        ui->tableData->setColumnWidth(5, 110);
    }

    ui->tableData->verticalHeader()->setDefaultSectionSize(24);
    ui->tableData->setAlternatingRowColors(false);
    ui->tableData->setSelectionBehavior(QAbstractItemView::SelectRows);
    ui->tableData->setEditTriggers(QAbstractItemView::NoEditTriggers);
    ui->tableData->setSortingEnabled(true);

    onQueryClicked();
}

QList<int> DataQueryWidget::checkedDeviceIds() const
{
    QList<int> ids;
    QTreeWidgetItem *root = ui->treeDevices->topLevelItem(0);
    if (!root) return ids;
    if (root->checkState(0) == Qt::Checked) {
        return ids;
    }
    appendCheckedDeviceIds(root, ids);
    return ids;
}

void DataQueryWidget::appendCheckedDeviceIds(QTreeWidgetItem *parent, QList<int> &ids) const
{
    if (!parent) return;
    for (int i = 0; i < parent->childCount(); ++i) {
        QTreeWidgetItem *child = parent->child(i);
        if (!child) continue;
        if (child->childCount() > 0) {
            appendCheckedDeviceIds(child, ids);
            continue;
        }
        if (child->checkState(0) == Qt::Checked) {
            ids.append(child->data(0, Qt::UserRole).toInt());
        }
    }
}

void DataQueryWidget::updateAncestorCheckState(QTreeWidgetItem *item)
{
    if (!item) return;
    bool allChecked = true;
    bool anyChecked = false;
    for (int i = 0; i < item->childCount(); ++i) {
        if (QTreeWidgetItem *child = item->child(i)) {
            const Qt::CheckState cs = child->checkState(0);
            if (cs == Qt::Checked) {
                anyChecked = true;
            } else if (cs == Qt::PartiallyChecked) {
                anyChecked = true;
                allChecked = false;
            } else {
                allChecked = false;
            }
        }
    }
    if (allChecked) {
        item->setCheckState(0, Qt::Checked);
    } else if (anyChecked) {
        item->setCheckState(0, Qt::PartiallyChecked);
    } else {
        item->setCheckState(0, Qt::Unchecked);
    }
    updateAncestorCheckState(item->parent());
}

DataQueryWidget::~DataQueryWidget()
{
    delete ui;
}

void DataQueryWidget::populateDeviceList()
{
    ui->cmbDevice->clear();
    ui->cmbDevice->addItem(tr("所有设备"), -1);
    ui->treeDevices->clear();

    QTreeWidgetItem *root = new QTreeWidgetItem(ui->treeDevices);
    root->setText(0, tr("全选"));
    root->setFlags(root->flags() | Qt::ItemIsUserCheckable);
    root->setCheckState(0, Qt::Checked);
    root->setData(0, Qt::UserRole, -1);

    QMap<QString, QList<DeviceInfo>> areaDevices;
    QList<DeviceInfo> devices = m_db->getAllDevices();
    for (const DeviceInfo &dev : devices) {
        if (!dev.enabled) continue;
        ui->cmbDevice->addItem(dev.name, dev.id);
        const QString area = dev.area.trimmed().isEmpty() ? tr("未分区") : dev.area.trimmed();
        areaDevices[area].append(dev);
    }

    QStringList areas = areaDevices.keys();
    areas.sort(Qt::CaseInsensitive);
    for (const QString &areaName : areas) {
        QTreeWidgetItem *areaItem = new QTreeWidgetItem(root);
        areaItem->setText(0, areaName);
        areaItem->setFlags(areaItem->flags() | Qt::ItemIsUserCheckable);
        areaItem->setCheckState(0, Qt::Checked);
        areaItem->setData(0, Qt::UserRole, -1);
        const QList<DeviceInfo> list = areaDevices.value(areaName);
        for (const DeviceInfo &dev : list) {
            QTreeWidgetItem *devItem = new QTreeWidgetItem(areaItem);
            devItem->setText(0, dev.name);
            devItem->setFlags(devItem->flags() | Qt::ItemIsUserCheckable);
            devItem->setCheckState(0, Qt::Checked);
            devItem->setData(0, Qt::UserRole, dev.id);
        }
        areaItem->setExpanded(true);
    }
    root->setExpanded(true);
}

void DataQueryWidget::onQueryClicked()
{
    QDateTime startTime = ui->dtStartTime->dateTime();
    QDateTime endTime = ui->dtEndTime->dateTime();
    int deviceId = ui->cmbDevice->currentData().toInt();
    const QList<int> treeSelectedIds = checkedDeviceIds();
    QTreeWidgetItem *root = ui->treeDevices->topLevelItem(0);
    const bool treeAllSelected = root && root->checkState(0) == Qt::Checked;

    int dataType = 0;
    if (ui->rbNormalData->isChecked()) dataType = 1;
    else if (ui->rbAbnormalData->isChecked()) dataType = 2;

    QList<SensorData> data = m_db->querySensorData(startTime, endTime, deviceId, dataType);

    // Apply filter if enabled
    if (ui->chkFilter->isChecked() && !ui->txtFilter->text().isEmpty()) {
        QRegularExpression rx(ui->txtFilter->text());
        QList<SensorData> filtered;
        filtered.reserve(data.size());
        for (const SensorData &sd : data) {
            if (rx.match(sd.deviceName).hasMatch()) {
                filtered.append(sd);
            }
        }
        data = std::move(filtered);
    }

    if (!treeAllSelected) {
        QList<SensorData> filtered;
        filtered.reserve(data.size());
        for (const SensorData &sd : data) {
            if (treeSelectedIds.contains(sd.deviceId)) {
                filtered.append(sd);
            }
        }
        data = std::move(filtered);
    }

    populateTable(data);
    updateCharts(data);
}

void DataQueryWidget::populateTable(const QList<SensorData> &data)
{
    ui->tableData->setRowCount(0);
    for (const SensorData &sd : data) {
        int row = ui->tableData->rowCount();
        ui->tableData->insertRow(row);
        ui->tableData->setItem(row, 0, new QTableWidgetItem(sd.recordTime.toString("yyyy-MM-dd HH:mm:ss")));
        ui->tableData->setItem(row, 1, new QTableWidgetItem(sd.deviceName));
        ui->tableData->setItem(row, 2, new QTableWidgetItem(QString::number(sd.temperature, 'f', 1)));
        ui->tableData->setItem(row, 3, new QTableWidgetItem(QString::number(sd.humidity, 'f', 1)));

        QString status;
        if (sd.tempAlarm && sd.humidAlarm) status = tr("温湿度超限");
        else if (sd.tempAlarm) status = tr("温度超限");
        else if (sd.humidAlarm) status = tr("湿度超限");
        else status = tr("正常");

        QTableWidgetItem *statusItem = new QTableWidgetItem(status);
        if (sd.tempAlarm || sd.humidAlarm) {
            statusItem->setForeground(Qt::red);
        }
        ui->tableData->setItem(row, 4, statusItem);
        ui->tableData->setItem(row, 5, new QTableWidgetItem(sd.handler));
        ui->tableData->setItem(row, 6, new QTableWidgetItem(sd.measures));
    }
}

void DataQueryWidget::updateCharts(const QList<SensorData> &data)
{
    // Group data by device for chart series
    QMap<QString, QLineSeries*> tempSeriesMap;
    QMap<QString, QLineSeries*> humidSeriesMap;

    for (const SensorData &sd : data) {
        if (!tempSeriesMap.contains(sd.deviceName)) {
            tempSeriesMap[sd.deviceName] = new QLineSeries();
            tempSeriesMap[sd.deviceName]->setName(sd.deviceName);
            humidSeriesMap[sd.deviceName] = new QLineSeries();
            humidSeriesMap[sd.deviceName]->setName(sd.deviceName);
        }
        qint64 ms = sd.recordTime.toMSecsSinceEpoch();
        tempSeriesMap[sd.deviceName]->append(ms, sd.temperature);
        humidSeriesMap[sd.deviceName]->append(ms, sd.humidity);
    }

    QChart *tempChart = new QChart();
    tempChart->setTitle(tr("温度曲线"));
    tempChart->legend()->setVisible(true);
    QChart *humidChart = new QChart();
    humidChart->setTitle(tr("湿度曲线"));
    humidChart->legend()->setVisible(true);

    qint64 minMs = std::numeric_limits<qint64>::max();
    qint64 maxMs = 0;
    double minTemp = std::numeric_limits<double>::max();
    double maxTemp = std::numeric_limits<double>::lowest();
    double minHumid = std::numeric_limits<double>::max();
    double maxHumid = std::numeric_limits<double>::lowest();

    for (QLineSeries *series : tempSeriesMap.values()) {
        tempChart->addSeries(series);
        for (const QPointF &pt : series->points()) {
            const qint64 ms = static_cast<qint64>(pt.x());
            minMs = qMin(minMs, ms);
            maxMs = qMax(maxMs, ms);
            minTemp = qMin(minTemp, pt.y());
            maxTemp = qMax(maxTemp, pt.y());
        }
    }
    for (QLineSeries *series : humidSeriesMap.values()) {
        humidChart->addSeries(series);
        for (const QPointF &pt : series->points()) {
            const qint64 ms = static_cast<qint64>(pt.x());
            minMs = qMin(minMs, ms);
            maxMs = qMax(maxMs, ms);
            minHumid = qMin(minHumid, pt.y());
            maxHumid = qMax(maxHumid, pt.y());
        }
    }

    if (!data.isEmpty()) {
        QDateTimeAxis *tempX = new QDateTimeAxis;
        tempX->setFormat("MM-dd HH:mm");
        tempX->setTitleText(tr("时间"));
        tempX->setRange(QDateTime::fromMSecsSinceEpoch(minMs), QDateTime::fromMSecsSinceEpoch(maxMs));
        tempChart->addAxis(tempX, Qt::AlignBottom);

        QValueAxis *tempY = new QValueAxis;
        tempY->setTitleText(tr("温度(°C)"));
        tempY->setRange(minTemp - 1.0, maxTemp + 1.0);
        tempChart->addAxis(tempY, Qt::AlignLeft);

        for (QLineSeries *series : tempSeriesMap.values()) {
            series->attachAxis(tempX);
            series->attachAxis(tempY);
        }

        QDateTimeAxis *humidX = new QDateTimeAxis;
        humidX->setFormat("MM-dd HH:mm");
        humidX->setTitleText(tr("时间"));
        humidX->setRange(QDateTime::fromMSecsSinceEpoch(minMs), QDateTime::fromMSecsSinceEpoch(maxMs));
        humidChart->addAxis(humidX, Qt::AlignBottom);

        QValueAxis *humidY = new QValueAxis;
        humidY->setTitleText(tr("湿度(%RH)"));
        humidY->setRange(qMax(0.0, minHumid - 5.0), qMin(100.0, maxHumid + 5.0));
        humidChart->addAxis(humidY, Qt::AlignLeft);

        for (QLineSeries *series : humidSeriesMap.values()) {
            series->attachAxis(humidX);
            series->attachAxis(humidY);
        }
    }

    if (m_tempChartView) m_tempChartView->setChart(tempChart);
    if (m_humidChartView) m_humidChartView->setChart(humidChart);
}

void DataQueryWidget::onExportPDFClicked()
{
    QString fileName = QFileDialog::getSaveFileName(this, tr("导出PDF"),
        QDir::homePath() + "/温湿度数据报表.pdf",
        tr("PDF文件 (*.pdf)"));
    if (fileName.isEmpty()) return;

    QPrinter printer(QPrinter::HighResolution);
    printer.setOutputFormat(QPrinter::PdfFormat);
    printer.setOutputFileName(fileName);
    printer.setPageSize(QPageSize(QPageSize::A4));
    printer.setPageOrientation(QPageLayout::Landscape);

    QPainter painter(&printer);
    painter.setRenderHint(QPainter::Antialiasing);

    // Draw title
    QFont titleFont("SimSun", 14, QFont::Bold);
    painter.setFont(titleFont);
    painter.drawText(QRect(0, 0, printer.width(), 100), Qt::AlignCenter,
                     tr("温湿度数据报表"));

    // Draw table header
    QFont headerFont("SimSun", 9, QFont::Bold);
    painter.setFont(headerFont);
    int y = 120;
    int colWidths[] = {300, 200, 100, 100, 100};
    QStringList headers = {tr("记录时间"), tr("仪表名称"), tr("温度"), tr("湿度"), tr("状态")};
    int x = 0;
    for (int i = 0; i < headers.size(); ++i) {
        painter.drawRect(x, y, colWidths[i], 60);
        painter.drawText(QRect(x, y, colWidths[i], 60), Qt::AlignCenter, headers[i]);
        x += colWidths[i];
    }

    // Draw data rows
    QFont dataFont("SimSun", 8);
    painter.setFont(dataFont);
    y += 60;
    int rowHeight = 50;
    for (int row = 0; row < ui->tableData->rowCount(); ++row) {
        if (y + rowHeight > printer.height() - 100) {
            printer.newPage();
            y = 50;
        }
        x = 0;
        for (int col = 0; col < 5 && col < ui->tableData->columnCount(); ++col) {
            QTableWidgetItem *item = ui->tableData->item(row, col);
            painter.drawRect(x, y, colWidths[col], rowHeight);
            painter.drawText(QRect(x + 5, y, colWidths[col] - 10, rowHeight),
                             Qt::AlignVCenter | Qt::AlignLeft,
                             item ? item->text() : "");
            x += colWidths[col];
        }
        y += rowHeight;
    }

    painter.end();
    QMessageBox::information(this, tr("导出成功"), tr("PDF已保存到：%1").arg(fileName));
}

void DataQueryWidget::onDeviceSelectionChanged()
{
    // Refresh query when device selection changes
}

void DataQueryWidget::onTreeItemChanged(QTreeWidgetItem *item, int column)
{
    if (!item || column != 0) return;
    QSignalBlocker blocker(ui->treeDevices);
    const Qt::CheckState st = item->checkState(0);

    if (item->childCount() > 0) {
        for (int i = 0; i < item->childCount(); ++i) {
            if (QTreeWidgetItem *child = item->child(i)) {
                child->setCheckState(0, st);
            }
        }
    }

    updateAncestorCheckState(item->parent());
}
