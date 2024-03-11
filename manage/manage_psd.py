from manage.manage_psd_init import PasswordManagerInit
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import base64
from logger.log import log

class PasswordManager(PasswordManagerInit):
    def __init__(self):
        super().__init__()

    def add_password(self, website, account, password):
        if self.connected:
            return self.db_manager.add_password(website, account, self.encrypt(password))
        else:
            return False
    
    def get_all_password(self):
        if not self.connected:
            return None
        try:
            source_results = self.db_manager.get_all_password()
        except:
            return None
        results = []
        for source_result in source_results:
            result = {
                "website": source_result[1],
                "account": source_result[2],
                "password": source_result[3]
            }
            if self.decrypt(source_result[3]) == None:
                log.debug("解密用户密码失败")
                continue
            
            results.append(result)
        
        return results
    
    def delete_password(self, website, account):
        if not self.connected:
            return False
        
        result = self.db_manager.get_password(website, account)
        if result == False or result == None:
            log.debug("查询不到信息")
            return False
        else:
            if self.decrypt(result[2]) == None:
                log.debug("删除密码失败：密钥无法解密密码")
                return False
        return self.db_manager.delete_password(website, account)
    
    def add_user(self, user, password):
        if not self.connected:
            log.info("数据库为连接，添加用户失败")
            return False

        salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        
        hashed_password = kdf.derive(password.encode())
        
        if self.db_manager.add_user(user, salt, hashed_password):
            log.info("添加账号成功")
        else:
            log.info("添加账户失败")
        return True
        
    def login(self, user, password):
        result = self.db_manager.get_user_password(user)
        if result == None:
            log.info("登录失败")
            return False
        else:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=result[1],
                iterations=100000,
                backend=default_backend()
            )
            
            hashed_password = result[2]
            try:
                kdf.verify(password.encode(), hashed_password)
                log.info("密码验证通过")
                return True
            except Exception as e:
                log.info("密码验证失败")
                log.debug(e)
                return False
    
    def get_user_login(self):
        return self.db_manager.get_user_login()
    
    def user_login(self, user):
        return self.db_manager.user_login(user)

manage = PasswordManager()