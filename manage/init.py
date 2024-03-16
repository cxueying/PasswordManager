
from logger.log import log
from DB.init import DBInit


class ManageInit:
    """管理器初始化, 连接数据库
    """
    
    def __init__(self):
        
        
        
        
        self.connected = False
        self.db_init = self.create_conn()
        if self.db_init == False:
            self.conn = None
        else:
            self.conn = self.db_init.conn
        
    
    
        
    
    
    
    
    def get_conf(self) -> dict:
        """获取数据库连接配置信息：主机地址、用户

        Returns:
            dict: 包含主机地址和用户的字典
        """
        
        if not self.__check_config_legal():
            return None
        result = self.__load_config()
        return {
            "host": result["host"],
            "user": result["user"]
        }
        
    
    def update_db_init(self):
        """更新数据库连接信息
        """
        
        self.db_init = self.create_conn()
        if self.db_init == None or self.db_init == False:
            return False
        self.conn = self.db_init.conn
        
