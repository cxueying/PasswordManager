from manage.manage_psd import manage
from logger.log import log
import mysql.connector
# 用于升级 v2.2 版本以后的数据库
class DBUpdate():
    def __init__(self):
        self.conn = manage.db_manager.conn
        self.alter_table()
        
    def alter_table(self):
        try:
            sql = f"ALTER TABLE passwords RENAME COLUMN username TO account"
            self.conn.cursor().execute(sql)
            log.debug("成功修改列名")
            
            sql = f"ALTER TABLE passwords ADD COLUMN user VARCHAR(255) NOT NULL FIRST"
            self.conn.cursor().execute(sql)
            log.debug("成功添加新的列")
            
            sql = f"UPDATE passwords set user = 'admin'"
            self.conn.cursor().execute(sql)
            log.debug("成功添加数据")
            
            sql = f"ALTER TABLE passwords DROP PRIMARY KEY"
            self.conn.cursor().execute(sql)
            log.debug("成功移除主键")
            
            sql = f"ALTER TABLE passwords ADD PRIMARY KEY (user, website, account)"
            self.conn.cursor().execute(sql)
            log.debug("成功设置主键")
            
        except mysql.connector.Error as e:
            print(e)
        

if __name__ == "__main__":
    DBUpdate()