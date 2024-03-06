import subprocess
import getpass
from command.cmd_help import cmd_helps
from psdmanage.psd_manage import PasswordManager

manage = PasswordManager()
    

def help():
    for help in cmd_helps:
        print(f"{help}: {cmd_helps[help]}")
    print()
        
        
def cls():
    subprocess.run(["cls"], shell=True)
    
    
def add():
    website = input("请输入网站：")
    username = input("请输入用户名：")
    password = getpass.getpass("请输入密码：")
    if manage.add_password(website, username, password):
        print("添加密码成功！")
    else:
        print("添加密码失败！")
    print()
    
    
def get():
    results = manage.get_all_password()
    if results:
        for result in results:
            print(result)
    else:
        print("未保存密码或密钥不匹配")
    print()
    
    
def delete():
    website = input("请输入网址：")
    username = input("请输入用户名：")
    if manage.delete_password(website, username):
        print("删除密码成功！")
    else:
        print("删除密码失败！")
    print()


