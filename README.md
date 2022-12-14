# download_hk_video
港剧天堂网下载视频 \
https://www.gq1000.com/ 
## 环境需求
1. python 3.9，使用anaconda比较方便，无需额外安装太多扩展，只需要额外安装以下两个插件即可：
   1. selenium
   2. [browsermob-proxy](https://github.com/lightbody/browsermob-proxy/)
2. java 8
3. chrome 或 微软Edge
    
## 检查浏览器版本和webDriver版本是否匹配
浏览器版本必须与webDriver版本匹配，否则会打开浏览器失败。 当前webDriver版本：
1. Chrome版本为105.0.5195.52
2. Edge版本为105.0.1343.34

如果版本不匹配，请自行下载对应版本的webDriver覆盖webDriver/win目录下的对应文件


## 使用
1. 当前默认使用Chrome浏览器，如果需要修改为Edge，请修改`config.json`文件中`driver_type`参数为`edge`。
2. 获取m3u8链接，需要用到代理服务器，而代理服务器需要占用一个端口，当前默认使用`8089`，如果`8089`端口已经被其他应用占用了，可以修改`config.json`文件中`proxy_port`的值为未被占用的端口
3. 在项目根目录，打开终端，输入`python ./main.py`
4. 根据提示，填入电视剧的播放页的链接，如：[https://www.gq1000.com/gjf/117512-1-0.html](https://www.gq1000.com/gjf/117512-1-0.html)
5. 程序会自动在项目根目录创建`output`文件夹，并获取剧集名称，创建剧集名文件夹，自动下载整个剧集的 ***给定链接对应集数*** 及 ***往后所有集数***，每集名称为 ***剧集名-集数.mp4***。

## 可执行程序
项目同时提供了已经打包好的exe程序，只需要解压，运行`main.exe`就可以了。

## 错误处理
1. 如果遇到`获取m3u8链接失败`错误，可以根据当前已完成下载的集数，可重新执行程序，填写下一集的链接，继续下载。
2. 如果存在某一集的文件夹，但是程序已经错误停止了，说明这一集下载失败，请删除该文件夹，如果有这一集的mp4文件，也删除掉，然后重新开始下载。