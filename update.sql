# 选择数据库
USE password_manager;

# 修改表passwords信息

ALTER TABLE passwords RENAME COLUMN username TO account;

ALTER TABLE passwords ADD COLUMN user VARCHAR(255) NOT NULL FIRST;

# 禁用安全模式
SET SQL_SAFE_UPDATES = 0;

UPDATE passwords set user = 'admin';

# 开启安全模式
SET SQL_SAFE_UPDATES = 1;

ALTER TABLE passwords DROP PRIMARY KEY;

ALTER TABLE passwords ADD PRIMARY KEY (user, website, account);