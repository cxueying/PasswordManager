import mysql.connector
from mysql.connector import errorcode
from DB.init import DBInit
from logger.log import log

class DBPasswords:
    """数据库表 passwords 的操作
    """
    
    def __init__(self):
        """表passwords 操作初始化

        Args:
            conn: 数据库连接
        """
        db_init = DBInit()
        self.conn = db_init.get_conn()
       
     
    def add(self, user: str, website: str, account: str, password: str) -> bool:
        """添加数据

        Args:
            user (str): 用户
            website (str): 网站
            account (str): 账号
            password (str): 密码

        Returns:
            bool: 添加成功返回 True，添加失败返回 False
        """
        
        try:
            self.conn.cursor().execute(
                "INSERT INTO passwords (user, website, account, password) VALUES(%s, %s, %s, %s)",
                (user, website, account, password)
            )
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            log.error(e)
            if e.errno == errorcode.ER_DUP_ENTRY:
                return 1062
            
            return False
    
        
    def get(self, user: str) -> list:
        """获取所有的数据

        Args:
            user (str): 用户

        Returns:
            list: (website, account, password)
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT website, account, password FROM passwords WHERE user = %s",
                (user, )
            )
            return cursor.fetchall()
        except mysql.connector.Error as e:
            log.error(e)
            return []
    
    
    def delete(self, user: str, website: str, account: str) -> bool:
        """删除数据

        Args:
            user (str): 用户
            website (str): 网站
            account (str): 账号

        Returns:
            bool: True：删除成功，False：删除失败
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "DELETE FROM passwords WHERE user = %s and website = %s and account = %s",
                (user, website, account)
            )
            self.conn.commit()
            
            if cursor.rowcount != 0:
                return True
            else:
                return False
        except mysql.connector.Error as e:
            log.error(e)
            return False
    
        
    def exist(self, user: str, website: str, account: str) -> bool:
        """判断数据库中是否存在相关数据

        Args:
            user(str): 用户
            website (str): 网站
            account (str): 账号

        Returns:
            bool: True: 存在， False: 不存在
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT * FROM passwords WHERE user = %s and website = %s and account = %s",
                (user, website, account)
            )
            result = cursor.fetchone()
            if result == None:
                return False
            else:
                return True
        except mysql.connector.Error as e:
            log.error(e)
            return False


    def update(self, user: str, **kwargs) -> bool:
        """更新信息

        Args:
            user (str): 用户

        Returns:
            True：成功
            False：数据库异常
            1062：信息已存在
        """
        
        try:
            self.conn.cursor().execute(
                "UPDATE passwords SET website = %s, account = %s, password = %s WHERE user = %s and website = %s and account = %s",
                (kwargs["new_website"], kwargs["new_account"], kwargs["new_password"], user, kwargs["website"], kwargs["account"])
            )
            self.conn.commit()
            return True
        
        except mysql.connector.Error as e:
            log.error(e)
            if e.errno == errorcode.ER_DUP_ENTRY:
                return 1062
            
            return False