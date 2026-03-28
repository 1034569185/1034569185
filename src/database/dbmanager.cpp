#include "dbmanager.h"
#include <QSqlRecord>
#include <QCryptographicHash>
#include <QStandardPaths>
#include <QDir>
#include <QDebug>

DbManager::DbManager(QObject *parent)
    : QObject(parent)
{
}

DbManager::~DbManager()
{
    close();
}

bool DbManager::open(const QString &dbPath)
{
    QString path = dbPath;
    if (path.isEmpty()) {
        QString dataDir = QStandardPaths::writableLocation(QStandardPaths::AppDataLocation);
        QDir().mkpath(dataDir);
        path = dataDir + "/hongruan_temp_humid.db";
    }

    m_db = QSqlDatabase::addDatabase("QSQLITE", "hongruan_main");
    m_db.setDatabaseName(path);

    if (!m_db.open()) {
        m_lastError = m_db.lastError().text();
        qCritical() << "Failed to open database:" << m_lastError;
        return false;
    }

    if (!createTables()) {
        return false;
    }

    return true;
}

void DbManager::close()
{
    if (m_db.isOpen()) {
        m_db.close();
    }
    QSqlDatabase::removeDatabase("hongruan_main");
}

bool DbManager::isOpen() const
{
    return m_db.isOpen();
}

QString DbManager::lastError() const
{
    return m_lastError;
}

bool DbManager::createTables()
{
    QSqlQuery q(m_db);

    // 设备表
    if (!q.exec(R"(
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address INTEGER NOT NULL UNIQUE,
            enabled INTEGER NOT NULL DEFAULT 1,
            area TEXT,
            temp_high REAL DEFAULT 30.0,
            temp_low REAL DEFAULT 0.0,
            humid_high REAL DEFAULT 80.0,
            humid_low REAL DEFAULT 20.0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    )")) {
        m_lastError = q.lastError().text();
        return false;
    }

    // 传感器数据表
    if (!q.exec(R"(
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER NOT NULL,
            device_name TEXT,
            record_time DATETIME NOT NULL,
            temperature REAL,
            humidity REAL,
            temp_alarm INTEGER DEFAULT 0,
            humid_alarm INTEGER DEFAULT 0,
            handler TEXT,
            measures TEXT,
            FOREIGN KEY (device_id) REFERENCES devices(id)
        )
    )")) {
        m_lastError = q.lastError().text();
        return false;
    }
    q.exec("CREATE INDEX IF NOT EXISTS idx_sensor_time ON sensor_data(record_time)");
    q.exec("CREATE INDEX IF NOT EXISTS idx_sensor_device ON sensor_data(device_id)");

    // 报警记录表
    if (!q.exec(R"(
        CREATE TABLE IF NOT EXISTS alarm_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER NOT NULL,
            device_name TEXT,
            alarm_time DATETIME NOT NULL,
            recover_time DATETIME,
            alarm_type TEXT,
            alarm_value REAL,
            limit_value REAL,
            handler TEXT,
            measures TEXT,
            FOREIGN KEY (device_id) REFERENCES devices(id)
        )
    )")) {
        m_lastError = q.lastError().text();
        return false;
    }
    q.exec("CREATE INDEX IF NOT EXISTS idx_alarm_time ON alarm_records(alarm_time)");

    // 用户表
    if (!q.exec(R"(
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            real_name TEXT,
            phone TEXT,
            email TEXT,
            password_hash TEXT NOT NULL,
            permissions INTEGER DEFAULT 0,
            active INTEGER DEFAULT 1,
            password_expiry DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    )")) {
        m_lastError = q.lastError().text();
        return false;
    }

    // 报警接收人员表
    if (!q.exec(R"(
        CREATE TABLE IF NOT EXISTS alarm_recipients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            phone TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    )")) {
        m_lastError = q.lastError().text();
        return false;
    }

    // 站点表
    if (!q.exec(R"(
        CREATE TABLE IF NOT EXISTS sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            hostname TEXT NOT NULL,
            connect_id TEXT,
            connect_pwd TEXT
        )
    )")) {
        m_lastError = q.lastError().text();
        return false;
    }

    // 系统配置表
    if (!q.exec(R"(
        CREATE TABLE IF NOT EXISTS system_config (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    )")) {
        m_lastError = q.lastError().text();
        return false;
    }

    // 系统日志表
    if (!q.exec(R"(
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_time DATETIME NOT NULL,
            log_type TEXT,
            username TEXT,
            operation TEXT,
            detail TEXT
        )
    )")) {
        m_lastError = q.lastError().text();
        return false;
    }
    q.exec("CREATE INDEX IF NOT EXISTS idx_log_time ON system_logs(log_time)");

    // 插入默认管理员（如果不存在）
    insertDefaultAdmin();

    // 插入默认配置
    QStringList defaults = {
        "warehouse_name|温湿度监测库房",
        "record_interval|5",
        "alarm_volume|10",
        "all_area_name|全部",
        "software_title|鸿软温湿度监测系统",
        "send_sms_on_recover|0",
        "send_sms_on_alarm|1",
        "target_ip|",
        "target_port|8080",
        "backup_dir|",
        "pwd_expire_days|90",
        "enable_email|0",
        "email_account|",
        "email_auth_code|"
    };
    for (const QString &entry : defaults) {
        QStringList kv = entry.split("|");
        if (kv.size() == 2) {
            q.prepare("INSERT OR IGNORE INTO system_config(key,value) VALUES(?,?)");
            q.addBindValue(kv[0]);
            q.addBindValue(kv[1]);
            q.exec();
        }
    }

    return true;
}

