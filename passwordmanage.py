import mysql.connector
import yaml
from pathlib import Path
from cryptography.fernet import Fernet

class PasswordManager:
    
    def __init__(self, key=None, config_filename='db_conf.yaml', config_key = 'db_conf.key'):
        self.key = self.import_key() or self.generate_key()
        self.fernet = Fernet(self.key)
        db_config = self.load_db_config(config_filename, config_key)
        self.conn = self.create_connection(**db_config)
        self.create_table()

    def generate_key(self):
        key = Fernet.generate_key()
        with open("database.key", "wb") as f:
            f.write(key)
        return key

    def encrypt(self, message):
        return self.fernet.encrypt(message.encode()).decode()

    def decrypt(self, encrypted_message):
        try:
            return self.fernet.decrypt(encrypted_message.encode()).decode()
        except:
            return None

    def create_db_config(host, user, password, database, filename = "db_conf"):
        db_key = Fernet.generate_key()
        with open(f"{filename}.key", "wb") as f:
            f.write(db_key)
        
        db_fernet = Fernet(db_key)
        
        def db_encrypt(message):
            return db_fernet.encrypt(message.encode()).decode()
        
        with open(f"{filename}.yaml", "w") as f:
            f.write(f'host: "{db_encrypt(host)}"\n')
            f.write(f'user: "{db_encrypt(user)}"\n')
            f.write(f'password: "{db_encrypt(password)}"\n')
            f.write(f'database: "{db_encrypt(database)}"\n')
  
    def load_db_config(self, filename, config_key):
        if not Path(filename).exists() or not Path(config_key).exists():
            print(f"file {filename} or {config_key} is not exists!")
            exit()
        with open(filename, 'r') as f:
            if filename.endswith('.yml') or filename.endswith('.yaml'):
                config = yaml.safe_load(f)
            else:
                raise ValueError('Unsupported file type')

            db_key = None
            with open(config_key, 'rb') as f:
                db_key = f.read()
            db_fernet = Fernet(db_key)
            
            def db_decrypt(encrypted_message):
                return db_fernet.decrypt(encrypted_message.encode()).decode()
            
            return {
                'host': db_decrypt(config['host']),
                'user': db_decrypt(config['user']),
                'password': db_decrypt(config['password']),
                'database': db_decrypt(config['database']),
            }

    def create_connection(self, host, user, password, database):
        conn = None;
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            conn.database = database
            return conn
        except mysql.connector.Error as e:
            print(e)
            exit()

    def create_table(self):
        try:
            self.conn.cursor().execute("""
                CREATE TABLE IF NOT EXISTS passwords(
                    website VARCHAR(255) NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    PRIMARY KEY(website, username)
                )
            """)
        except mysql.connector.Error as e:
            print(e)

    def close_connection(self):
        self.conn.close()

    def import_key(self, filename = "database.key"):
        if Path(filename).exists():
            with open(filename, "rb") as f:
                return f.read()
        else:
            return None
            
    def export_key(self, filename = "database.key"):
        with open(filename, "wb") as f:
            f.write(self.key)




    def add_password(self, website, username, password):
        try:
            self.conn.cursor().execute("""
                INSERT INTO passwords(website, username, password)
                VALUES(%s, %s, %s)
            """, (website, username, self.encrypt(password)))
            self.conn.commit()
        except mysql.connector.Error as e:
            print(e)

    def get_password(self, website):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM passwords WHERE website=%s", (website,))
        datas = cursor.fetchall()
        if datas:
            results = []
            for data in datas:
                result = {
                    'website': data[0],
                    'username': data[1],
                    'password': self.decrypt(data[2])
                }
                if result['password'] == None:
                    continue
                
                results.append(result)
            
            return results


    def delete_password(self, website, username):
        try:
            self.conn.cursor().execute("DELETE FROM passwords WHERE website=%s AND username=%s", (website,username))
            self.conn.commit()
        except mysql.connector.Error as e:
            print(e)

    def show_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM passwords")
        datas = cursor.fetchall()
        if datas:
            results = []
            for data in datas:
                result = {
                    "website": data[0],
                    "username": data[1],
                    "password": self.decrypt(data[2])
                }
                if result['password'] == None:
                    continue
                
                results.append(result)
            return results
