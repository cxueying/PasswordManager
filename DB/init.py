from cryptography.fernet import Fernet
from logger.log import log
from pathlib import Path
import mysql.connector
import base64
import yaml

class DBInit:
    """数据库初始化、连接
    """
    
    def __init__(self):
        """数据库初始化
        """
        
        self.__DB_CONF_KEY = r".\assets\config\db_conf.key"
        self.__DB_CONF = r".\assets\config\db_conf.yaml"
        self.__CONF_PATH = r".\assets\config"
        
        
        self.__conn = self.__create_conn()
        if self.__conn != None:
            self.__create_table()

    
    def __check_config_legal(self) -> bool:
        """检查数据库配置文件是否合法

        Returns:
            bool: True: 合法， False：不合法
        """
        
        path_db_conf_yaml = Path(self.__DB_CONF)
        path_db_conf_key = Path(self.__DB_CONF_KEY)
        
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
    
    
    def __load_config(self) -> dict:
        """加载数据库配置信息

        Returns:
            dict: 数据库配置信息
        """
        
        path_db_conf_yaml = Path(self.__DB_CONF)
        path_db_conf_key = Path(self.__DB_CONF_KEY)
        
        load_fernet = Fernet(path_db_conf_key.read_bytes())
        conf_dict = yaml.safe_load(path_db_conf_yaml.read_text())
        
        return {
            "host": load_fernet.decrypt(conf_dict["host"].encode()).decode(),
            "user": load_fernet.decrypt(conf_dict["user"].encode()).decode(),
            "password": load_fernet.decrypt(conf_dict["password"].encode()).decode(),
            "database": load_fernet.decrypt(conf_dict["database"].encode()).decode(),
        }
    
        
    def __connection(self, host: str, user: str, password: str, database: str):
        """连接数据库

        Args:
            host (str): 数据库主机地址
            user (str): 数据库用户
            password (str): 数据库用户密码
            database (str): 数据库名称

        Returns:
            None: 连接失败
            Other: 连接成功
        """
        
        conn = None;
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(database))
            conn.database = database
            return conn
        except mysql.connector.Error as e:
            log.error(e)
            return None
    
    
    def create_config(self, host: str, user: str, password: str, database: str = "password_manager_dev"):
        """创建数据库配置文件并导出
        """
        
         # 确保config目录存在 
        if not Path(self.__CONF_PATH).exists():
            log.debug(f"目录 {Path(self.__CONF_PATH)} 不存在")
            
            # 父目录 assets 不存在
            if not Path(self.__CONF_PATH).parent.exists():
                Path(self.__CONF_PATH).parent.mkdir()
                
            Path(self.__CONF_PATH).mkdir()
            log.debug(f"成功创建目录：{Path(self.__CONF_PATH)}")
        
        
        # 创建密钥并导出
        db_conf_key = Fernet.generate_key()
        path_db_conf_key = Path(self.__DB_CONF_KEY)
        path_db_conf_key.write_bytes(db_conf_key)
        log.debug("数据库配置文件密钥创建成功")
        log.debug(path_db_conf_key)
        
        db_conf_fernet = Fernet(db_conf_key)
        
        path_db_conf_yaml = Path(self.__DB_CONF)
        path_db_conf_yaml.write_text(
            f'host: "{db_conf_fernet.encrypt(host.encode()).decode()}"\n' +
            f'user: "{db_conf_fernet.encrypt(user.encode()).decode()}"\n' +
            f'password: "{db_conf_fernet.encrypt(password.encode()).decode()}"\n' +
            f'database: "{db_conf_fernet.encrypt(database.encode()).decode()}"\n'
        )
        
        log.debug("数据库配置文件创建成功")
        log.debug(path_db_conf_yaml)
        
    
    def __create_conn(self):
        """连接数据库

        Returns:
            False: 连接失败
            None： 配置文件非法
            Other：连接成功
        """
        
        if self.__check_config_legal():
            conf = self.__load_config()
            log.debug("获取数据库配置信息成功")
            
            
            log.debug("正在尝试连接数据库...")
            conn = self.__connection(**conf)
            
            if conn == None:
                log.debug("连接数据库失败！")
            
            else:
                log.debug("成功连接数据库")
                
            return conn
        
        return None
    
    
    def re_conn(self):
        self.__conn = self.__create_conn()
        
        if self.__conn == None:
            return False

        else:
            self.__create_table()
            return True
    
    
    def __create_table(self):
        """创建表格
        """
        
        self.__create_table_passwords()
        self.__create_table_users()
    
    
    def __create_table_passwords(self):
        """创建 passwords 表
        """
        
        try:
            self.__conn.cursor().execute("""
                CREATE TABLE IF NOT EXISTS passwords(
                    user VARCHAR(255) NOT NULL,
                    website VARCHAR(255) NOT NULL,
                    account VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    PRIMARY KEY(user, website, account)
                )
            """)
        except mysql.connector.Error as e:
            log.error(e)
        
        
    def __create_table_users(self):
        """创建 users 表
        """
        
        try:
            self.__conn.cursor().execute("""
                CREATE TABLE IF NOT EXISTS users(
                    user VARCHAR(255) NOT NULL PRIMARY KEY,
                    salt BLOB NOT NULL,
                    password BLOB NOT NULL,
                    login CHAR(1) NOT NULL
                )
            """)
        except mysql.connector.Error as e:
            log.error(e)
            
    
    def get_conn(self):
        """获取数据库连接信息

        Returns:
            None: 未连接
            Other：连接信息
        """
        return self.__conn
    

db_init = DBInit()