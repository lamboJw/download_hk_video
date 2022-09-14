# -*- encoding=utf-8 -*-
import os

from browsermobproxy import Server

from webDriver import create_driver

driver_type = "chrome"
proxy_port = 8089


def get_video_url(base_url):
    server = None
    driver = None
    video_url = None
    try:
        server = Server(r'.\lib\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat', options={"port": proxy_port})
        server.start()
        proxy = server.create_proxy()
        driver = create_driver(driver_type, proxy.proxy)
        proxy.new_har("hk_video", options={'captureHeaders': True, 'captureContent': True})
        driver.get(base_url)
        result = proxy.har
        for entry in result['log']['entries']:
            _url = entry['request']['url']
            if _url.find("dplayer.html") != -1:
                video_url = _url
                break
    except Exception as e:
        print(e)
    finally:
        server_port = server.port
        server.stop()
        if driver is not None:
            driver.quit()
        # 关闭进程中的java进程
        find_port = 'netstat -aon|findstr %s' % server_port
        result = os.popen(find_port)
        text = result.read()
        if text.__len__() > 0:
            pid_line = text.split('\n', 1)[0]
            pid = pid_line.replace(" ", "").split("LISTENING")[1]
            find_kill = 'taskkill -f -pid %s' % pid
            result = os.popen(find_kill)
            cmd = result.read()
            print(cmd)
        result.close()

    return video_url
