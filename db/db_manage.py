import mysql.connector
from config import constants

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.conn = self.create_connection(host, user, password, database)
        if self.conn != None:
            self.create_table()

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
            return None

    def create_table(self):
        try:
            self.conn.cursor().execute("""
                CREATE TABLE IF NOT EXISTS %s(
                    website VARCHAR(255) NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    PRIMARY KEY(website, username)
                )
            """, (constants.DB_TABLE_PASSWORD))
        except mysql.connector.Error as e:
            print(e)

    def close_connection(self):
        self.conn.close()


#===================================================================================================================#
#===================================================================================================================#
#===================================================================================================================#
#===================================================================================================================#

    def add_password(self, website, username, password):
        try:
            sql = "INSERT INTO {} (website, username, password) VALUES(%s, %s, %s)".format(constants.DB_TABLE_PASSWORD)
            self.conn.cursor().execute(sql, (website, username, password))
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            print(e)
            return False

    def get_all_password(self):
        try:
            sql = "SELECT * FROM {}".format(constants.DB_TABLE_PASSWORD)
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(e)
            return False

    def get_password(self, website, username):
        try:
            sql = "SELECT * FROM {} where website = %s and username = %s".format(constants.DB_TABLE_PASSWORD)
            cursor = self.conn.cursor()
            cursor.execute(sql, (website, username))
            return cursor.fetchone()
        except mysql.connector.Error as e:
            print(e)
            return False

    def delete_password(self, website, username):
        try:
            sql = "DELETE FROM {} WHERE website=%s AND username=%s".format(constants.DB_TABLE_PASSWORD)
            cursor = self.conn.cursor()
            cursor.execute(sql, (website, username))
            self.conn.commit()
            if cursor.rowcount != 0:
                return True
            else:
                return False
        except mysql.connector.Error as e:
            print(e)
            return False

