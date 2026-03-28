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
        ? "QLabel { font-size: 23px; font-weight: bold; color: #e74c3c; }"
        : "QLabel { font-size: 23px; font-weight: bold; color: #2b7fba; }";
    QString humidStyle = humidAlarm
        ? "QLabel { font-size: 23px; font-weight: bold; color: #e74c3c; }"
        : "QLabel { font-size: 23px; font-weight: bold; color: #2b7fba; }";

    // For below-limit alarms, use blue for temperature too
    if (tempAlarm && temperature < m_device.tempLow) {
        tempStyle = "QLabel { font-size: 23px; font-weight: bold; color: #3498db; }";
    }
    if (humidAlarm && humidity < m_device.humidLow) {
        humidStyle = "QLabel { font-size: 23px; font-weight: bold; color: #3498db; }";
    }

    ui->lblTemperature->setStyleSheet(tempStyle);
    ui->lblHumidity->setStyleSheet(humidStyle);

    // Background highlight when alarm (keep consistent with global QSS)
    if (tempAlarm || humidAlarm) {
        setStyleSheet("QWidget#SensorWidget { border: 2px solid #e74c3c; border-radius: 6px; background-color: #eef6ff; }");
    } else {
        setStyleSheet("QWidget#SensorWidget { border: 1px solid #7F9AB8; border-radius: 6px; background-color: #CFDDEE; }");
    }
}

void SensorWidget::setOffline()
{
    ui->lblTemperature->setText("--.-");
    ui->lblHumidity->setText("--.-");
    ui->lblLastOnline->setText(tr("设备不在线"));
    ui->lblTemperature->setStyleSheet("QLabel { font-size: 23px; font-weight: bold; color: #7f8c8d; }");
    ui->lblHumidity->setStyleSheet("QLabel { font-size: 23px; font-weight: bold; color: #7f8c8d; }");
    setStyleSheet("QWidget#SensorWidget { border: 1px solid #7F9AB8; border-radius: 6px; background-color: #D7E4F3; }");
}
