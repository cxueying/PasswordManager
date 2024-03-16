# 创建用户
# 修改 username 和 password
CREATE USER "username"@"localhost" IDENTIFIED BY "password";

# 创建数据库 
CREATE DATABASE IF NOT EXISTS password_manager;

# 授予权限
# 修改 username 
GRANT ALL PRIVILEGES ON password_manager.* TO "username"@"localhost";

# 刷新权限
FLUSH PRIVILEGES;