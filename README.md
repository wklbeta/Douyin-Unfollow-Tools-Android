# Douyin-Unfollow-Tools-Android
抖音自动取消关注Python脚本

# 特点
- 代码精简，纯本地操作，隐私无忧
- 通过官方Android Debug Bridge（adb）获取布局精准识别“取关按钮”在页面中的位置进行操作
- 兼容关注列表中有“正在直播的头像”时获取不到布局的情况
- 兼容近期互动最少的人页面可能出现“假的加载到底”的情况

# 环境要求
- 操作系统支持：Windows/Mac/Linux
- 手机要求：Android
- 测试通过的抖音Android版本：26.0.0(260001)，其他版本不保证成功，有问题可以提issue
- 需要安装 [adb](https://developer.android.com/studio/releases/platform-tools?hl=zh-cn) 并放置到环境目录下
- 需要安装 Python3 并放置 python3 到环境目录下（Mac已自带，Windows需[手动安装](https://www.python.org/downloads/windows/)）

# 支持取关的页面
1. 近期互动最少的人页面
2. 关注的人页面

# 注意事项
1. 近期互动最少的人页面全部取关之后会自动停止
2. 关注的人列表页全部取关之后会自动停止
3. 关注的人页面不会取关“互相关注”的人
4. 因为“假的加载到底”出现返回上一页再进入页面重试是正常逻辑

# 运行方式
1. 打开抖音App
2. 进入关注的人页面/近期互动最少的人页面
3. 电脑通过USB连接Android手机
4. 在Android手机上启用「开发者模式」：一般位于 设置 > 关于手机 > 软件信息 > 版本号，连续点按版本号七次，会提示已成功开启开发者选项
5. 在Android手机上打开「高级设置」-「开发者选项」-「USB调试开关」
6. 在手机弹出的弹窗中确认开启调试开关并信任当前主机
7. 在Mac上打开“终端”；或在Windows打开“命令提示符”：Windows键+R > 输入"cmd" > 回车
8. 进入本工程的根目录：在“终端”或“命令提示符”窗口中输入“cd + 空格”，然后把工程目录用鼠标拖进窗口中，再点击回车即可
9. 在“终端”或“命令提示符”窗口中输入`python3 unfollow.py`，回车

# 打赏
<img src="./WeChat_QR_Code.jpg" alt="WeChat_QR_Code" height="400px" />