bool DbManager::insertDefaultAdmin()
{
    QSqlQuery q(m_db);
    q.prepare("SELECT COUNT(*) FROM users WHERE username = 'admin'");
    if (!q.exec() || !q.next()) return false;
    if (q.value(0).toInt() > 0) return true;

    q.prepare(R"(
        INSERT INTO users(username, real_name, password_hash, permissions, active)
        VALUES('admin', '系统管理员', ?, -1, 1)
    )");
    q.addBindValue(hashPassword("admin123"));
    return q.exec();
}

QString DbManager::hashPassword(const QString &password)
{
    return QCryptographicHash::hash(
        password.toUtf8(), QCryptographicHash::Sha256).toHex();
}

// ---- 设备管理 ----

QList<DeviceInfo> DbManager::getAllDevices()
{
    QList<DeviceInfo> list;
    QSqlQuery q(m_db);
    q.exec("SELECT id,name,address,enabled,area,temp_high,temp_low,humid_high,humid_low FROM devices ORDER BY address");
    while (q.next()) {
        DeviceInfo d;
        d.id = q.value(0).toInt();
        d.name = q.value(1).toString();
        d.address = q.value(2).toInt();
        d.enabled = q.value(3).toBool();
        d.area = q.value(4).toString();
        d.tempHigh = q.value(5).toDouble();
        d.tempLow = q.value(6).toDouble();
        d.humidHigh = q.value(7).toDouble();
        d.humidLow = q.value(8).toDouble();
        list.append(d);
    }
    return list;
}

DeviceInfo DbManager::getDevice(int deviceId)
{
    DeviceInfo d;
    d.id = -1;
    QSqlQuery q(m_db);
    q.prepare("SELECT id,name,address,enabled,area,temp_high,temp_low,humid_high,humid_low FROM devices WHERE id=?");
    q.addBindValue(deviceId);
    if (q.exec() && q.next()) {
        d.id = q.value(0).toInt();
        d.name = q.value(1).toString();
        d.address = q.value(2).toInt();
        d.enabled = q.value(3).toBool();
        d.area = q.value(4).toString();
        d.tempHigh = q.value(5).toDouble();
        d.tempLow = q.value(6).toDouble();
        d.humidHigh = q.value(7).toDouble();
        d.humidLow = q.value(8).toDouble();
    }
    return d;
}

