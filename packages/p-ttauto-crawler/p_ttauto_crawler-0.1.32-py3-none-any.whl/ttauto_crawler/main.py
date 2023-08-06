import sys
import os
import platform
import logging
import urllib3
import datetime
import shutil
from logging.handlers import RotatingFileHandler
from urllib.parse import *
from pkg_resources import parse_version
from ttauto_crawler import utils
from ttauto_crawler import auto_crawler
from ttauto_crawler import txt2proj
from ttauto_crawler import video_merge

def img2video():
    if len(sys.argv) <= 2:
        print('please s')
        return
    dir = sys.argv[2]
    cnt = sys.argv[3]
    if cnt.isdigit() == False:
        print('count is not digit')
        return
    if os.path.exists(dir) == False:
        print(f'path: {dir} not found')
        return
    txt2proj.randomImageCntToVideo(dir, int(cnt))
    
def mergeVideo():
    config = sys.argv[2]
    if os.path.exists(config) == False:
        print(f'path: {config} not found')
        return
    if os.path.isfile(config) == False:
        print(f'path: {config} not file!')
        return
    video_merge.mergeWithConfig(config)
         
def auto():  
    auto_crawler.autoCrawler()

module_func = {
    "--img2video": img2video,
    "--merge": mergeVideo,
    "--auto": auto
}

def main():
    urllib3.disable_warnings()
    my_handler = RotatingFileHandler(f"{os.path.dirname(os.path.abspath(__file__))}/log.log",
                                      mode='a', 
                                      maxBytes=5*1024*1024, 
                                      backupCount=2, 
                                      encoding=None,
                                      delay=0)
    my_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    my_handler.setLevel(logging.INFO)
    app_log = logging.getLogger()
    app_log.setLevel(logging.INFO)
    app_log.addHandler(my_handler)

    if len(sys.argv) < 2:
        auto()
        return
    module = sys.argv[1]
    if module in module_func:
        module_func[module]()
        
if __name__ == '__main__':
    main()
