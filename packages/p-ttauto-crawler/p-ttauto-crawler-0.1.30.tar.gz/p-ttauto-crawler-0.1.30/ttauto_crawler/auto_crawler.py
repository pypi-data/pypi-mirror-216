import sys
import os
import time
from ttauto_crawler import utils
from ttauto_crawler import txt2proj
from ttauto_crawler import downloader
from ttauto_crawler import video_random_cutter
from ttauto_crawler import processing
from ttauto_crawler import uploading
from ttauto_crawler import task
from template_generator import binary as genertor_binary
from threading import Thread, current_thread, Lock
import calendar
from urllib.parse import *
import queue
import requests
import json
import random
import socket

THEADING_LIST = []
lock = Lock()

def qyWechatRobot(param):
    try:
        s = requests.session()
        s.headers.update({'Connection':'close'})
        headers = dict()
        headers['Content-Type'] = "application/json"
        res = s.post(f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ab1e9959-5bb2-4c7f-aa85-221bccffcea8", json.dumps(param), headers=headers, verify=False)
        s.close()
    except Exception as e:
        utils.logInfo(f"===== qyapi.weixin.qq.com fail ", True)

class CralwerStateThread(Thread):
    running = False
    machine_name = socket.gethostname()
    last_data = None
    def __init__(self):
        super().__init__()
        self.running = True
        self.daemon = True
        self.start()
    def run(self):
        qyWechatRobot({
            "msgtype": "text",
            "text": {
                "content": f"爬虫机<{self.machine_name}> 上线"
            }
        })
        while self.running:
            time.sleep(60)
            try:
                data = task.allTaskState(lock)
                if len(data["task_list"].strip()) == 0:
                    param = {
                        "msgtype": "text",
                        "text": {
                            "content": f"爬虫机<{self.machine_name}> 空载"
                        }
                    }
                    qyWechatRobot(param)
                    time.sleep(60*5)
                else:
                    if (self.last_data != None and data != None and 
                                data["task_list"] == self.last_data["task_list"] and 
                                data["downloading"] == self.last_data["downloading"] and 
                                data["processing"] == self.last_data["processing"] and 
                                data["uploading"] == self.last_data["uploading"]):
                        continue
                    self.last_data = data
                    task_list = data["task_list"]
                    wait_downloading = data["wait_downloading"]
                    downloading = data["downloading"]
                    wait_processing = data["wait_processing"]
                    processing = data["processing"]
                    wait_uploading = data["wait_uploading"]
                    uploading = data["uploading"]
                    param = {
                        "msgtype": "markdown",
                        "markdown": {
                            "content": f"爬虫机<<font color=\"warning\">{self.machine_name}</font>> 挂载任务: <<font color=\"warning\">{task_list}</font>> \n\
                                >等待下载<font color=\"warning\">{wait_downloading}</font> \n\
                                >下载中<font color=\"warning\">{downloading}</font> \n\
                                >等待合成<font color=\"warning\">{wait_processing}</font> \n\
                                >合成中<font color=\"warning\">{processing}</font> \n\
                                >等待上传<font color=\"warning\">{wait_uploading}</font> \n\
                                >上传中<font color=\"warning\">{uploading}</font>"
                        }
                    }
                    qyWechatRobot(param)
            except:
                utils.logInfo(f"===== somthing CralwerStateThread fail", True)
    def markStop(self):
        self.running = False

class CralwerThread(Thread):
    running = False
    type = task.C_STATE.WAIT_DOWNLOAD
    def __init__(self, t=task.C_STATE.WAIT_DOWNLOAD):
        super().__init__()
        self.running = True
        self.daemon = True
        self.type = t
        self.start()
    def run(self):
        while self.running:
            if self.type == task.C_STATE.DOWNLOADING:
                taskItem = task.popDownload(lock)
                if taskItem:
                    curGroupId = taskItem["curGroupId"]
                    url = taskItem["url"]
                    utils.logInfo(f"==={curGroupId} begin", True)
                    utils.logInfo(f"==={curGroupId} GetTask: {taskItem}", True)
                    curDownloadDir, allCount = downloader.download(url, curGroupId)
                    taskItem["start_pts"] = calendar.timegm(time.gmtime())
                    taskItem["download_count"] = allCount
                    taskItem["download_dir"] = curDownloadDir
                    task.finishDownload(lock, taskItem)

            if self.type == task.C_STATE.TEMPLATEING and task.canTemplate(lock):
                taskItem = task.popTemplate(lock)
                if taskItem:
                    curGroupId = taskItem["curGroupId"]
                    curDownloadDir = taskItem["download_dir"]
                    utils.logInfo(f"==={curGroupId} processing video", True)
                    if taskItem["video_merge_num"] > 0 and taskItem["video_merge_second"] > 0:
                        # random cutter
                        utils.logInfo(f"==={curGroupId} random cutter ", True)
                        curDownloadDir = video_random_cutter.video_cutter(curDownloadDir, curGroupId, taskItem)
                    utils.logInfo(f"==={curGroupId} template video", True)
                    outputDir, processCount = processing.processToVideo(curDownloadDir, taskItem)
                    taskItem["processed_dir"] = outputDir
                    task.finishTemplate(lock, taskItem)

            if self.type == task.C_STATE.UPLOADING and task.canUpload(lock):
                taskItem = task.popUpload(lock)
                if taskItem:
                    curGroupId = taskItem["curGroupId"]
                    allCount = taskItem["download_count"]
                    processed_dir = taskItem["processed_dir"]
                    start_pts = taskItem["start_pts"]
                    utils.logInfo(f"==={curGroupId} uploading + notifying ", True)
                    uploadCount = uploading.upload(processed_dir, curGroupId)
                    current_pts = calendar.timegm(time.gmtime())
                    utils.logInfo(f"==={curGroupId} complate => {curGroupId} rst={uploadCount}/{allCount} duration={(current_pts - start_pts)}", True)
                    task.finishUpload(lock, taskItem)
                    clearDir(curGroupId)
                    needNotifyGroups, needNotifyCounts, yesterday = utils.saveToCounter(curGroupId, uploadCount)
                    if needNotifyGroups and len(needNotifyGroups) > 0:
                        param = {
                            "msgtype": "markdown",
                            "markdown": {
                                "content": f"昨日:<<font color=\"warning\">{yesterday}</font>> 共处理: <<font color=\"warning\">{needNotifyCounts}</font>>个视频 \n\
                                    >已处理任务<font color=\"warning\">{needNotifyGroups}</font>"
                            }
                        }
                        qyWechatRobot(param)
            time.sleep(10)
    def markStop(self):
        self.running = False

def clearDir(curGroupId):
    downloader.clearDir(curGroupId)
    video_random_cutter.clearDir(curGroupId)
    processing.clearDir(curGroupId)

def canbeDownload():
    return downloader.downloadDirSubCount() < 3

def getTask():
    try:
        s = requests.session()
        s.headers.update({'Connection':'close'})
        res = s.get(f"https://beta.2tianxin.com/common/admin/tta/get_task?t={random.randint(100,99999999)}", verify=False)
        s.close()
        if len(res.content) > 0:
            data = json.loads(res.content)
            if len(data) > 0 and "id" in data:
                curGroupId = data["id"]
                url = data["url"].replace("\n", "").replace(";", "").replace(",", "").strip()
                template_name_list = data["template_name_list"]
                if template_name_list == None:
                    template_name_list = []
                video_merge_num = int(data["video_merge_num"])
                video_merge_second = int(data["video_merge_second"])
                img_to_video = int(data["img_to_video"])
                split_video = int(data["split_video"])
                add_text = int(data["add_text"])
                tag = data["tag"]
                verticalScreen = False
                if "VerticalScreen=true" in url:
                    verticalScreen = True
                    url = url.replace("VerticalScreen=true","")
                return curGroupId, url, template_name_list, video_merge_num, video_merge_second, img_to_video, split_video, add_text, verticalScreen, tag
    except Exception as e:
         utils.logInfo(e)
    return None, None, None, None, None, None, None, None, None, None

def autoCrawler():    
    thisFileDir = os.path.dirname(os.path.abspath(__file__))
    global THEADING_LIST
    for i in range(0, task.MAX_DOWNLOADING_COUNT):
        THEADING_LIST.append(CralwerThread(t=task.C_STATE.DOWNLOADING))
    for i in range(0, task.MAX_PROCESSING_COUNT):
        THEADING_LIST.append(CralwerThread(t=task.C_STATE.TEMPLATEING))
    for i in range(0, task.MAX_UPLOADING_COUNT):
        THEADING_LIST.append(CralwerThread(t=task.C_STATE.UPLOADING))
    THEADING_LIST.append(CralwerStateThread())
    while (os.path.exists(os.path.join(thisFileDir, "stop.now")) == False):
        if task.canAddDownload(lock):
            try:
                # task.push(lock, {
                #     "curGroupId":0, 
                #     "url":"ftp://192.168.3.220/1TB01/data/test/",
                #     "crawler_template_name":[ "lady_bags_recommend" ], 
                #     "addRandomText":False, 
                #     "splitDuration":0, 
                #     "img_to_video":5,
                #     "video_merge_num":0,
                #     "video_merge_second":0, 
                #     "verticalScreen":False, 
                #     "tag":"bag"
                # })
                curGroupId, url, template_name_list, video_merge_num, video_merge_second, img_to_video, split_video, add_text, verticalScreen, tag = getTask()
                if curGroupId:    
                    task.push(lock, {
                        "curGroupId":curGroupId, 
                        "url":url,
                        "crawler_template_name":template_name_list, 
                        "addRandomText":add_text, 
                        "splitDuration":split_video, 
                        "img_to_video":img_to_video,
                        "video_merge_num":video_merge_num,
                        "video_merge_second":video_merge_second, 
                        "verticalScreen":verticalScreen, 
                        "tag":tag
                    })
            except Exception as e:
                utils.logInfo("====================== uncatch Exception ======================", True)
                utils.logInfo(e)
                utils.logInfo("======================      end      ======================")
        time.sleep(10)
    utils.logInfo(f"prepare stop !", True)
    for t in THEADING_LIST:
        t.markStop()
    for t in THEADING_LIST:
        t.join()
    os.remove(os.path.join(thisFileDir, "stop.now"))
    qyWechatRobot({
        "msgtype": "text",
        "text": {
            "content": f"爬虫机<{socket.gethostname()}> 下线"
        }
    })
    utils.logInfo(f"stoped !", True)