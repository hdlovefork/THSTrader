# THSTrader
量化交易工具。同花顺手机版模拟炒股python API，基于uiautomator2方法实现。依赖下面的项目：
* pytdx（用于获取行情）
* uiautomator2（用于读取与操作界面）

## 为什么有这个项目
源于打首板总是破板之后被买进的痛苦，不光是当天蒙受损失，还要等T+1才能卖出，所以就想着能不能写个程序，能够在打首板的时候排队监控买1的手数，如果有人大量撤单，那么程序就能监控到并且撤单，防止破板被迫买进。

## 程序执行流程
1. THSWithdrawWatcher线程不断的刷新撤单列表，得到添加或删除的股票
2. 如果有添加的股票，那么就将其加入到监控列表中，同时QuotationWatcher线程会不断的请求监控列表中股票的行情，当然如果有删除的股票，那么就将其从监控列表中删除
3. 当行情数据返回时会交给THSWithdrawal.resolve方法处理
4. 接下来会按.env中withdraw配置项条件来判断是否需要撤单，如果需要撤单，那么就会调用THSAction.withdraw方法撤单
5. 重复第1-4步

## 运行时所需依赖
### 1. Python依赖
我使用的是Python3.9.1，请务必使用该版本，否则可能会出现无法正常运行的情况。
> windows下载地址：https://www.python.org/downloads/windows/
> macos下载地址：https://www.python.org/downloads/macos/

### 2. 下载项目并安装依赖
``` bash
git clone https://github.com/nladuo/THSTrader.git
cd THSTrader
pip install -r requirements.txt
```
> 安装依赖过程中如果有报错，请将下面内容添加到hosts文件中：
```bash
185.199.109.133 raw.githubusercontent.com
```

### 3. 安装夜神模拟器（支持Mac、Windows、Linux）
下载链接：[https://www.yeshen.com/](https://www.yeshen.com/)

### 4. 配置模拟器分辨率
与屏幕分辨率无关

### 5. 安装同花顺APP
在模拟器上安装同花顺APP，模拟器上用浏览器打开链接：[http://focus.10jqka.com.cn/special/phone/wapsubject_8299.shtml](http://focus.10jqka.com.cn/special/phone/wapsubject_8299.shtml) 

### 6. 查看模拟器或真机serial_no（推荐使用真机）
* 模拟器推荐夜神支持Mac、Windows、Linux 
* 真机推荐安卓手机

本项目在小米12手机上测试通过
> 小米12需要在开发者选项中开启以下选项：
> * "USB调试"该项允许adb连接真机
> * "USB调试（安全设置）"该项允许模拟点击
> * "USB安装"该项允许真机通过adb安装ATX

本项目在荣耀play手机上测试通过
> 荣耀play需要在开发者选项中开启以下选项：
> * "USB调试"该项允许adb连接真机

```bash
# 查看方法如下：
# 1.进入uiautomatorviewer目录
cd uiautomatorviewer
# 2.连接模拟器或真机
./adb kill-server
#   a.连接手机示例
./adb devices
#   b.连接夜神模拟器示例
#   夜神模拟器默认serial_no为127.0.0.1:62001，其它模拟器请自行查看
./adb connect 127.0.0.1:62001
```
当通过上面步骤连接好模拟器或真机后，按下面所示输入`./adb devices`命令，如果看到类似下面的输出，那么就说明连接成功了：
```bash
➜  uiautomatorviewer ./adb devices
* daemon not running; starting now at tcp:5037
* daemon started successfully
List of devices attached
acfd70a2	unauthorized
```
这里看到的`acfd70a2`就是serial_no，如果是夜神模拟器，那么serial_no为`127.0.0.1:62001`
，然后请将这个serial_no填入.env.toml文件中的`serial_no`字段

## 运行程序
### 1. 获取可用行情服务器的ip，进入tools/目录下运行：
``` bash
cd tools
python check.py
参数（可选）:
    --num: 获取可用服务器的数量（默认为5个）
    --out: 输出到文件的路径（默认为当前目录下的ips.toml）
```
> check程序会自动测试并获取可用的行情服务器ip，然后将可用的ip写入到ips.toml文件中，会按照速度从快到慢的顺序排列，速度越快，排在越前面。

### 2. 复制配置文件，然后根据需要修改配置文件：
``` bash
cp .env.toml.example .env.toml
```

### 3. 运行程序，进入项目根目录下运行：
``` bash
python main.py
```

## 二次开发
### 1. 用到的工具
查看[uiautomatorviewer](uiautomatorviewer/README.md)的使用方法
