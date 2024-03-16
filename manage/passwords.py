from cryptography.fernet import Fernet
from DB.passwords import DBPasswords
from logger.log import log
from pathlib import Path


class PSDManager:
    """表passwords的使用
    """

    def __init__(self):
        self.DB_KEY = r".\assets\config\database.key"
        self.__key = self.__import_key() or self.__generate_key()
        self.__ferent = Fernet(self.__key)
        
        self.db_psd = DBPasswords()
    
    
    def __import_key(self):
        """导入数据库密钥

        Returns:
            bytes: 密钥
            None: 密钥不存在
        """
        
        path = Path(self.DB_KEY)
        if not path.exists() or not path.read_bytes():  # 文件不存在或文件为空
            log.debug("加载数据库密钥失败：数据库密钥不存在")
            return None
        
        else:
            log.debug("加载数据库密钥成功")
            return path.read_bytes()


    def __generate_key(self):
        """创建数据库密钥，并写入到指定位置

        Returns:
            key: 新创建的密钥
        """
        
        key = Fernet.generate_key()
       
            
        path = Path(self.DB_KEY)
        path.write_bytes(key)
        log.debug(f"创建密钥成功：{path}")
        return key
    
    
    def encrypt(self, message: str):
        """加密数据

        Args:
            message (str): 要加密的数据

        Returns:
            None: 异常
            Other： 加密结果
        """
        
        return self.__ferent.encrypt(message.encode()).decode()


    def decrypt(self, encrypted_message: str):
        """解密数据

        Args:
            encrypted_message (str): 要解密的数据

        Returns:
            None: 解密失败
            Other：解密后的数据
        """
        
        try:
            return self.__ferent.decrypt(encrypted_message.encode()).decode()
        except:
            log.warning("解密失败")
            return None
        
    
    def add(self, user: str, website: str, account: str, password: str):
        """添加新的密码

        Args:
            user (str): 用户
            website (str): 网站
            account (str): 账号
            password (str): 密码

        Returns:
            False：添加失败
            True：添加成功
        """
        
        return self.db_psd.add(user, website, account, self.encrypt(password))

        
    
    def get(self, user: str):
        """获取所有账号信息
        
        Argv:
            user(str): 用户

        Returns:
            list：账号信息
            None：查询失败
        """

        try:
            source_results = self.db_psd.get(user)
        except:
            return None
        
        results = []
        for source_result in source_results:
            result = {
                "website": source_result[0],
                "account": source_result[1],
                "password": source_result[2]
            }
            if self.decrypt(source_result[2]) == None:
                log.debug("解密用户密码失败")
                continue
            
            results.append(result)
        
        return results
    
    
    def delete(self, user: str, website: str, account: str):
        """删除账号信息

        Args:
            user (str): 用户
            website (str): 网站
            account (str): 账号

        Returns:
            True：删除成功
            False：删除失败
        """
        
        exist = self.db_psd.exist(user, website, account)
        if exist == False:
            log.debug("查询不到信息")
            return False
        else:
            return self.db_psd.delete(user, website, account)