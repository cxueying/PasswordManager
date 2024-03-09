from manage.manage_psd_init import PasswordManagerInit
from logger.log import log

class PasswordManager(PasswordManagerInit):
    def __init__(self):
        super().__init__()

    def add_password(self, website, username, password):
        return self.db_manager.add_password(website, username, self.encrypt(password))
    
    def get_all_password(self):
        source_results = self.db_manager.get_all_password()
        results = []
        for source_result in source_results:
            result = {
                "website": source_result[0],
                "username": source_result[1],
                "password": self.decrypt(source_result[2])
            }
            if result["password"] == None:
                log.debug("解密密码失败")
                continue
            
            results.append(result)
        
        return results
    
    def delete_password(self, website, username):
        result = self.db_manager.get_password(website, username)
        if result == False or result == None:
            log.debug("查询不到信息")
            return False
        else:
            if self.decrypt(result[2]) == None:
                log.debug("删除密码失败：密钥无法解密密码")
                return False
        return self.db_manager.delete_password(website, username)