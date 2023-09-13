# bilibli simple biggest video download

# bilibili简单粗暴下载最高画质视频备份视频

## 配置文件

​        在`bilibili_video_download_config.txt`的`SESSDATA`字段填入浏览器获取的cookie中的`SESSDATA`值，`video_save_path`字段填入视频保存的路径（Windows中路径中所有的`\`要改成`\\`）。

## 运行环境&安装依赖

​        需要安装python3

​        `pip install -r requirements.txt`

## 使用方法

​        在当前目录的命令行中输入：`py bilibili_video_download.py`运行，根据提示输入视频的av号或BV号。一次只能下载一个视频。