
Flask 知乎
=====================
## 简介
- 2019/07-2019/08 部署在：http://www.blackjude.com/zhihu
- 线上项目的测试账号 用户名：maixy  密码：123
- 实现用户注册，问题与回答的提交，用户回复与点赞，私信，邮件提醒，以及游客浏览等功能
- 使用MySQL作为后端数据库，实现并使用以 MySQL为底层的ORM
- 使用Redis为服务端Session以及首页话题列表进行数据缓存
- 使用Jinja2模版引擎进行内容渲染以及模版继承，提高代码的复用率
- 前端JS AJAX实现无刷新式的回答与点赞操作
- JS实现富文本编辑与显示，CSS完成布局
- 使用Gunicorn实现多进程并发编程
- 部署Nginx实现应用的反向代理与文件缓存


## 运行环境
- Ubuntu Server 18.04.1 LTS 64位
- Python 3.6.5

## 部署
### 相关依赖的安装

```
bash deploy.sh
```

### 测试环境的数据库初始化
```
python3 reset.py
```

### 重启应用
```
bash restart.sh
```

## 功能演示
### 游客模式下浏览话题详情
- 从话题列表进入详情页
- 游客模式下不能点赞，不能提交回答与评论
![浏览话题详情](https://github.com/maixianyu/flask_zhihu/blob/master/readme/enter_detail.gif)

### 登录
- 利用测试账号进行登录，用户名：maixy  密码：123
- 登录后可以点赞，提交回答与评论
![浏览话题详情](https://github.com/maixianyu/flask_zhihu/blob/master/readme/login.gif)

### 提交回答
- AJAX 无刷新提交回答
- 回答的文本支持富文本显示
![提交回答](https://github.com/maixianyu/flask_zhihu/blob/master/readme/submit-answer.gif)

### 点赞
- AJAX 无刷新点赞
![点赞](https://github.com/maixianyu/flask_zhihu/blob/master/readme/press-zan.gif)

### 发表评论
- 在具体的回答下发表评论
![发表评论](https://github.com/maixianyu/flask_zhihu/blob/master/readme/submit-comment.gif)

### 查看并修改用户个人资料
- 查看用户资料
- 修改用户头像
![查看资料](https://github.com/maixianyu/flask_zhihu/blob/master/readme/user-profile.gif)

### 用户间发送站内信
- 用户间发送站内信
- 收到信后能得到邮件提示
![站内信](https://github.com/maixianyu/flask_zhihu/blob/master/readme/user-mail.gif)
