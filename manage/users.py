from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from DB.users import DBUsers
from logger.log import log
import os


class UsersManage:
    """表users的使用
    """
    
    def __init__(self):
        self.db_user = DBUsers()
        self.__add_admin()
    
    
    def __add_admin(self):
        """添加管理员账号
        """
        
        if self.db_user.has_admin():
            log.debug("管理员账号已存在")
            return
        else:
            self.add("admin", "admin")
            log.debug("添加管理员账户成功")
    
    
    def add(self, user: str, password: str):
        """添加用户

        Args:
            user (str): 用户
            password (str): 密码

        Returns:
            True：添加成功
            False：添加失败
        """

        salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        
        hashed_password = kdf.derive(password.encode())
        
        if self.db_user.add(user, salt, hashed_password):
            log.info("添加账号成功")
            return True
        else:
            log.info("添加账户失败")
            return False
        
    
    def login(self, user: str, password: str):
        """登录

        Args:
            user (str): 用户
            password (str): 密码

        Returns:
            True：登录成功
            False：登录失败
        """
        
        
        result = self.db_user.get_psd(user)
        if result == None:
            log.info("登录失败")
            return False
        else:
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=result[0],
                iterations=100000,
                backend=default_backend()
            )
            
            hashed_password = result[1]
            try:
                kdf.verify(password.encode(), hashed_password)
                log.info("密码验证通过")
                return True
            except Exception as e:
                log.info("密码验证失败")
                log.debug(e)
                return False
    
    
    def get_login(self):
        """获取登录状态为 T 的用户

        Returns:
            str: 用户
            None：无
        """
        
        return self.db_user.get_login()
    
    
    def set_login(self, user: str):
        """将user的登录状态设置为 T 

        Args:
            user (str): 用户

        Returns:
            True：设置成功
            False：设置失败
        """
        return self.db_user.set_login(user)
    
    
    def change_psd(self, user: str, old_password: str, new_password: str) -> bool:
        """修改用户密码

        Args:
            user (str): 用户
            old_password (str): 旧密码
            new_password (str): 新密码

        Returns:
            True：成功
            False：失败
        """
        
        if self.login(user, old_password) == True: # 验证通过
            salt = os.urandom(16)
        
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            
            hashed_password = kdf.derive(new_password.encode())
            
            return self.db_user.change_psd(user, salt, hashed_password)
        
        else:
            return False
        