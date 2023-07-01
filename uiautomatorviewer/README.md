### 1.运行adb连接手机或模拟器
```bash
# 连接夜神模拟器（支持Mac、Windows、Linux）
cd uiautomatorviewer
# 连接夜神模拟器示例
./adb connect 127.0.0.1:62001
# 连接手机示例
./adb kill-server
./adb devices
```
### 2.运行uiautomatorviewer
```bash
java -XstartOnFirstThread -jar uiautomatorviewer-standalone-1.1-all.jar
```
> 注意：当运行THSTrader/main.py后，需要重启模拟器或真机才能通过uiautomatorviewer查看到界面元素，否则它连接时会报错