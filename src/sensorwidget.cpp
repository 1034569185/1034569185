#include "sensorwidget.h"
#include "ui_sensorwidget.h"
#include <QDateTime>

SensorWidget::SensorWidget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::SensorWidget)
{
    ui->setupUi(this);
}

SensorWidget::~SensorWidget()
{
    delete ui;
}

void SensorWidget::setDeviceInfo(const DeviceInfo &device)
{
    m_device = device;
    ui->lblSensorName->setText(device.name);
    ui->lblTempHigh->setText(tr("上限: %1°C").arg(device.tempHigh, 0, 'f', 1));
    ui->lblTempLow->setText(tr("下限: %1°C").arg(device.tempLow, 0, 'f', 1));
    ui->lblHumidHigh->setText(tr("上限: %1%%").arg(device.humidHigh, 0, 'f', 1));
    ui->lblHumidLow->setText(tr("下限: %1%%").arg(device.humidLow, 0, 'f', 1));
    setOffline();
}

void SensorWidget::updateReading(double temperature, double humidity,
                                  bool tempAlarm, bool humidAlarm)
{
    ui->lblTemperature->setText(QString::number(temperature, 'f', 1));
    ui->lblHumidity->setText(QString::number(humidity, 'f', 1));
    ui->lblLastOnline->setText(tr("最后在线: %1").arg(
        QDateTime::currentDateTime().toString("HH:mm:ss")));

    // Set alarm colors
    QString tempStyle = tempAlarm
        ? "QLabel { font-size: 22px; font-weight: bold; color: #e74c3c; }"
        : "QLabel { font-size: 22px; font-weight: bold; color: #27ae60; }";
    QString humidStyle = humidAlarm
        ? "QLabel { font-size: 22px; font-weight: bold; color: #e74c3c; }"
        : "QLabel { font-size: 22px; font-weight: bold; color: #3498db; }";

    // For below-limit alarms, use blue for temperature too
    if (tempAlarm && temperature < m_device.tempLow) {
        tempStyle = "QLabel { font-size: 22px; font-weight: bold; color: #3498db; }";
    }
    if (humidAlarm && humidity < m_device.humidLow) {
        humidStyle = "QLabel { font-size: 22px; font-weight: bold; color: #3498db; }";
    }

    ui->lblTemperature->setStyleSheet(tempStyle);
    ui->lblHumidity->setStyleSheet(humidStyle);

    // Background highlight when alarm
    if (tempAlarm || humidAlarm) {
        setStyleSheet("QWidget#SensorWidget { background-color: #fdecea; border: 2px solid #e74c3c; border-radius: 6px; }");
    } else {
        setStyleSheet("QWidget#SensorWidget { background-color: #eafaf1; border: 1px solid #bdc3c7; border-radius: 6px; }");
    }
}

void SensorWidget::setOffline()
{
    ui->lblTemperature->setText("--.-");
    ui->lblHumidity->setText("--.-");
    ui->lblLastOnline->setText(tr("设备不在线"));
    ui->lblTemperature->setStyleSheet("QLabel { font-size: 22px; font-weight: bold; color: #95a5a6; }");
    ui->lblHumidity->setStyleSheet("QLabel { font-size: 22px; font-weight: bold; color: #95a5a6; }");
    setStyleSheet("QWidget#SensorWidget { background-color: #ecf0f1; border: 1px solid #bdc3c7; border-radius: 6px; }");
}
