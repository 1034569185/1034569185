#pragma once

#include <QObject>
#include <QSerialPort>
#include <QTimer>
#include <QMap>
#include <QMutex>

struct SensorReading {
    int deviceAddress;
    double temperature;
    double humidity;
    bool valid;
    QString errorMsg;
};

class SerialManager : public QObject
{
    Q_OBJECT
public:
    explicit SerialManager(QObject *parent = nullptr);
    ~SerialManager();

    bool openPort(const QString &portName, int baudRate = 9600);
    void closePort();
    bool isOpen() const;
    QString portName() const;

    void startPolling(const QList<int> &deviceAddresses, int intervalMs = 10000);
    void stopPolling();
    bool isPolling() const;

    // 读取单个设备的温湿度（Modbus RTU协议）
    SensorReading readDevice(int deviceAddress);

    // 写报警配置到仪表
    bool writeAlarmConfig(int deviceAddress, double tempHigh, double tempLow,
                          double humidHigh, double humidLow);

    // 从仪表读配置
    bool readAlarmConfig(int deviceAddress, double &tempHigh, double &tempLow,
                         double &humidHigh, double &humidLow);

    QStringList availablePorts();

signals:
    void dataReceived(const SensorReading &reading);
    void pollingError(int deviceAddress, const QString &error);
    void portStatusChanged(bool opened);

private slots:
    void onPollTimer();
    void onReadyRead();

private:
    QByteArray buildModbusRequest(int deviceAddr, int functionCode,
                                   int startReg, int numRegs);
    static quint16 calcCRC(const QByteArray &data);
    bool sendAndReceive(const QByteArray &request, QByteArray &response,
                        int timeoutMs = 1000);
    SensorReading parseTemperatureHumidity(int deviceAddress, const QByteArray &response);

    QSerialPort *m_serialPort;
    QTimer *m_pollTimer;
    QList<int> m_deviceAddresses;
    int m_currentDeviceIndex;
    QMutex m_mutex;
    bool m_polling;
};
