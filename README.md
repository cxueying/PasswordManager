# PasswordManager（密码管理器）

# 使用
    需要链接Mysql数据库使用
    第一次启动会要求连接数据库，依照提示输入信息即可
    
    密钥和配置文件保存在 config 目录下，请妥善保存
    如果丢失 database.key ，则无法获取数据库中的密码
    db_conf.key 是解密 db_conf.yaml 的密钥
    db_conf.yaml 记录连接信息
    
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

    git checkout main       切换到 main 分支

    git merge feature-branch    将feature-branch 分支合并到当前分支

    git push origin main    将main分支推送到远程仓库

    git branch  查看本地分支

    git branch -r   查看与本地仓库关联的远程仓库

    git branch -a   查看本地和远程分支

    git tag     查看仓库中的所有标签

    git tag -d v1.0 删除 v1.0 标签

    git push --delete origin v1.0   删除远程仓库（通常是origin）上名为v1.0的标签（需要先删除本地标签）