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
        self.key = self.import_key() or self.generate_key()
        self.fernet = Fernet(self.key)
        self.db_manager = self.create_db_conn()

    def import_key(self):   # 导入数据库密钥
        path = Path(constants.CONF_LOCATION, constants.FN_DB_KEY)
        if not path.exists() or not path.read_bytes():  # 文件不存在或文件为空
            log.debug("加载数据库密钥失败：数据库密钥不存在")
            return None
        else:
            log.debug("加载数据库密钥成功")
            return path.read_bytes()

    def generate_key(self):
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
    
    def __get_db_config(self):
        host = input("请输入主机地址：")
        user = input("请输入数据库管理员用户名：")
        password = getpass.getpass("请输入密码：")
        self.create_db_config(host, user, password)
        
        
    
    def load_db_config(self):
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
        
    def backup_db_conf(self):
        path_db_conf_key = Path(constants.CONF_LOCATION, constants.FN_DB_CONF_KEY)
        path_db_conf_yaml = Path(constants.CONF_LOCATION, constants.FN_DB_CONF_YAML)
        
        key_bak = Path(path_db_conf_key.parent, path_db_conf_key.name + ".bak" + "1")
        yaml_bak = Path(path_db_conf_yaml.parent, path_db_conf_yaml.name + ".bak" + "1")

        if key_bak.exists() or yaml_bak.exists():
            key_bak_str = str(key_bak)
            yaml_bak_str = str(yaml_bak)
            num = int(key_bak_str[-1]) + 1
            while True:
                key_bak_str = key_bak_str[:-1] + str(num)
                yaml_bak_str = yaml_bak_str[:-1] + str(num)
                if not Path(key_bak_str).exists() and not Path(yaml_bak_str).exists():
                    path_db_conf_key.rename(Path(key_bak_str))
                    log.debug("数据库配置文件密钥备份成功")
                    log.debug(Path(key_bak_str))
                    
                    path_db_conf_yaml.rename(Path(yaml_bak_str))
                    log.debug("数据库配置文件备份成功")
                    log.debug(Path(yaml_bak_str))
                    break
                num += 1
        else:
            path_db_conf_key.rename(key_bak)
            log.debug("数据库配置文件密钥备份成功")
            log.debug(key_bak)
            
            path_db_conf_yaml.rename(yaml_bak)
            log.debug("数据库配置文件备份成功")
            log.debug(yaml_bak)
            
        
    def create_db_conn(self):
        has_backup = False
        while True:
            if self.__check_config_legal():
                db_conf = self.load_db_config()
                log.debug("获取数据库配置信息成功")
                
                log.debug("正在尝试连接数据库...")
                db_manage = DatabaseManager(**db_conf)
                if db_manage.conn == None:
                    log.debug("连接数据库失败！")
                    
                    choose = None
                    while True:
                        choose = input("是否重新尝试(Y/n)：")
                        if choose in ["y", "Y", "n", "N"]:
                            break
                    
                    if choose in ["y", "Y"]:
                        log.debug("尝试重新连接数据库")
                        if has_backup == False:
                            # 备份 密钥
                            self.backup_db_conf()
                            has_backup = True
                        else:
                            # 删除之前创建、无法连接的配置文件（不包括 bak 文件）
                            Path(constants.CONF_LOCATION, constants.FN_DB_CONF_KEY).unlink()
                            Path(constants.CONF_LOCATION, constants.FN_DB_CONF_YAML).unlink()
                        continue
                    else:
                        log.debug("取消连接数据库")
                        log.debug("程序退出")
                        exit()
                else:
                    log.debug("成功连接数据库")
                    return db_manage
                        
            else:
                self.__get_db_config()