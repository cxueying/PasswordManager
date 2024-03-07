# PasswordManager（密码管理器）

# 使用
    需要链接Mysql数据库使用
    第一次启动会要求连接数据库，依照提示输入信息即可
    
    密钥和配置文件保存在 config 目录下，请妥善保存
    如果丢失 database.key ，则无法获取数据库中的密码
    db_conf.key 是解密 db_conf.yaml 的密钥
    db_conf.yaml 记录连接信息
# 操作命令
    /help 查看所有命令
    /exit 退出程序
    /cls 清屏
    /add 添加密码
    /get 获取密码
    /delete 删除密码
# Git 使用
    git config --global user.email "you@example.com"
    git config --global user.name "Your Name"

    git tag v1.0    创建一个名称为 v1.0 的标签
    git push origin v1.0    推送刚刚创建的 v1.0 标签

    git checkout v1.0   切换到 v1.0 版本

    git add file1.txt   添加推送的文件
    git commit -m "message"     提交的消息（提交到本地仓库）
    
    git remote add origin url      将本地仓库与 url 关联起来

    git push origin master      将提交推送的github仓库
        origin 是远程仓库的名字
        master 是推送分支的名字