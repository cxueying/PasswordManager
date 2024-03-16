from logger.log import log
from DB.init import DBInit
import mysql.connector

class DBUsers:
    """数据库表 users 的操作
    """
    
    def __init__(self) -> None:
        """初始化

        Args:
            conn (_type_): 数据库连接
        """
        db_init = DBInit()
        self.conn = db_init.get_conn()
        
    
    def add(self, user: str, salt: bytes, password: bytes) -> bool:
        """添加用户

        Args:
            user (str): 用户
            salt (bytes): 盐值
            password (bytes): 密码

        Returns:
            bool: True：添加成功， False：添加失败
        """
        
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
        
        
    def get_psd(self, user: str) -> list:
        """获取盐值和密码

        Args:
            user (str): 用户

        Returns:
            list: 包含盐值和密码的列表，空列表表示未查询到数据
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT salt, password FROM users WHERE user = %s",
                (user, )
            )
            return cursor.fetchone()
        except mysql.connector.Error as e:
            log.error(e)
            return []
        
    
    def set_login(self, user) -> bool:
        """设置登录标志

        Args:
            user (_type_): 登录的用户

        Returns:
            bool: True：成功， False：失败
        """
        
        try:
            result = self.get_login()
            if result != None:
                self.conn.cursor().execute("UPDATE users SET login = 'F' WHERE user = %s", (result, ))
            self.conn.cursor().execute("UPDATE users SET login = 'T' WHERE user = %s", (user, ))
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            log.error(e)
            return False
        
    
    def get_login(self) -> str:
        """获取登录标志为 T 的用户

        Returns:
            str: 
                None：没有标志为 T 的用户
                Other： 标志为 T 用户
        """
        
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
            return None
        
    
    def has_admin(self) -> bool:
        """是否存在管理员账号

        Returns:
            bool: 
                True: 存在
                False: 不存在 
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT user FROM users WHERE user = %s", ('admin', ))
            result = cursor.fetchone()
            if result == None:
                return False
            else:
                return True
        except mysql.connector.Error as e:
            log.error(e)
            return False