# BookRecommend_Back

**此处存放后端项目**

## 配置

1. 修改config.py.example中的内容
2. 将config.py.example重命名为config.py

## 前后端在同一局域网中通信

1. 关闭后端机公用网络防火墙
2. 后端机`ipconfig`,找到对应的IPv4 地址
3. 修改后端代码为`app.run(host='0.0.0.0', port=5000, debug=True)`
4. 注意pycharm的flask配置文件需在additional option一栏手动添加`--host=0.0.0.0 --port=5000`
5. 修改baseUrl