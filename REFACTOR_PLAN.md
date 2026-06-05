# 砀山麻游改造计划

## 项目名称
- 麻将名称：砀山麻游
- 项目名：ds-majiang

## 核心规则改造

### 1. 牌池改造 (120张) ✅
- 筒子：1-9 各4张 = 36张
- 条子：1-9 各4张 = 36张
- 万子：1-9 各4张 = 36张
- 花牌（中发白）：各4张 = 12张
- **总计：120张**

### 2. 规则修改 ✅
- ✅ 不能吃牌
- ✅ 只能碰、杠、胡
- ✅ 碰牌后可再杠
- ✅ 所有杠牌吃三家（赢家除外）
- ✅ 明杠（含碰后杠）1分
- ✅ 暗杠2分
- ✅ 胡牌3分
- ✅ 七对翻倍（不可胡花牌除非自摸，不可胡已有对牌，胡七对需明牌其他六对）
- ✅ 可截胡，可胡碰后杠

### 3. 用户系统 ✅
- 手机号注册 + 密码设置
- 支持 PASSWORD 登录类型

### 4. 局数选择 ✅
- 每场可选：8局、12局、16局、24局
- 按场计分

### 5. 结算展示 ✅
- 每场结束统计积分
- 生成可复制文本

### 6. 部署 ✅
- 通过 nginx 暴露对外服务

## 已完成改造

### 核心规则文件
1. ✅ `server/project/mj-data/src/main/java/mj/data/PaiType.java` - 添加 HUAPAI 花牌类型
2. ✅ `server/project/mj-data/src/main/java/mj/data/Pai.java` - 中发白改为 HUAPAI 花牌类型
3. ✅ `server/project/mj-scene/src/main/java/game/scene/room/majiang/rules/DsMajiangRules.java` - 新建砀山麻游规则类
4. ✅ `server/project/mj-scene/src/main/java/game/scene/room/majiang/rules/Rules.java` - 添加砀山麻游规则选择
5. ✅ `server/project/mj-scene/src/main/java/game/scene/room/majiang/ComputeFan.java` - 修改番数计算

### 用户系统
6. ✅ `server/project/mj-boss/src/main/java/game/boss/services/UserService.java` - 添加 PASSWORD 登录类型
7. ✅ `server/project/mj-data/src/main/java/mj/net/message/login/Login.java` - 添加 password 字段

### 配置和结算
8. ✅ `server/project/mj-data/src/main/java/mj/data/Config.java` - 添加局数配置常量
9. ✅ `server/project/mj-data/src/main/java/mj/data/DsMajiangSummary.java` - 场结算汇总类
10. ✅ `server/database/migration_ds_majiang.sql` - 数据库迁移 SQL
11. ✅ `server/nginx/ds-majiang.conf` - Nginx 配置

## 部署步骤

1. 编译 Java 代码：`mvn clean package -DskipTests`
2. 执行数据库迁移：`mysql -u root -p < server/database/migration_ds_majiang.sql`
3. 部署服务：将编译产物部署到服务器
4. 配置 Nginx：`cp server/nginx/ds-majiang.conf /etc/nginx/conf.d/ && nginx -t && nginx -s reload`
5. 启动服务

## 注意事项
- 保持原有框架结构不变
- 新增规则类继承 Rules 抽象类
- 通过配置区分不同麻将类型
- 密码加密存储（建议使用 BCrypt）
