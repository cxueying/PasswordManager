import yaml
import base64
import getpass
from pathlib import Path
from cryptography.fernet import Fernet
from db.db_manage import DatabaseManager
from config import constants
from logger.log import log

class PasswordManagerInit:
    def __init__(self):
        self.key = self.__import_key() or self.__generate_key()
        self.fernet = Fernet(self.key)
        self.connected = False
        self.db_manager = self.create_db_conn()

    def __import_key(self):   # 导入数据库密钥
        path = Path(constants.CONF_LOCATION, constants.FN_DB_KEY)
        if not path.exists() or not path.read_bytes():  # 文件不存在或文件为空
            log.debug("加载数据库密钥失败：数据库密钥不存在")
            return None
        else:
            log.debug("加载数据库密钥成功")
            return path.read_bytes()

    def __generate_key(self):
        key = Fernet.generate_key()
        # 确保config目录存在 
        if not Path(constants.CONF_LOCATION).exists():
            log.debug(f"目录 {Path(constants.CONF_LOCATION).name} 不存在")
            Path(constants.CONF_LOCATION).mkdir()
            log.debug(f"成功创建目录：{Path(constants.CONF_LOCATION).name}")
            
        path = Path(constants.CONF_LOCATION, constants.FN_DB_KEY)
        path.write_bytes(key)
        log.debug(f"创建密钥成功：{path}")
        return key

    def encrypt(self, message):
        return self.fernet.encrypt(message.encode()).decode()

    def decrypt(self, encrypted_message):
        try:
            return self.fernet.decrypt(encrypted_message.encode()).decode()
        except:
            return None
  
    # 检查 config 下的数据库配置文件是否合法
    # db_conf.key  db_conf.yaml
    def __check_config_legal(self):
        path_db_conf_yaml = Path(constants.CONF_LOCATION, constants.FN_DB_CONF_YAML)
        path_db_conf_key = Path(constants.CONF_LOCATION, constants.FN_DB_CONF_KEY)
        
        # 文件缺失
        if not path_db_conf_key.exists() or not path_db_conf_yaml.exists():
            log.debug("数据库配置文件缺失")
            return False
        
        # 文件为空
        if not path_db_conf_key.read_bytes() or not path_db_conf_yaml.read_text():
            log.debug("数据库配置文件为空")
            return False
        
        # key是否合法
        decode_key = None
        try:
            decode_key = base64.urlsafe_b64decode(path_db_conf_key.read_bytes())
        except:
            log.debug("数据库配置文件密钥无法解密")
            return False
        else:
            if len(decode_key) != 32:
                log.debug("数据库配置文件密钥非法")
                return False
        
        # yaml 配置文件是否合法
        db_conf_set = ("host", "user", "password", "database")
        with open(path_db_conf_yaml, 'r') as f:
            conf_dict = yaml.safe_load(f)
            conf_set = (conf_dict.keys())
            # 参数不相同
            if conf_set - db_conf_set != db_conf_set - conf_set:
                log.debug("数据库配置文件参数非法")
                return False
            
            # 尝试解密
            check_fernet = Fernet(path_db_conf_key.read_bytes())
            try:
                check_fernet.decrypt(conf_dict["host"].encode()).decode()
                check_fernet.decrypt(conf_dict["user"].encode()).decode()
                check_fernet.decrypt(conf_dict["password"].encode()).decode()
                check_fernet.decrypt(conf_dict["database"].encode()).decode()
                log.debug("数据库配置文件解密成功")
            except:
                log.debug("数据库配置文件解密失败")
                return False
        
        log.debug("数据库配置文件及密钥合法")
        return True
    
    def __load_db_config(self):
        path_db_conf_yaml = Path(constants.CONF_LOCATION, constants.FN_DB_CONF_YAML)
        path_db_conf_key = Path(constants.CONF_LOCATION, constants.FN_DB_CONF_KEY)
        
        load_fernet = Fernet(path_db_conf_key.read_bytes())
        conf_dict = yaml.safe_load(path_db_conf_yaml.read_text())
        
        return {
            "host": load_fernet.decrypt(conf_dict["host"].encode()).decode(),
            "user": load_fernet.decrypt(conf_dict["user"].encode()).decode(),
            "password": load_fernet.decrypt(conf_dict["password"].encode()).decode(),
            "database": load_fernet.decrypt(conf_dict["database"].encode()).decode(),
        }

    def create_db_config(self, host, user, password, database=constants.DB_NAME):
        # 创建密钥并导出
        db_conf_key = Fernet.generate_key()
        path_db_conf_key = Path(constants.CONF_LOCATION, constants.FN_DB_CONF_KEY)
        path_db_conf_key.write_bytes(db_conf_key)
        log.debug("数据库配置文件密钥创建成功")
        log.debug(path_db_conf_key)
        
        db_conf_fernet = Fernet(db_conf_key)
        
        path_db_conf_yaml = Path(constants.CONF_LOCATION, constants.FN_DB_CONF_YAML)
        path_db_conf_yaml.write_text(
            f'host: "{db_conf_fernet.encrypt(host.encode()).decode()}"\n' +
            f'user: "{db_conf_fernet.encrypt(user.encode()).decode()}"\n' +
            f'password: "{db_conf_fernet.encrypt(password.encode()).decode()}"\n' +
            f'database: "{db_conf_fernet.encrypt(database.encode()).decode()}"\n'
        )
        
        log.debug("数据库配置文件创建成功")
        log.debug(path_db_conf_yaml)
            
        
    def create_db_conn(self):
        if self.__check_config_legal():
            db_conf = self.__load_db_config()
            log.debug("获取数据库配置信息成功")
            
            log.debug("正在尝试连接数据库...")
            db_manage = DatabaseManager(**db_conf)
            if db_manage.conn == None:
                log.debug("连接数据库失败！")
                self.connected = False
                return False
            else:
                log.debug("成功连接数据库")
                self.connected = True
                return db_manage
        return None
                
    def get_db_conf(self):
        if not self.__check_config_legal():
            return None
        result = self.__load_db_config()
        return {
            "host": result["host"],
            "user": result["user"]
        }
        
    def update_db_manage(self):
        self.db_manager = self.create_db_conn()
        
    def is_db_connected(self):
        return self.connected