bool DbManager::addDevice(const DeviceInfo &device)
{
    QSqlQuery q(m_db);
    q.prepare(R"(
        INSERT INTO devices(name,address,enabled,area,temp_high,temp_low,humid_high,humid_low)
        VALUES(?,?,?,?,?,?,?,?)
    )");
    q.addBindValue(device.name);
    q.addBindValue(device.address);
    q.addBindValue(device.enabled ? 1 : 0);
    q.addBindValue(device.area);
    q.addBindValue(device.tempHigh);
    q.addBindValue(device.tempLow);
    q.addBindValue(device.humidHigh);
    q.addBindValue(device.humidLow);
    if (!q.exec()) {
        m_lastError = q.lastError().text();
        return false;
    }
    return true;
}

bool DbManager::updateDevice(const DeviceInfo &device)
{
    QSqlQuery q(m_db);
    q.prepare(R"(
        UPDATE devices SET name=?,address=?,enabled=?,area=?,
        temp_high=?,temp_low=?,humid_high=?,humid_low=?,
        updated_at=CURRENT_TIMESTAMP WHERE id=?
    )");
    q.addBindValue(device.name);
    q.addBindValue(device.address);
    q.addBindValue(device.enabled ? 1 : 0);
    q.addBindValue(device.area);
    q.addBindValue(device.tempHigh);
    q.addBindValue(device.tempLow);
    q.addBindValue(device.humidHigh);
    q.addBindValue(device.humidLow);
    q.addBindValue(device.id);
    if (!q.exec()) {
        m_lastError = q.lastError().text();
        return false;
    }
    return true;
}

bool DbManager::deleteDevice(int deviceId)
{
    QSqlQuery q(m_db);
    q.prepare("DELETE FROM devices WHERE id=?");
    q.addBindValue(deviceId);
    if (!q.exec()) {
        m_lastError = q.lastError().text();
        return false;
    }
    return true;
}

// ---- 传感器数据 ----

bool DbManager::insertSensorData(const SensorData &data)
{
    QSqlQuery q(m_db);
    q.prepare(R"(
        INSERT INTO sensor_data(device_id,device_name,record_time,temperature,humidity,temp_alarm,humid_alarm)
        VALUES(?,?,?,?,?,?,?)
    )");
    q.addBindValue(data.deviceId);
    q.addBindValue(data.deviceName);
    q.addBindValue(data.recordTime.toString(Qt::ISODate));
    q.addBindValue(data.temperature);
    q.addBindValue(data.humidity);
    q.addBindValue(data.tempAlarm ? 1 : 0);
    q.addBindValue(data.humidAlarm ? 1 : 0);
    if (!q.exec()) {
        m_lastError = q.lastError().text();
        return false;
    }
    return true;
}

QList<SensorData> DbManager::querySensorData(const QDateTime &startTime,
                                               const QDateTime &endTime,
                                               int deviceId,
                                               int dataType)
{
    QList<SensorData> list;
    QString sql = R"(
        SELECT id,device_id,device_name,record_time,temperature,humidity,
               temp_alarm,humid_alarm,handler,measures
        FROM sensor_data WHERE record_time BETWEEN ? AND ?
    )";
    if (deviceId > 0) sql += " AND device_id=" + QString::number(deviceId);
    if (dataType == 1) sql += " AND temp_alarm=0 AND humid_alarm=0";
    else if (dataType == 2) sql += " AND (temp_alarm=1 OR humid_alarm=1)";
    sql += " ORDER BY record_time DESC";

    QSqlQuery q(m_db);
    q.prepare(sql);
    q.addBindValue(startTime.toString(Qt::ISODate));
    q.addBindValue(endTime.toString(Qt::ISODate));
    if (!q.exec()) {
        m_lastError = q.lastError().text();
        return list;
    }
    while (q.next()) {
        SensorData d;
        d.id = q.value(0).toInt();
        d.deviceId = q.value(1).toInt();
        d.deviceName = q.value(2).toString();
        d.recordTime = QDateTime::fromString(q.value(3).toString(), Qt::ISODate);
        d.temperature = q.value(4).toDouble();
        d.humidity = q.value(5).toDouble();
        d.tempAlarm = q.value(6).toBool();
        d.humidAlarm = q.value(7).toBool();
        d.handler = q.value(8).toString();
        d.measures = q.value(9).toString();
        list.append(d);
    }
    return list;
}

