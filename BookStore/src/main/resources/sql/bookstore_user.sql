-- 实验八：bookstore.user 表初始化脚本（可复用）
-- 使用方式：
-- mysql -u root -p < bookstore_user.sql

CREATE DATABASE IF NOT EXISTS `bookstore`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_general_ci;

USE `bookstore`;

CREATE TABLE IF NOT EXISTS `user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(20) NOT NULL,
  `password` VARCHAR(20) NOT NULL,
  `gender` VARCHAR(255) DEFAULT NULL,
  `email` VARCHAR(50) DEFAULT NULL,
  `telephone` VARCHAR(255) DEFAULT NULL,
  `introduce` VARCHAR(100) DEFAULT NULL,
  `role` VARCHAR(10) DEFAULT '普通用户',
  `registTime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
