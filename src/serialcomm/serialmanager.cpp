#include "serialmanager.h"
#include <QSerialPortInfo>
#include <QEventLoop>
#include <QTimer>
#include <QMutexLocker>
#include <QDebug>

SerialManager::SerialManager(QObject *parent)
    : QObject(parent)
    , m_serialPort(new QSerialPort(this))
    , m_pollTimer(new QTimer(this))
    , m_currentDeviceIndex(0)
    , m_polling(false)
{
    connect(m_pollTimer, &QTimer::timeout, this, &SerialManager::onPollTimer);
    connect(m_serialPort, &QSerialPort::readyRead, this, &SerialManager::onReadyRead);
}

SerialManager::~SerialManager()
{
    stopPolling();
    closePort();
}

bool SerialManager::openPort(const QString &portName, int baudRate)
{
    if (m_serialPort->isOpen()) {
        m_serialPort->close();
    }
    m_serialPort->setPortName(portName);
    m_serialPort->setBaudRate(baudRate);
    m_serialPort->setDataBits(QSerialPort::Data8);
    m_serialPort->setParity(QSerialPort::NoParity);
    m_serialPort->setStopBits(QSerialPort::OneStop);
    m_serialPort->setFlowControl(QSerialPort::NoFlowControl);

    if (!m_serialPort->open(QIODevice::ReadWrite)) {
        qWarning() << "Failed to open serial port" << portName << ":" << m_serialPort->errorString();
        emit portStatusChanged(false);
        return false;
    }
    emit portStatusChanged(true);
    return true;
}

void SerialManager::closePort()
{
    if (m_serialPort->isOpen()) {
        m_serialPort->close();
        emit portStatusChanged(false);
    }
}

bool SerialManager::isOpen() const
{
    return m_serialPort->isOpen();
}

QString SerialManager::portName() const
{
    return m_serialPort->portName();
}

void SerialManager::startPolling(const QList<int> &deviceAddresses, int intervalMs)
{
    m_deviceAddresses = deviceAddresses;
    m_currentDeviceIndex = 0;
    m_polling = true;
    m_pollTimer->start(intervalMs / qMax(1, deviceAddresses.size()));
}

void SerialManager::stopPolling()
{
    m_polling = false;
    m_pollTimer->stop();
}

bool SerialManager::isPolling() const
{
    return m_polling;
}

QStringList SerialManager::availablePorts()
{
    QStringList ports;
    for (const QSerialPortInfo &info : QSerialPortInfo::availablePorts()) {
        ports << info.portName();
    }
    return ports;
}

void SerialManager::onPollTimer()
{
    if (!m_polling || m_deviceAddresses.isEmpty() || !m_serialPort->isOpen()) return;
    if (m_currentDeviceIndex >= m_deviceAddresses.size()) {
        m_currentDeviceIndex = 0;
    }
    int addr = m_deviceAddresses.at(m_currentDeviceIndex);
    SensorReading reading = readDevice(addr);
    emit dataReceived(reading);
    if (!reading.valid) {
        emit pollingError(addr, reading.errorMsg);
    }
    ++m_currentDeviceIndex;
}

void SerialManager::onReadyRead()
{
    // Data is handled in sendAndReceive synchronously
}

// Modbus RTU: Read Holding Registers (FC03)
QByteArray SerialManager::buildModbusRequest(int deviceAddr, int functionCode,
                                               int startReg, int numRegs)
{
    QByteArray pdu;
    pdu.append(static_cast<char>(deviceAddr & 0xFF));
    pdu.append(static_cast<char>(functionCode & 0xFF));
    pdu.append(static_cast<char>((startReg >> 8) & 0xFF));
    pdu.append(static_cast<char>(startReg & 0xFF));
    pdu.append(static_cast<char>((numRegs >> 8) & 0xFF));
    pdu.append(static_cast<char>(numRegs & 0xFF));
    quint16 crc = calcCRC(pdu);
    pdu.append(static_cast<char>(crc & 0xFF));
    pdu.append(static_cast<char>((crc >> 8) & 0xFF));
    return pdu;
}

quint16 SerialManager::calcCRC(const QByteArray &data)
{
    quint16 crc = 0xFFFF;
    for (unsigned char byte : data) {
        crc ^= byte;
        for (int i = 0; i < 8; ++i) {
            if (crc & 0x0001) {
                crc = (crc >> 1) ^ 0xA001;
            } else {
                crc >>= 1;
            }
        }
    }
    return crc;
}

bool SerialManager::sendAndReceive(const QByteArray &request, QByteArray &response, int timeoutMs)
{
    QMutexLocker locker(&m_mutex);
    if (!m_serialPort->isOpen()) return false;

    m_serialPort->clear();
    m_serialPort->write(request);
    if (!m_serialPort->waitForBytesWritten(timeoutMs)) {
        return false;
    }

    QEventLoop loop;
    QTimer timer;
    timer.setSingleShot(true);
    connect(&timer, &QTimer::timeout, &loop, &QEventLoop::quit);
    connect(m_serialPort, &QSerialPort::readyRead, &loop, &QEventLoop::quit);
    timer.start(timeoutMs);
    loop.exec();

    response = m_serialPort->readAll();
    return !response.isEmpty();
}