bool DbManager::updateSensorDataRemark(int id, const QString &handler, const QString &measures)
{
    QSqlQuery q(m_db);
    q.prepare("UPDATE sensor_data SET handler=?,measures=? WHERE id=?");
    q.addBindValue(handler);
    q.addBindValue(measures);
    q.addBindValue(id);
    return q.exec();
}

// ---- 报警记录 ----

bool DbManager::insertAlarmRecord(const AlarmRecord &alarm)
{
    QSqlQuery q(m_db);
    q.prepare(R"(
        INSERT INTO alarm_records(device_id,device_name,alarm_time,alarm_type,alarm_value,limit_value)
        VALUES(?,?,?,?,?,?)
    )");
    q.addBindValue(alarm.deviceId);
    q.addBindValue(alarm.deviceName);
    q.addBindValue(alarm.alarmTime.toString(Qt::ISODate));
    q.addBindValue(alarm.alarmType);
    q.addBindValue(alarm.alarmValue);
    q.addBindValue(alarm.limitValue);
    if (!q.exec()) {
        m_lastError = q.lastError().text();
        return false;
    }
    return true;
}

bool DbManager::updateAlarmRecover(int deviceId, const QDateTime &recoverTime)
{
    QSqlQuery q(m_db);
    q.prepare("UPDATE alarm_records SET recover_time=? WHERE device_id=? AND recover_time IS NULL");
    q.addBindValue(recoverTime.toString(Qt::ISODate));
    q.addBindValue(deviceId);
    return q.exec();
}

QList<AlarmRecord> DbManager::queryAlarmRecords(const QDateTime &startTime,
                                                  const QDateTime &endTime)
{
    QList<AlarmRecord> list;
    QSqlQuery q(m_db);
    q.prepare(R"(
        SELECT id,device_id,device_name,alarm_time,recover_time,alarm_type,
               alarm_value,limit_value,handler,measures
        FROM alarm_records WHERE alarm_time BETWEEN ? AND ?
        ORDER BY alarm_time DESC
    )");
    q.addBindValue(startTime.toString(Qt::ISODate));
    q.addBindValue(endTime.toString(Qt::ISODate));
    if (!q.exec()) {
        m_lastError = q.lastError().text();
        return list;
    }
    while (q.next()) {
        AlarmRecord a;
        a.id = q.value(0).toInt();
        a.deviceId = q.value(1).toInt();
        a.deviceName = q.value(2).toString();
        a.alarmTime = QDateTime::fromString(q.value(3).toString(), Qt::ISODate);
        a.recoverTime = QDateTime::fromString(q.value(4).toString(), Qt::ISODate);
        a.alarmType = q.value(5).toString();
        a.alarmValue = q.value(6).toDouble();
        a.limitValue = q.value(7).toDouble();
        a.handler = q.value(8).toString();
        a.measures = q.value(9).toString();
        list.append(a);
    }
    return list;
}

bool DbManager::updateAlarmRemark(int id, const QString &handler, const QString &measures)
{
    QSqlQuery q(m_db);
    q.prepare("UPDATE alarm_records SET handler=?,measures=? WHERE id=?");
    q.addBindValue(handler);
    q.addBindValue(measures);
    q.addBindValue(id);
    return q.exec();
}

// ---- 用户管理 ----

QList<UserInfo> DbManager::getAllUsers()
{
    QList<UserInfo> list;
    QSqlQuery q(m_db);
    q.exec("SELECT id,username,real_name,phone,email,password_hash,permissions,active,password_expiry FROM users");
    while (q.next()) {
        UserInfo u;
        u.id = q.value(0).toInt();
        u.username = q.value(1).toString();
        u.realName = q.value(2).toString();
        u.phone = q.value(3).toString();
        u.email = q.value(4).toString();
        u.passwordHash = q.value(5).toString();
        u.permissions = q.value(6).toInt();
        u.active = q.value(7).toBool();
        u.passwordExpiry = QDateTime::fromString(q.value(8).toString(), Qt::ISODate);
        list.append(u);
    }
    return list;
}

