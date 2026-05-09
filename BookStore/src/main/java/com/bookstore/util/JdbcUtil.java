package com.bookstore.util;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Lab 8 JDBC 工具类（用于 JSP 直接获取 MySQL 连接）
 */
public final class JdbcUtil {

    private static final String DEFAULT_MYSQL_URL =
            "jdbc:mysql://localhost:3306/bookstore?useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Shanghai&useSSL=false&allowPublicKeyRetrieval=true";
    private static final String DEFAULT_MYSQL_USER = "root";
    private static final String DEFAULT_MYSQL_PASSWORD = "123456";

    private static final String DEFAULT_H2_URL =
            "jdbc:h2:mem:bookstoredb;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE";
    private static final String DEFAULT_H2_USER = "sa";
    private static final String DEFAULT_H2_PASSWORD = "";

    private static final Object INIT_LOCK = new Object();
    private static volatile boolean initialized = false;
    private static volatile DbConfig activeConfig;

    private JdbcUtil() {
    }

    static {
        loadDriver("com.mysql.cj.jdbc.Driver");
        loadDriver("org.h2.Driver");
    }

    public static Connection getConnection() throws SQLException {
        DbConfig config = activeConfig;
        if (config != null) {
            Connection conn = DriverManager.getConnection(config.url, config.username, config.password);
            initializeSchema(conn);
            return conn;
        }

        DbConfig resolved = resolveConfig();
        try {
            Connection conn = DriverManager.getConnection(resolved.url, resolved.username, resolved.password);
            activeConfig = resolved;
            initializeSchema(conn);
            return conn;
        } catch (SQLException ex) {
            if (!resolved.isH2()) {
                DbConfig fallback = defaultH2Config();
                Connection conn = DriverManager.getConnection(fallback.url, fallback.username, fallback.password);
                activeConfig = fallback;
                initializeSchema(conn);
                return conn;
            }
            throw ex;
        }
    }

    private static void initializeSchema(Connection conn) throws SQLException {
        if (initialized) {
            return;
        }
        synchronized (INIT_LOCK) {
            if (initialized) {
                return;
            }
            try (Statement stmt = conn.createStatement()) {
                stmt.execute("CREATE TABLE IF NOT EXISTS products (" +
                        "id INT AUTO_INCREMENT PRIMARY KEY," +
                        "name VARCHAR(40)," +
                        "price DOUBLE," +
                        "category VARCHAR(40)," +
                        "pnum INT," +
                        "imgurl VARCHAR(100)," +
                        "description VARCHAR(255)" +
                        ")");
                stmt.execute("CREATE TABLE IF NOT EXISTS `user` (" +
                        "id INT AUTO_INCREMENT PRIMARY KEY," +
                        "username VARCHAR(20) NOT NULL," +
                        "password VARCHAR(20) NOT NULL," +
                        "gender VARCHAR(255)," +
                        "email VARCHAR(50)," +
                        "telephone VARCHAR(255)," +
                        "introduce VARCHAR(100)," +
                        "role VARCHAR(10) DEFAULT '普通用户'," +
                        "registTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP" +
                        ")");
            }
            seedProducts(conn);
            initialized = true;
        }
    }

    private static void seedProducts(Connection conn) throws SQLException {
        int count = 0;
        try (PreparedStatement countStmt = conn.prepareStatement("SELECT COUNT(*) FROM products");
             ResultSet rs = countStmt.executeQuery()) {
            if (rs.next()) {
                count = rs.getInt(1);
            }
        }
        if (count > 0) {
            return;
        }
        String sql = "INSERT INTO products (name, price, category, pnum, imgurl, description) VALUES (?, ?, ?, ?, ?, ?)";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            addSampleProduct(stmt, "Java Web 开发实战", 59.00, "computer", 50,
                    "/static/images/productImg/0270eba2-2b48-48df-956b-0341204384d9.jpg",
                    "Servlet/JSP 实战项目入门");
            addSampleProduct(stmt, "Spring Boot 企业应用", 66.00, "computer", 40,
                    "/static/images/productImg/697a23d6-225a-41a3-8c20-7ab624265ecc.png",
                    "Spring Boot 企业级开发实践");
            addSampleProduct(stmt, "数据库系统原理", 72.00, "science", 35,
                    "/static/images/productImg/a2da626c-c72d-4972-83de-cf48405c5563.jpg",
                    "数据库核心概念与实践");
            addSampleProduct(stmt, "数据结构与算法", 68.00, "science", 28,
                    "/static/images/productImg/c4ab442f-95c7-4d6f-a57e-3eb7dc6b83c4.jpg",
                    "常用数据结构与算法解析");
            stmt.executeBatch();
        }
    }

    private static void addSampleProduct(PreparedStatement stmt, String name, double price, String category,
                                         int pnum, String imgUrl, String description) throws SQLException {
        stmt.setString(1, name);
        stmt.setDouble(2, price);
        stmt.setString(3, category);
        stmt.setInt(4, pnum);
        stmt.setString(5, imgUrl);
        stmt.setString(6, description);
        stmt.addBatch();
    }

    private static DbConfig resolveConfig() {
        String url = System.getenv("BOOKSTORE_DB_URL");
        String username = System.getenv("BOOKSTORE_DB_USERNAME");
        String password = System.getenv("BOOKSTORE_DB_PASSWORD");
        if (url != null && !url.trim().isEmpty()) {
            return new DbConfig(url.trim(),
                    username == null ? DEFAULT_MYSQL_USER : username,
                    password == null ? DEFAULT_MYSQL_PASSWORD : password);
        }
        return defaultH2Config();
    }

    private static DbConfig defaultH2Config() {
        return new DbConfig(DEFAULT_H2_URL, DEFAULT_H2_USER, DEFAULT_H2_PASSWORD);
    }

    private static void loadDriver(String className) {
        try {
            Class.forName(className);
        } catch (ClassNotFoundException e) {
            System.err.println("[JdbcUtil] JDBC Driver not found: " + className);
        }
    }

    private static final class DbConfig {
        private final String url;
        private final String username;
        private final String password;

        private DbConfig(String url, String username, String password) {
            this.url = url;
            this.username = username;
            this.password = password;
        }

        private boolean isH2() {
            return url != null && url.startsWith("jdbc:h2:");
        }
    }
}
