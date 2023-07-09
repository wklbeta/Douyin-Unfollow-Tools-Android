# Douyin-Unfollow-Tools-Android
抖音自动取关自动化Python脚本

# 环境要求
- 电脑要求：Mac
- 手机要求：Android
- 测试通过抖音Android版本：26.0.0(260001)
- 需要安装 [adb](https://developer.android.com/studio/releases/platform-tools?hl=zh-cn) 并放置到环境目录下
- 需要安装 Python3 并放置 python3 到环境目录下（Mac已自带）

# 支持取关的页面
1. 近期互动最少的人页面
2. 关注的人页面

# 注意事项
1. 近期互动最少的人页面全部取关之后会自动停止
2. 关注的人列表页全部取关之后会自动停止
3. 关注的人页面不会取关“互相关注”的人

# 运行方式
1. 打开抖音App
2. 进入关注的人页面/近期互动最少的人页面
3. Mac连接Android手机
4. 在Android手机上启用「开发者模式」：一般位于 设置 > 关于手机 > 软件信息 > 版本号，连续点按版本号七次，会提示已成功开启开发者选项
5. 在Android手机上打开「高级设置」-「开发者选项」-「USB调试开关」
6. 在手机弹出的弹窗中确认开启调试开关并信任当前主机
7. 在Mac上打开“终端”，进入本工程的根目录，执行 `python3 unfollow.py`