UserInfo DbManager::getUserByName(const QString &username)
{
    UserInfo u;
    u.id = -1;
    QSqlQuery q(m_db);
    q.prepare("SELECT id,username,real_name,phone,email,password_hash,permissions,active,password_expiry FROM users WHERE username=?");
    q.addBindValue(username);
    if (q.exec() && q.next()) {
        u.id = q.value(0).toInt();
        u.username = q.value(1).toString();
        u.realName = q.value(2).toString();
        u.phone = q.value(3).toString();
        u.email = q.value(4).toString();
        u.passwordHash = q.value(5).toString();
        u.permissions = q.value(6).toInt();
        u.active = q.value(7).toBool();
        u.passwordExpiry = QDateTime::fromString(q.value(8).toString(), Qt::ISODate);
    }
    return u;
}

bool DbManager::addUser(const UserInfo &user)
{
    QSqlQuery q(m_db);
    q.prepare(R"(
        INSERT INTO users(username,real_name,phone,email,password_hash,permissions,active,password_expiry)
        VALUES(?,?,?,?,?,?,?,?)
    )");
    q.addBindValue(user.username);
    q.addBindValue(user.realName);
    q.addBindValue(user.phone);
    q.addBindValue(user.email);
    q.addBindValue(user.passwordHash);
    q.addBindValue(user.permissions);
    q.addBindValue(user.active ? 1 : 0);
    q.addBindValue(user.passwordExpiry.isValid() ? user.passwordExpiry.toString(Qt::ISODate) : QVariant());
    if (!q.exec()) {
        m_lastError = q.lastError().text();
        return false;
    }
    return true;
}

bool DbManager::updateUser(const UserInfo &user)
{
    QSqlQuery q(m_db);
    q.prepare(R"(
        UPDATE users SET real_name=?,phone=?,email=?,permissions=?,active=?,password_expiry=? WHERE id=?
    )");
    q.addBindValue(user.realName);
    q.addBindValue(user.phone);
    q.addBindValue(user.email);
    q.addBindValue(user.permissions);
    q.addBindValue(user.active ? 1 : 0);
    q.addBindValue(user.passwordExpiry.isValid() ? user.passwordExpiry.toString(Qt::ISODate) : QVariant());
    q.addBindValue(user.id);
    if (!q.exec()) {
        m_lastError = q.lastError().text();
        return false;
    }
    return true;
}

bool DbManager::deleteUser(int userId)
{
    QSqlQuery q(m_db);
    q.prepare("DELETE FROM users WHERE id=?");
    q.addBindValue(userId);
    if (!q.exec()) {
        m_lastError = q.lastError().text();
        return false;
    }
    return true;
}

bool DbManager::verifyPassword(const QString &username, const QString &password)
{
    UserInfo u = getUserByName(username);
    if (u.id < 0 || !u.active) return false;
    return u.passwordHash == hashPassword(password);
}

bool DbManager::changePassword(const QString &username, const QString &newPassword)
{
    QSqlQuery q(m_db);
    q.prepare("UPDATE users SET password_hash=? WHERE username=?");
    q.addBindValue(hashPassword(newPassword));
    q.addBindValue(username);
    return q.exec();
}

// ---- 站点管理 ----

QList<SiteInfo> DbManager::getAllSites()
{
    QList<SiteInfo> list;
    QSqlQuery q(m_db);
    q.exec("SELECT id,name,hostname,connect_id,connect_pwd FROM sites");
    while (q.next()) {
        SiteInfo s;
        s.id = q.value(0).toInt();
        s.name = q.value(1).toString();
        s.hostname = q.value(2).toString();
        s.connectId = q.value(3).toString();
        s.connectPwd = q.value(4).toString();
        list.append(s);
    }
    return list;
}

