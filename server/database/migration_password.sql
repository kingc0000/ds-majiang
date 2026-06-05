-- 砀山麻游数据库迁移
-- 添加密码字段（如果不存在）
ALTER TABLE user ADD COLUMN IF NOT EXISTS password VARCHAR(255) DEFAULT '';

-- 更新现有用户密码为随机值
UPDATE user SET password = MD5(RAND()) WHERE password = '' OR password IS NULL;
