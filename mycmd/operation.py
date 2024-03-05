import subprocess
import getpass
from mycmd.cmd_help import cmd_helps
from passwordmanage import PasswordManager


manage = None

def close():
    manage.close_connection()

def help():
    for help in cmd_helps:
        print(f"{help}: {cmd_helps[help]}")
        
def cls():
    subprocess.run(["cls"], shell=True)

    
def init():
    global manage
    manage = PasswordManager()
    
def import_key():
    filename = input("请输入密钥名：")
    manage.import_key(filename)
    
def export_key():
    filename = input("请输入密钥名：")
    manage.export_key(filename)
    
def add():
    website = input("请输入网站：")
    username = input("请输入用户名：")
    password = getpass.getpass("请输入密码：")
    manage.add_password(website, username, password)
    
    
def get():
    website = input("请输入网址：")
    results = manage.get_password(website)
    if results:
        for result in results:
            print(result)
    
    
def delete():
    website = input("请输入网址：")
    username = input("请输入用户名：")
    manage.delete_password(website, username)
    
    
def show_all():
    results = manage.show_all()
    if results:
        for result in results:
            print(result)