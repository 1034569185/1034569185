#pragma once

#include <QObject>
#include <QSqlDatabase>
#include <QSqlQuery>
#include <QSqlError>
#include <QDateTime>
#include <QList>
#include <QString>
#include <QVariant>

struct DeviceInfo {
    int id;
    QString name;
    int address;
    bool enabled;
    QString area;
    double tempHigh;
    double tempLow;
    double humidHigh;
    double humidLow;
};

struct SensorData {
    int id;
    int deviceId;
    QString deviceName;
    QDateTime recordTime;
    double temperature;
    double humidity;
    bool tempAlarm;
    bool humidAlarm;
    QString handler;
    QString measures;
};

struct AlarmRecord {
    int id;
    int deviceId;
    QString deviceName;
    QDateTime alarmTime;
    QDateTime recoverTime;
    QString alarmType;
    double alarmValue;
    double limitValue;
    QString handler;
    QString measures;
};

struct UserInfo {
    int id;
    QString username;
    QString realName;
    QString phone;
    QString email;
    QString passwordHash;
    int permissions;
    bool active;
    QDateTime passwordExpiry;
};

struct SiteInfo {
    int id;
    QString name;
    QString hostname;
    QString connectId;
    QString connectPwd;
};

struct SystemLog {
    int id;
    QDateTime logTime;
    QString logType;
    QString username;
    QString operation;
    QString detail;
};

class DbManager : public QObject
{
    Q_OBJECT
public:
    explicit DbManager(QObject *parent = nullptr);
    ~DbManager();

    bool open(const QString &dbPath = QString());
    void close();
    bool isOpen() const;
    QString lastError() const;

    // 设备管理
    QList<DeviceInfo> getAllDevices();
    DeviceInfo getDevice(int deviceId);
    bool addDevice(const DeviceInfo &device);
    bool updateDevice(const DeviceInfo &device);
    bool deleteDevice(int deviceId);

    // 传感器数据
    bool insertSensorData(const SensorData &data);
    QList<SensorData> querySensorData(const QDateTime &startTime,
                                      const QDateTime &endTime,
                                      int deviceId = -1,
                                      int dataType = 0); // 0=all,1=normal,2=abnormal
    bool updateSensorDataRemark(int id, const QString &handler, const QString &measures);

    // 报警记录
    bool insertAlarmRecord(const AlarmRecord &alarm);
    bool updateAlarmRecover(int deviceId, const QDateTime &recoverTime);
    QList<AlarmRecord> queryAlarmRecords(const QDateTime &startTime,
                                         const QDateTime &endTime);
    bool updateAlarmRemark(int id, const QString &handler, const QString &measures);

    // 用户管理
    QList<UserInfo> getAllUsers();
    UserInfo getUserByName(const QString &username);
    bool addUser(const UserInfo &user);
    bool updateUser(const UserInfo &user);
    bool deleteUser(int userId);
    bool verifyPassword(const QString &username, const QString &password);
    bool changePassword(const QString &username, const QString &newPassword);

    // 站点管理
    QList<SiteInfo> getAllSites();
    bool addSite(const SiteInfo &site);
    bool updateSite(const SiteInfo &site);
    bool deleteSite(int siteId);

    // 参数配置
    QString getConfig(const QString &key, const QString &defaultValue = QString());
    bool setConfig(const QString &key, const QString &value);

    // 系统日志
    bool insertLog(const QString &logType, const QString &username,
                   const QString &operation, const QString &detail);
    QList<SystemLog> queryLogs(const QDateTime &startTime,
                                const QDateTime &endTime,
                                bool includeService = true,
                                bool includeUI = true);

private:
    bool createTables();
    bool insertDefaultAdmin();
    static QString hashPassword(const QString &password);

    QSqlDatabase m_db;
    QString m_lastError;
};
