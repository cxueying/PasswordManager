import mysql.connector
from config import constants
from logger.log import log

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.conn = self.create_connection(host, user, password, database)
        if self.conn != None:
            self.create_table()

    def create_connection(self, host, user, password, database):
        conn = None;
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            conn.database = database
            
            log.debug("数据库连接成功")
            
            return conn
        except mysql.connector.Error as e:
            
            log.debug(f"数据库连接失败")
            log.debug(e)
            
            return None

    def create_table(self):
        try:
            self.conn.cursor().execute("""
                CREATE TABLE IF NOT EXISTS {}(
                    website VARCHAR(255) NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    PRIMARY KEY(website, username)
                )
            """.format(constants.TABLE_PASSWORD))
            
            log.debug(f"创建表成功：{constants.TABLE_PASSWORD}")
            
        except mysql.connector.Error as e:
            
            log.debug(f"创建表失败：{constants.TABLE_PASSWORD}")
            log.debug(e)

    def close_connection(self):
        self.conn.close()
        
        log.debug("数据库断开连接")


#===================================================================================================================#
#===================================================================================================================#
#===================================================================================================================#
#===================================================================================================================#

    def add_password(self, website, username, password):
        try:
            sql = "INSERT INTO {} (website, username, password) VALUES(%s, %s, %s)".format(constants.TABLE_PASSWORD)
            self.conn.cursor().execute(sql, (website, username, password))
            self.conn.commit()
            
            log.debug("成功添加密码")
            
            return True
        except mysql.connector.Error as e:
            log.debug("添加密码失败")
            log.debug(e)
            
            return False

    def get_all_password(self):
        try:
            sql = "SELECT * FROM {}".format(constants.TABLE_PASSWORD)
            cursor = self.conn.cursor()
            cursor.execute(sql)
            
            log.debug("查询所有密码成功")
            
            return cursor.fetchall()
        except mysql.connector.Error as e:
            
            log.debug("查询所有密码失败")
            log.debug(e)
            return False

    def get_password(self, website, username):
        try:
            sql = "SELECT * FROM {} where website = %s and username = %s".format(constants.TABLE_PASSWORD)
            cursor = self.conn.cursor()
            cursor.execute(sql, (website, username))
            return cursor.fetchone()
        except mysql.connector.Error as e:
            
            log.debug("查询密码失败")
            log.debug(e)
            return False

    def delete_password(self, website, username):
        try:
            sql = "DELETE FROM {} WHERE website=%s AND username=%s".format(constants.TABLE_PASSWORD)
            cursor = self.conn.cursor()
            cursor.execute(sql, (website, username))
            self.conn.commit()
            if cursor.rowcount != 0:
                log.debug("删除密码成功")
                return True
            else:
                log.debug("删除密码失败")
                return False
        except mysql.connector.Error as e:
            log.debug("删除密码失败")
            log.debug(e)
            return False