bool DbManager::addSite(const SiteInfo &site)
{
    QSqlQuery q(m_db);
    q.prepare("INSERT INTO sites(name,hostname,connect_id,connect_pwd) VALUES(?,?,?,?)");
    q.addBindValue(site.name);
    q.addBindValue(site.hostname);
    q.addBindValue(site.connectId);
    q.addBindValue(site.connectPwd);
    if (!q.exec()) {
        m_lastError = q.lastError().text();
        return false;
    }
    return true;
}

bool DbManager::updateSite(const SiteInfo &site)
{
    QSqlQuery q(m_db);
    q.prepare("UPDATE sites SET name=?,hostname=?,connect_id=?,connect_pwd=? WHERE id=?");
    q.addBindValue(site.name);
    q.addBindValue(site.hostname);
    q.addBindValue(site.connectId);
    q.addBindValue(site.connectPwd);
    q.addBindValue(site.id);
    if (!q.exec()) {
        m_lastError = q.lastError().text();
        return false;
    }
    return true;
}

bool DbManager::deleteSite(int siteId)
{
    QSqlQuery q(m_db);
    q.prepare("DELETE FROM sites WHERE id=?");
    q.addBindValue(siteId);
    if (!q.exec()) {
        m_lastError = q.lastError().text();
        return false;
    }
    return true;
}

// ---- 参数配置 ----

QString DbManager::getConfig(const QString &key, const QString &defaultValue)
{
    QSqlQuery q(m_db);
    q.prepare("SELECT value FROM system_config WHERE key=?");
    q.addBindValue(key);
    if (q.exec() && q.next()) {
        return q.value(0).toString();
    }
    return defaultValue;
}

bool DbManager::setConfig(const QString &key, const QString &value)
{
    QSqlQuery q(m_db);
    q.prepare("INSERT OR REPLACE INTO system_config(key,value) VALUES(?,?)");
    q.addBindValue(key);
    q.addBindValue(value);
    if (!q.exec()) {
        m_lastError = q.lastError().text();
        return false;
    }
    return true;
}

// ---- 系统日志 ----

bool DbManager::insertLog(const QString &logType, const QString &username,
                           const QString &operation, const QString &detail)
{
    QSqlQuery q(m_db);
    q.prepare("INSERT INTO system_logs(log_time,log_type,username,operation,detail) VALUES(?,?,?,?,?)");
    q.addBindValue(QDateTime::currentDateTime().toString(Qt::ISODate));
    q.addBindValue(logType);
    q.addBindValue(username);
    q.addBindValue(operation);
    q.addBindValue(detail);
    return q.exec();
}

QList<SystemLog> DbManager::queryLogs(const QDateTime &startTime,
                                       const QDateTime &endTime,
                                       bool includeService,
                                       bool includeUI)
{
    QList<SystemLog> list;
    QString sql = "SELECT id,log_time,log_type,username,operation,detail FROM system_logs WHERE log_time BETWEEN ? AND ?";
    QStringList typeFilters;
    if (includeService) typeFilters << "'service'";
    if (includeUI) typeFilters << "'ui'";
    if (!typeFilters.isEmpty()) {
        sql += " AND log_type IN (" + typeFilters.join(",") + ")";
    }
    sql += " ORDER BY log_time DESC";

    QSqlQuery q(m_db);
    q.prepare(sql);
    q.addBindValue(startTime.toString(Qt::ISODate));
    q.addBindValue(endTime.toString(Qt::ISODate));
    if (!q.exec()) {
        m_lastError = q.lastError().text();
        return list;
    }
    while (q.next()) {
        SystemLog l;
        l.id = q.value(0).toInt();
        l.logTime = QDateTime::fromString(q.value(1).toString(), Qt::ISODate);
        l.logType = q.value(2).toString();
        l.username = q.value(3).toString();
        l.operation = q.value(4).toString();
        l.detail = q.value(5).toString();
        list.append(l);
    }
    return list;
}
