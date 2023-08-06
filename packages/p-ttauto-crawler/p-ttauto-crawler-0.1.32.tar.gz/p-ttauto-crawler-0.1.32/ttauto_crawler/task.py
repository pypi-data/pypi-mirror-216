import sys
import os
import time
import requests
import zipfile
import json
from ttauto_crawler import utils
from ttauto_crawler import binary
import shutil
import subprocess
import random
from urllib.parse import *
from PIL import Image
from fake_useragent import UserAgent
import mutagen
from enum import Enum

class C_STATE(Enum):
    WAIT_DOWNLOAD = 0
    DOWNLOADING = 1
    WAIT_TEMPLATE = 2
    TEMPLATEING = 3
    WAIT_UPLOAD = 4
    UPLOADING = 5
    END = 6
    
MAX_DOWNLOADING_COUNT = 2
MAX_PROCESSING_COUNT = 2
MAX_UPLOADING_COUNT = 2

def _configFile():
    thisFileDir = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(thisFileDir, "task.config")
    if os.path.exists(file) == False:
        with open(file, 'w') as f:
            json.dump([], f)
    datas = []
    with open(file, 'r', encoding='UTF-8') as f:
        datas = json.load(f)
    return datas

# task edit
def push(lock, data):
    lock.acquire()
    datas = _configFile()
    data["state"] = C_STATE.WAIT_DOWNLOAD.value
    datas.append(data)
    _saveTask(datas)
    lock.release()

def _saveTask(datas):
    thisFileDir = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(thisFileDir, "task.config")
    with open(file, 'w') as f:
        json.dump(datas, f)

def _getTask(state):
    datas = _configFile()
    for it in datas:
        fff = it["state"]
        if it["state"] == state:
            it["state"] = it["state"] + 1
            _saveTask(datas)
            return it
    return None

def allTaskState(lock):
    lock.acquire()
    datas = _configFile()
    state_list = {
        "task_list": "",
        "wait_downloading": "",
        "downloading": "",
        "wait_processing": "",
        "processing": "",
        "wait_uploading": "",
        "uploading": "",
    }
    for it in datas:
        state_list["task_list"] = state_list["task_list"] + " " + str(it["curGroupId"])
        if it["state"] == C_STATE.WAIT_DOWNLOAD.value:
            state_list["wait_downloading"] = state_list["wait_downloading"] + " " + str(it["curGroupId"])
        if it["state"] == C_STATE.DOWNLOADING.value:
            state_list["downloading"] = state_list["downloading"] + " " + str(it["curGroupId"])
        if it["state"] == C_STATE.WAIT_TEMPLATE.value:
            state_list["wait_processing"] = state_list["wait_processing"] + " " + str(it["curGroupId"])
        if it["state"] == C_STATE.TEMPLATEING.value:
            state_list["processing"] = state_list["processing"] + " " + str(it["curGroupId"])
        if it["state"] == C_STATE.WAIT_UPLOAD.value:
            state_list["wait_uploading"] = state_list["wait_uploading"] + " " + str(it["curGroupId"])
        if it["state"] == C_STATE.UPLOADING.value:
            state_list["uploading"] = state_list["uploading"] + " " + str(it["curGroupId"])
    lock.release()
    return state_list

def _updateTaskToNext(taskItem, state):
    datas = _configFile()
    for it in datas:
        if it["curGroupId"] == taskItem["curGroupId"] and it["state"] == state:
            keys = taskItem.keys()
            for k in keys:
                it[k] = taskItem[k]
            it["state"] = it["state"] + 1
            _saveTask(datas)
            return

# downloading
def canAddDownload(lock):
    lock.acquire()
    c = 0
    datas = _configFile()
    for it in datas:
        if it["state"] <= C_STATE.WAIT_TEMPLATE.value:
            c+=1
    lock.release()
    return c < MAX_DOWNLOADING_COUNT
def popDownload(lock):
    lock.acquire()
    it = _getTask(C_STATE.WAIT_DOWNLOAD.value)
    lock.release()
    return it
def finishDownload(lock, taskItem):
    lock.acquire()
    _updateTaskToNext(taskItem, C_STATE.DOWNLOADING.value)
    lock.release()

# processing
def canTemplate(lock):
    lock.acquire()
    c = 0
    datas = _configFile()
    for it in datas:
        if it["state"] == C_STATE.TEMPLATEING.value:
            c+=1
    lock.release()
    return c < MAX_PROCESSING_COUNT
def popTemplate(lock):
    lock.acquire()
    it = _getTask(C_STATE.WAIT_TEMPLATE.value)
    lock.release()
    return it
def finishTemplate(lock, taskItem):
    lock.acquire()
    _updateTaskToNext(taskItem, C_STATE.TEMPLATEING.value)
    lock.release()
    
# uploading
def canUpload(lock):
    lock.acquire()
    c = 0
    datas = _configFile()
    for it in datas:
        if it["state"] == C_STATE.UPLOADING.value:
            c+=1
    lock.release()
    return c < MAX_UPLOADING_COUNT
def popUpload(lock):
    lock.acquire()
    it = _getTask(C_STATE.WAIT_UPLOAD.value)
    lock.release()
    return it
def finishUpload(lock, taskItem):
    lock.acquire()
    _updateTaskToNext(taskItem, C_STATE.UPLOADING.value)
    _updateEndTask()
    lock.release()

def _updateEndTask():
    datas = _configFile()
    newDatas = []
    for it in datas:
        if it["state"] < C_STATE.END.value:
            newDatas.append(it)
    _saveTask(newDatas)
