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

QT_CHARTS_USE_NAMESPACE

DataQueryWidget::DataQueryWidget(DbManager *db, QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::DataQueryWidget)
    , m_db(db)
{
    ui->setupUi(this);

    // Set default time range: last 24 hours
    QDateTime now = QDateTime::currentDateTime();
    ui->dtEndTime->setDateTime(now);
    ui->dtStartTime->setDateTime(now.addDays(-1));

    populateDeviceList();

    connect(ui->btnQuery, &QPushButton::clicked, this, &DataQueryWidget::onQueryClicked);
    connect(ui->btnExportPDF, &QPushButton::clicked, this, &DataQueryWidget::onExportPDFClicked);

    // Setup chart placeholders
    QChartView *tempChartView = new QChartView(new QChart());
    tempChartView->chart()->setTitle(tr("温度曲线"));
    tempChartView->setRenderHint(QPainter::Antialiasing);
    QVBoxLayout *tempLayout = qobject_cast<QVBoxLayout*>(ui->tempChartLayout);
    if (tempLayout) {
        tempLayout->addWidget(tempChartView);
    }

    QChartView *humidChartView = new QChartView(new QChart());
    humidChartView->chart()->setTitle(tr("湿度曲线"));
    humidChartView->setRenderHint(QPainter::Antialiasing);
    QVBoxLayout *humidLayout = qobject_cast<QVBoxLayout*>(ui->humidChartLayout);
    if (humidLayout) {
        humidLayout->addWidget(humidChartView);
    }
}

DataQueryWidget::~DataQueryWidget()
{
    delete ui;
}

void DataQueryWidget::populateDeviceList()
{
    ui->cmbDevice->clear();
    ui->cmbDevice->addItem(tr("所有设备"), -1);
    ui->lstDevices->clear();
    ui->lstDevices->addItem(tr("所有设备"));

    QList<DeviceInfo> devices = m_db->getAllDevices();
    for (const DeviceInfo &dev : devices) {
        ui->cmbDevice->addItem(dev.name, dev.id);
        ui->lstDevices->addItem(dev.name);
    }
}

void DataQueryWidget::onQueryClicked()
{
    QDateTime startTime = ui->dtStartTime->dateTime();
    QDateTime endTime = ui->dtEndTime->dateTime();
    int deviceId = ui->cmbDevice->currentData().toInt();

    int dataType = 0;
    if (ui->rbNormalData->isChecked()) dataType = 1;
    else if (ui->rbAbnormalData->isChecked()) dataType = 2;

    QList<SensorData> data = m_db->querySensorData(startTime, endTime, deviceId, dataType);

    // Apply filter if enabled
    if (ui->chkFilter->isChecked() && !ui->txtFilter->text().isEmpty()) {
        QRegularExpression rx(ui->txtFilter->text());
        data.erase(std::remove_if(data.begin(), data.end(),
            [&rx](const SensorData &sd) {
                return !rx.match(sd.deviceName).hasMatch();
            }), data.end());
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

    // Update temperature chart
    QChart *tempChart = new QChart();
    tempChart->setTitle(tr("温度曲线"));
    for (QLineSeries *series : tempSeriesMap.values()) {
        tempChart->addSeries(series);
    }
    if (!data.isEmpty()) {
        QDateTimeAxis *axisX = new QDateTimeAxis;
        axisX->setFormat("MM-dd HH:mm");
        axisX->setTitleText(tr("时间"));
        tempChart->addAxis(axisX, Qt::AlignBottom);

        QValueAxis *axisY = new QValueAxis;
        axisY->setTitleText(tr("温度 (°C)"));
        tempChart->addAxis(axisY, Qt::AlignLeft);

        for (QLineSeries *series : tempSeriesMap.values()) {
            series->attachAxis(axisX);
            series->attachAxis(axisY);
        }
    }

    // Find and update chart views
    // (In practice, we'd keep references to chart views)
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
