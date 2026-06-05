-- 砀山麻游数据库迁移脚本
-- 创建数据库和表

-- 创建数据库
CREATE DATABASE IF NOT EXISTS boss CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS mj CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE boss;

-- 用户表
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(64) NOT NULL DEFAULT '',
    `open_id` VARCHAR(128) DEFAULT NULL UNIQUE,
    `uuid` VARCHAR(128) NOT NULL UNIQUE,
    `avatar` VARCHAR(255) DEFAULT '',
    `sex` INT NOT NULL DEFAULT 2 COMMENT '0:女生,1:男生,2:未知',
    `create_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `update_date` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `version` INT NOT NULL DEFAULT 0,
    `gold` INT NOT NULL DEFAULT 0,
    `mobile` VARCHAR(20) DEFAULT NULL UNIQUE,
    `login_token` VARCHAR(128) DEFAULT NULL,
    `history_gold` INT NOT NULL DEFAULT 0,
    `level` INT NOT NULL DEFAULT 0 COMMENT '用户代理级别',
    `ip` VARCHAR(45) DEFAULT '',
    `longitude` DOUBLE DEFAULT 0,
    `latitude` DOUBLE DEFAULT 0,
    `password` VARCHAR(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 管理员表
CREATE TABLE IF NOT EXISTS `admin` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(64) NOT NULL DEFAULT '',
    `username` VARCHAR(64) NOT NULL UNIQUE,
    `password` VARCHAR(128) NOT NULL,
    `create_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `update_date` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `status` INT NOT NULL DEFAULT 1 COMMENT '0:禁用,1:启用'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 设置表
CREATE TABLE IF NOT EXISTS `setting` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `key_name` VARCHAR(128) NOT NULL UNIQUE,
    `value` TEXT,
    `create_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `update_date` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 房间表
CREATE TABLE IF NOT EXISTS `room` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `room_id` VARCHAR(32) NOT NULL UNIQUE,
    `creator_id` INT NOT NULL,
    `game_type` INT NOT NULL DEFAULT 1 COMMENT '游戏类型',
    `status` INT NOT NULL DEFAULT 1 COMMENT '1:进行中,2:已结束,3:已解散',
    `max_players` INT NOT NULL DEFAULT 4,
    `current_players` INT NOT NULL DEFAULT 0,
    `create_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `end_date` DATETIME DEFAULT NULL,
    `config` TEXT COMMENT '房间配置 JSON'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 房间用户表
CREATE TABLE IF NOT EXISTS `room_user` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `room_id` VARCHAR(32) NOT NULL,
    `user_id` INT NOT NULL,
    `seat` INT NOT NULL DEFAULT 0 COMMENT '座位号',
    `status` INT NOT NULL DEFAULT 1 COMMENT '1:准备,2:游戏中,3:已离开',
    `join_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `leave_date` DATETIME DEFAULT NULL,
    UNIQUE KEY `uk_room_user` (`room_id`, `user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 房间结果表
CREATE TABLE IF NOT EXISTS `room_result` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `room_id` VARCHAR(32) NOT NULL,
    `user_id` INT NOT NULL,
    `score` INT NOT NULL DEFAULT 0,
    `rank` INT NOT NULL DEFAULT 0,
    `create_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_room_id` (`room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户关联房间表
CREATE TABLE IF NOT EXISTS `user_link_room` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `room_id` VARCHAR(32) NOT NULL,
    `link_type` INT NOT NULL DEFAULT 1 COMMENT '1:创建,2:加入',
    `create_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_room_id` (`room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户登录日志表
CREATE TABLE IF NOT EXISTS `user_login_log` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `login_type` INT NOT NULL DEFAULT 1 COMMENT '1:密码,2:短信,3:微信',
    `ip` VARCHAR(45) DEFAULT '',
    `create_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_create_date` (`create_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户代理令牌表
CREATE TABLE IF NOT EXISTS `user_agent_token` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `token` VARCHAR(128) NOT NULL UNIQUE,
    `expire_date` DATETIME NOT NULL,
    `create_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 房间检查 ID 池表
CREATE TABLE IF NOT EXISTS `room_check_id_pool` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `check_id` VARCHAR(32) NOT NULL UNIQUE,
    `room_id` VARCHAR(32) DEFAULT NULL,
    `status` INT NOT NULL DEFAULT 1 COMMENT '1:可用,2:已使用',
    `create_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `use_date` DATETIME DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入默认管理员账号
INSERT INTO `admin` (`name`, `username`, `password`, `status`) VALUES 
    ('系统管理员', 'admin', 'e10adc3949ba59abbe56e057f20f883e', 1)
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`);

-- 插入默认设置
INSERT INTO `setting` (`key_name`, `value`) VALUES 
    ('game.majiang.type', 'ds_majiang'),
    ('game.majiang.name', '砀山麻游'),
    ('user.default.gold', '1000'),
    ('room.default.max_players', '4')
ON DUPLICATE KEY UPDATE `value` = VALUES(`value`);

-- 创建 mj 数据库的用户表（如果需要独立数据库）
USE mj;

CREATE TABLE IF NOT EXISTS `user` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(64) NOT NULL DEFAULT '',
    `open_id` VARCHAR(128) DEFAULT NULL UNIQUE,
    `uuid` VARCHAR(128) NOT NULL UNIQUE,
    `avatar` VARCHAR(255) DEFAULT '',
    `sex` INT NOT NULL DEFAULT 2,
    `create_date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `update_date` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `version` INT NOT NULL DEFAULT 0,
    `gold` INT NOT NULL DEFAULT 0,
    `mobile` VARCHAR(20) DEFAULT NULL UNIQUE,
    `login_token` VARCHAR(128) DEFAULT NULL,
    `history_gold` INT NOT NULL DEFAULT 0,
    `level` INT NOT NULL DEFAULT 0,
    `ip` VARCHAR(45) DEFAULT '',
    `longitude` DOUBLE DEFAULT 0,
    `latitude` DOUBLE DEFAULT 0,
    `password` VARCHAR(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
