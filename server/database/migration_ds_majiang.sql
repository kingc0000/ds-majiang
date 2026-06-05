-- 砀山麻游数据库迁移
-- 添加密码字段（如果不存在）
ALTER TABLE user ADD COLUMN IF NOT EXISTS password VARCHAR(255) DEFAULT '';

-- 更新现有用户密码为随机值（避免空密码登录）
UPDATE user SET password = MD5(RAND()) WHERE password = '' OR password IS NULL;

-- 添加规则类型字段（用于区分不同麻将规则）
ALTER TABLE room ADD COLUMN IF NOT EXISTS rules_name VARCHAR(50) DEFAULT 'dsMajiang';

-- 添加局数字段
ALTER TABLE room ADD COLUMN IF NOT EXISTS chapter_max INT DEFAULT 8;

-- 更新现有房间默认规则为砀山麻游
UPDATE room SET rules_name = 'dsMajiang' WHERE rules_name IS NULL OR rules_name = '';
UPDATE room SET chapter_max = 8 WHERE chapter_max IS NULL OR chapter_max = 0;
