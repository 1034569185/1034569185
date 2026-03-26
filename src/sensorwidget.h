#pragma once

#include <QWidget>
#include "database/dbmanager.h"

QT_BEGIN_NAMESPACE
namespace Ui { class SensorWidget; }
QT_END_NAMESPACE

class SensorWidget : public QWidget
{
    Q_OBJECT
public:
    explicit SensorWidget(QWidget *parent = nullptr);
    ~SensorWidget();

    void setDeviceInfo(const DeviceInfo &device);
    void updateReading(double temperature, double humidity,
                       bool tempAlarm, bool humidAlarm);
    void setOffline();

private:
    Ui::SensorWidget *ui;
    DeviceInfo m_device;
};
