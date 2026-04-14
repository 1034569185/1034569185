package com.bookstore.util;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * Lab 8 JDBC 工具类（用于 JSP 直接获取 MySQL 连接）
 */
public final class JdbcUtil {

    private static final String DEFAULT_URL =
            "jdbc:mysql://localhost:3306/bookstore?useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Shanghai&useSSL=false&allowPublicKeyRetrieval=true";
    private static final String DEFAULT_USER = "root";
    private static final String DEFAULT_PASSWORD = "123456";

    private JdbcUtil() {
    }

    static {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            throw new IllegalStateException("MySQL JDBC Driver not found", e);
        }
    }

    public static Connection getConnection() throws SQLException {
        String url = System.getenv().getOrDefault("BOOKSTORE_DB_URL", DEFAULT_URL);
        String username = System.getenv().getOrDefault("BOOKSTORE_DB_USERNAME", DEFAULT_USER);
        String password = System.getenv().getOrDefault("BOOKSTORE_DB_PASSWORD", DEFAULT_PASSWORD);
        return DriverManager.getConnection(url, username, password);
    }
}
