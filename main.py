import mysql.connector
import getpass
from mycmd.cmd import cmds
from pathlib import Path
from passwordmanage import PasswordManager
from mycmd import operation


def init():
    print("正在初始化程序中...")
    if not Path("db_conf.key").exists() or not Path("db_conf.yaml").exists():
        while True:
            host = input("请输主机ip：")
            username = input("请输入数据库管理员名称：")
            password = getpass.getpass("请输入数据库管理员密码：")
            database = input("请输入数据库名称：")
            
            print("正在尝试连接数据库...")
            try:
                conn = mysql.connector.connect(
                    host=host,
                    user=username,
                    password=password
                )
                PasswordManager.create_db_config(host, username, password, database)
                break
            
            except mysql.connector.Error as e:
                print(e)
                choose = input("是否重新尝试(Y/n)：")
                while True:
                    if choose == 'y' or choose == 'Y' or choose == 'n' or choose == 'N':
                        break
                    choose = input("是否重新尝试(Y/n)：")
                    
                if choose == 'y' or choose == 'Y':
                    continue
                elif choose == 'n' or choose == 'N':
                    exit()
                else:
                    print("非法输入！")
            
    operation.init()
    print("初始化成功！")

    

def main():
    while True:
        full_cmd = input("PSDManage> ")
        cmd_list = full_cmd.split()
        if cmd_list == []:
            continue
        cmd = cmd_list[0]
        args = cmd_list[1:]

        if cmd in cmds:
            if cmds[cmd](*args) == "exit":
                break
            
        else:
            print("未知指令")
            

            
    

if __name__ == "__main__":
    cmds["/cls"]()
    init()
    cmds["/cls"]()
    main()
    cmds["/close"]()
    print("done.")