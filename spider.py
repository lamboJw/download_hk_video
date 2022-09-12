# -*- encoding=utf-8 -*-
from browsermobproxy import Server

from webDriver import create_driver


def get_video_url(base_url):
    server = None
    driver = None
    video_url = None
    try:
        server = Server(r'.\lib\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
        server.start()

        proxy = server.create_proxy()

        driver = create_driver("edge", proxy.proxy)

        # base_url = "https://www.gq1000.com/gjf/164112-2-0.html"

        proxy.new_har("hk_video", options={'captureHeaders': True, 'captureContent': True})

        driver.get(base_url)

        result = proxy.har

        for entry in result['log']['entries']:

            _url = entry['request']['url']

            # 根据URL找到数据接口

            if _url.find("dplayer.html") != -1:
                # 获取接口返回内容
                video_url = _url
                break
    finally:
        server.stop()
        driver.quit()

    return video_url
