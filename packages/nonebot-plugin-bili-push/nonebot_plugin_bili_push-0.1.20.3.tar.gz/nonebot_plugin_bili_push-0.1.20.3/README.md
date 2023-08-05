<div align="center">
  <p><img src="http://cdn.kanon.ink/api/image?key=899178&imageid=image-20230618-220942-65085441" width="150" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-bili-push
 B订阅推送插件 
</div>

## 示例

![输入图片描述](README_md_files/9cf89890-0952-11ee-8733-25d9c7397331.jpeg?v=1&type=image)
![输入图片描述](README_md_files/7fd7ee50-0952-11ee-8733-25d9c7397331.jpeg?v=1&type=image)


## 安装
（以下方法三选一）

一.命令行安装：（貌似安装不了，可以试一下先） 

    nb plugin install nonebot-plugin-bili-push
    
二.pip安装：

1.执行此命令

    pip install nonebot-plugin-bili-push
    
2.修改pyproject.toml使其可以加载插件

    plugins = [”nonebot-plugin-bili-push“]
    
 三.使用插件文件安装：（不推荐） 
 
 1.下载插件文件，放到plugins文件夹。

2.修改pyproject.toml使其可以加载插件

 
## 配置
在 nonebot2 项目的`.env`文件中选填配置

配置管理员账户，只有管理员才能添加订阅

    SUPERUSERS=["12345678"] # 配置 NoneBot 超级用户
插件数据存放位置，默认为 “./”。

    bilipush_basepath="./"

是否使用api来获取emoji图像，默认使用。

    bilipush_emojiapi=True

刷新间隔：每次刷新间隔多少分钟，默认为12分钟。

    bilipush_waittime=12

发送间隔： 每次发送完成后等待的时间，单位秒，默认10-30秒。
时间为设置的时间再加上随机延迟10-20秒

    bilipush_sleeptime=10
    
只响应一个bot（beta）

一个群内有多个bot，可以只让1个bot处理消息。
默认为关闭该功能，既所有bot都会响应

    bilipush_botswift=False
    

## To-Do

 - [ ] 将请求api改为异步
 - [ ] 完善动态类型（目前仅支持文字、图文、视频、转发、~~文章~~）
 - [ ] 增加上下播推送（差点忘了还有直播推送）
 - [ ] 自动断开api连接
 - [ ] 自动bug报告
 - [ ] 字体排版优化（字符位置以及）
 - [ ] 添加话题标签
 - [ ] 添加动态底部相关的内容绘制（游戏、动漫）
 - [ ] 添加各种装饰（头像框、装扮等）
 - [ ] 配置推送样式
 - [ ] 增加可配置内容（或尝试创建配置文件的方式
 - [ ] 动态背景图？闲的时候可以整一下
 - [ ] 单nb对接多q的兼容
 - [ ] 版面优化
 - [ ] 优化print（）
 - [ ] 代码整理
 - [x] ~~添加本地计算emoji模式~~
 - [x] ~~取消推送过时动态~~
 - [x] ~~emoji不能正常打印~~
 - [x] ~~添加动态类型不支持时的解决方法~~

## 参考内容
Mirai动态绘制插件 [BilibiliDynamic MiraiPlugin](https://github.com/Colter23/bilibili-dynamic-mirai-plugin)

## 交流
-   交流群[鸽子窝里有鸽子（291788927）](https://qm.qq.com/cgi-bin/qm/qr?k=QhOk7Z2jaXBOnAFfRafEy9g5WoiETQhy&jump_from=webapi&authKey=fCvx/auG+QynlI8bcFNs4Csr2soR8UjzuwLqrDN9F8LDwJrwePKoe89psqpozg/m)
-   有疑问或者建议都可以进群唠嗑唠嗑。
