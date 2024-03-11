import mysql.connector
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
            
            log.error(e)
            
            return None

    def create_table(self):
        try:
            self.conn.cursor().execute("""
                CREATE TABLE IF NOT EXISTS passwords(
                    user VARCHAR(255) NOT NULL,
                    website VARCHAR(255) NOT NULL,
                    account VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    PRIMARY KEY(user, website, account)
                )
            """)
            
            log.debug("创建表成功：passwords")
            
            self.conn.cursor().execute("""
                CREATE TABLE IF NOT EXISTS users(
                    user VARCHAR(255) NOT NULL PRIMARY KEY,
                    salt BLOB NOT NULL,
                    password BLOB NOT NULL,
                    login CHAR(1) NOT NULL
                )
            """)
            
            log.debug("创建表成功：users")
            
        except mysql.connector.Error as e:
            
            log.error(e)
    
    def close_connection(self):
        self.conn.close()
        
        log.info("数据库断开连接")


#===================================================================================================================#
#===================================================================================================================#
#===================================================================================================================#
#===================================================================================================================#

    def add_password(self, website, account, password):
        try:
            user = self.get_user_login()
            if user == None:
                return False
            sql = "INSERT INTO passwords (user, website, account, password) VALUES(%s, %s, %s, %s)"
            self.conn.cursor().execute(sql, (user, website, account, password))
            self.conn.commit()
            
            log.debug("成功添加密码")
            
            return True
        except mysql.connector.Error as e:
            log.error(e)
            
            return False

    def get_all_password(self):
        try:
            user = self.get_user_login()
            if user == None:
                return False
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT * FROM passwords WHERE user = %s",
                (user, )
            )
            return cursor.fetchall()
        except mysql.connector.Error as e:
            
            log.error(e)
            return False

    def get_password(self, website, account):
        try:
            user = self.get_user_login()
            if user == None:
                return False
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT * FROM passwords WHERE user = %s and website = %s and account = %s",
                (user, website, account)
            )
            return cursor.fetchone()
        except mysql.connector.Error as e:
            
            log.error(e)
            return False

    def delete_password(self, website, account):
        try:
            user = self.get_user_login()
            if user == None:
                return False
            cursor = self.conn.cursor()
            cursor.execute(
                "DELETE FROM passwords WHERE user = %s and website = %s and account = %s",
                (user, website, account)
            )
            self.conn.commit()
            if cursor.rowcount != 0:
                log.debug("删除密码成功")
                return True
            else:
                log.debug("删除密码失败")
                return False
        except mysql.connector.Error as e:
            log.error(e)
            return False
        
    def add_user(self, user, salt, password):
        try:
            self.conn.cursor().execute(
                "INSERT INTO users (user, salt, password, login) VALUES (%s, %s, %s, %s)",
                (user, salt, password, "F")
            )
            self.conn.commit()
            
            return True
        except mysql.connector.Error as e:
            log.error(e)
            return False

    def get_user_password(self, user):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user = %s", (user, ))
            
            return cursor.fetchone()
        except mysql.connector.Error as e:
            log.error(e)
            
    def user_login(self, user):
        try:
            result = self.get_user_login()
            if result != None:
                self.conn.cursor().execute("UPDATE users SET login = 'F' WHERE user = %s", (result, ))
            self.conn.cursor().execute("UPDATE users SET login = 'T' WHERE user = %s", (user, ))
            self.conn.commit()
            
        except mysql.connector.Error as e:
            log.error(e)
        
    def get_user_login(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT user FROM users WHERE login = 'T'")
            result = cursor.fetchone()
            if result == None:
                return None
            else: 
                return result[0]
        except mysql.connector.Error as e:
            log.error(e)

    def has_admin(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT user FROM users WHERE user = %s", ('admin', ))
            results = cursor.fetchone()
            if results == None:
                return False
            else:
                return True
        except mysql.connector.Error as e:
            log.error(e)
            