SensorReading SerialManager::readDevice(int deviceAddress)
{
    SensorReading result;
    result.deviceAddress = deviceAddress;
    result.valid = false;

    // Read 2 registers starting from 0x0000 (temperature=reg0, humidity=reg1)
    // This assumes a common RS485 temp/humid sensor Modbus register mapping
    QByteArray request = buildModbusRequest(deviceAddress, 0x03, 0x0000, 0x0002);
    QByteArray response;

    if (!sendAndReceive(request, response, 1000)) {
        result.errorMsg = QString("设备%1通信超时").arg(deviceAddress);
        return result;
    }

    return parseTemperatureHumidity(deviceAddress, response);
}

SensorReading SerialManager::parseTemperatureHumidity(int deviceAddress, const QByteArray &response)
{
    SensorReading result;
    result.deviceAddress = deviceAddress;
    result.valid = false;

    // Modbus FC03 response: addr(1) + fc(1) + byteCount(1) + data(N) + crc(2)
    if (response.size() < 9) {
        result.errorMsg = QString("设备%1响应数据不足").arg(deviceAddress);
        return result;
    }

    if ((unsigned char)response[0] != (unsigned char)(deviceAddress & 0xFF)) {
        result.errorMsg = QString("设备%1地址不匹配").arg(deviceAddress);
        return result;
    }

    if ((unsigned char)response[1] != 0x03) {
        result.errorMsg = QString("设备%1功能码错误").arg(deviceAddress);
        return result;
    }

    // Verify CRC (Modbus RTU: low byte first, then high byte)
    QByteArray dataForCRC = response.left(response.size() - 2);
    quint16 expectedCRC = calcCRC(dataForCRC);
    quint16 receivedCRC = ((unsigned char)response[response.size()-2]) |
                          (((unsigned char)response[response.size()-1]) << 8);
    if (expectedCRC != receivedCRC) {
        result.errorMsg = QString("设备%1CRC校验失败").arg(deviceAddress);
        return result;
    }

    // Parse temperature (signed 16-bit, 0.1 precision)
    qint16 rawTemp = ((unsigned char)response[3] << 8) | (unsigned char)response[4];
    // Parse humidity (unsigned 16-bit, 0.1 precision)
    quint16 rawHumid = ((unsigned char)response[5] << 8) | (unsigned char)response[6];

    result.temperature = rawTemp / 10.0;
    result.humidity = rawHumid / 10.0;
    result.valid = true;
    return result;
}

bool SerialManager::writeAlarmConfig(int deviceAddress, double tempHigh, double tempLow,
                                      double humidHigh, double humidLow)
{
    // Write 4 registers starting from 0x0010
    // FC16: Write Multiple Registers
    QByteArray request;
    request.append(static_cast<char>(deviceAddress));
    request.append(static_cast<char>(0x10)); // FC16
    request.append(static_cast<char>(0x00)); // start reg high
    request.append(static_cast<char>(0x10)); // start reg low (reg 16)
    request.append(static_cast<char>(0x00)); // num regs high
    request.append(static_cast<char>(0x04)); // num regs low
    request.append(static_cast<char>(0x08)); // byte count

    qint16 th = static_cast<qint16>(tempHigh * 10);
    qint16 tl = static_cast<qint16>(tempLow * 10);
    qint16 hh = static_cast<qint16>(humidHigh * 10);
    qint16 hl = static_cast<qint16>(humidLow * 10);

    request.append(static_cast<char>((th >> 8) & 0xFF));
    request.append(static_cast<char>(th & 0xFF));
    request.append(static_cast<char>((tl >> 8) & 0xFF));
    request.append(static_cast<char>(tl & 0xFF));
    request.append(static_cast<char>((hh >> 8) & 0xFF));
    request.append(static_cast<char>(hh & 0xFF));
    request.append(static_cast<char>((hl >> 8) & 0xFF));
    request.append(static_cast<char>(hl & 0xFF));

    quint16 crc = calcCRC(request);
    request.append(static_cast<char>(crc & 0xFF));
    request.append(static_cast<char>((crc >> 8) & 0xFF));

    QByteArray response;
    return sendAndReceive(request, response, 2000) && response.size() >= 8;
}

bool SerialManager::readAlarmConfig(int deviceAddress, double &tempHigh, double &tempLow,
                                     double &humidHigh, double &humidLow)
{
    // Read 4 registers starting from 0x0010
    QByteArray request = buildModbusRequest(deviceAddress, 0x03, 0x0010, 0x0004);
    QByteArray response;
    if (!sendAndReceive(request, response, 1000)) return false;
    if (response.size() < 13) return false;

    qint16 th = ((unsigned char)response[3] << 8) | (unsigned char)response[4];
    qint16 tl = ((unsigned char)response[5] << 8) | (unsigned char)response[6];
    qint16 hh = ((unsigned char)response[7] << 8) | (unsigned char)response[8];
    qint16 hl = ((unsigned char)response[9] << 8) | (unsigned char)response[10];

    tempHigh = th / 10.0;
    tempLow = tl / 10.0;
    humidHigh = hh / 10.0;
    humidLow = hl / 10.0;
    return true;
}
