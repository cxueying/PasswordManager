import subprocess
import getpass
from command.cmd_help import cmd_helps
from psdmanage.psd_manage import PasswordManager
from logger.log import log



manage = PasswordManager()
log.debug("manage初始化成功")

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
        log.info("添加密码成功！")
        log.debug(f"website: {website}, username: {username}")
    else:
        log.info("添加密码失败！")
        log.debug(f"website: {website}, username: {username}")
    print()
    
    
def get():
    results = manage.get_all_password()
    if results:
        log.info("获取所有密码成功")
        for result in results:
            print(result)
    else:
        log.info("获取所有密码失败")
        log.info("未保存密码或密钥不匹配")
    print()
    
    
def delete():
    website = input("请输入网址：")
    username = input("请输入用户名：")
    if manage.delete_password(website, username):
        log.info("删除密码成功！")
        log.debug(f"website: {website}, username: {username}")
    else:
        log.info(f"删除密码失败！")
        log.debug(f"website: {website}, username: {username}")
    print()


