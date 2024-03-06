from command.cmd import cmds
   

def main():
    while True:
        cmd = input("PSDManage> ")
        if cmd in cmds and cmds[cmd]() == 'exit':
            break
        elif not cmd in cmds:
            print("未知指令\n")
            

if __name__ == "__main__":
    cmds["/cls"]()
    main()
    print("done.")