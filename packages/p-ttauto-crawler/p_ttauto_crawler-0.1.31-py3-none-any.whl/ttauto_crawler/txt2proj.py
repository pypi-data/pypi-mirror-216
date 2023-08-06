import sys
import os
import time
import requests
import zipfile
import json
from ttauto_crawler import utils
from ttauto_crawler import binary
from ttauto_crawler import ttsUtils
import logging
import urllib3
import datetime
import shutil
import subprocess
import random
from urllib.parse import *
from PIL import Image
from fake_useragent import UserAgent
from template_generator import template as genertor_template
import uuid
import calendar
import hashlib
import mutagen
import math

def randomMusicPath(minLen):
    musicDir = binary.musicPath("")
    s = []
    for root,dirs,files in os.walk(musicDir):
        for file in files:
            if file.find(".") <= 0:
                continue
            name = file[0:file.index(".")].lower()
            ext = file[file.index("."):].lower()
            if ext in [".mp3",".aac",".wav",".wma",".cda",".flac",".m4a",".mid",".mka",".mp2",".mpa",".mpc",".ape",".ofr",".ogg",".ra",".wv",".tta",".ac3",".dts"]:
                audioPath = os.path.join(root, file)
                f = mutagen.File(audioPath)
                if f.info.length > minLen:
                    s.append(audioPath)
        if root != files:
            break
    if len(s) <= 0:
        raise Exception("music not found!")
    rd_idx = random.randint(0,len(s)-1)
    tmp_s = s[rd_idx]
    return tmp_s

def genTemplate(config):
    rdx = random.randint(100,99999999)
    inputArgs = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"genTemplate_{rdx}.in")
    if os.path.exists(inputArgs):
        os.remove(inputArgs)
    with open(inputArgs, 'w') as f:
        json.dump(config, f)
        
    outputDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"genTemplate_{rdx}")
    if os.path.exists(outputDir):
        shutil.rmtree(outputDir)
    os.makedirs(outputDir)

    try:
        genertor_template.generateTemplate(inputArgs, outputDir, "")
    except subprocess.CalledProcessError as e:
        shutil.rmtree(outputDir)
        raise e
    finally:
        os.remove(inputArgs)
    return outputDir

def firstSkyFile(rootDir):
    if len(rootDir) > 0:
        for root,dirs,files in os.walk(rootDir):
            for file in files:
                if file.find(".") <= 0:
                    continue
                ext = file[file.index("."):]
                if ext == ".sky":
                    return os.path.join(root, file)
            if root != files:
                break
    return ""

def txtConfig(txt, w, h, start, duration):
    txt_idx = 0
    # txt_fontsize = 6
    # txt_positonX_offset = random.random() * 0.1
    # txt_threshold = math.ceil(w / (min([w,h]) * ((txt_fontsize*1.6)/100)))
    # while txt_idx*10 < len(txt):
    #     txt = f"{txt[0:(txt_idx+1)*txt_threshold]}\n{txt[(txt_idx+1)*txt_threshold:]}"
    #     txt_idx += 1
    # txt_position_y = random.random() * 0.6 + 0.2 - 0.5
    txt_fontsize = 3
    txt_positonX_offset = 0
    txt_threshold = math.ceil(w / (min([w,h]) * ((txt_fontsize*1.6)/100)))
    while txt_idx*10 < len(txt):
        txt = f"{txt[0:(txt_idx+1)*txt_threshold]}\n{txt[(txt_idx+1)*txt_threshold:]}"
        txt_idx += 1
    txt_position_y = 0.7
    return {
                "res":txt,
                "type":"text",
                "startTime":start,
                "duration":duration,
                "positionType":"relative",
                "positionX":txt_positonX_offset,
                "positionY":txt_position_y,
                "params": {
                    "textColor":"#ffffffff",
                    "stroke":1,
                    "alignment":0,
                    "fontSize":txt_fontsize
                }
            }

def newTemplateWithText(template, w, h, duration, tag):
    skyFile = firstSkyFile(template)
    lyric, mp3, mp3_duration = ttsUtils.randomTTS(tag, duration)
    
    config = {
        "layer": [
            [ ],
            [ ]
        ]
    }
    for it in lyric:
        config["layer"][0].append(txtConfig(it["text"], w, h, float(it["start"]), float(it["end"])))
    if mp3:
        config["layer"][1].append({
            "res":mp3,
            "type":"audio",
            "startTime":0,
            "duration":mp3_duration,
            "params": {  
                "volume": 1
            }
        })
    if len(skyFile) > 0:
        config["template"] = skyFile
    else:
        config["width"] = w
        config["height"] = h
    newTemplateDir = genTemplate(config)
    if os.path.exists(newTemplateDir) == False:
        return ""
    return newTemplateDir

def singleVideoToTemplate(s, addRandomText, w, h, duration, tag):
    txtLayer = []
    otherLayer = []
    imgLayer = []
    start_pts = 0
    if addRandomText:
        lyric, mp3, mp3_duration = ttsUtils.randomTTS(tag, duration)
        for it in lyric:
            txtLayer.append(txtConfig(it["text"], w, h, float(it["start"]), float(it["end"])))
        if mp3:
            otherLayer.append({
                "res":mp3,
                "type":"audio",
                "startTime":0,
                "duration":mp3_duration,
                "params": {  
                    "volume": 1
                }
            })
    vit = {
        "res":s,
        "type":"video",
        "startTime":start_pts,
        "duration":duration,
        "positionType":"relative",
        "positionX":0,
        "positionY":0,
        "params": {  
            "volume": 1 if len(otherLayer) == 0 else 0.1
        }
    }
    imgLayer.append(vit)
    config = {
        "width": int(w),
        "height": int(h),
        "layer": [
            imgLayer,
            txtLayer,
            otherLayer
        ]
    }
    templateDir = genTemplate(config)
    return templateDir

def imgsToTemplate(s1, addRandomText, tag):
    firstImage = s1[0]
    img = Image.open(firstImage)
    txtLayer = []
    imgLayer = []
    start_pts = 0
    transtion_duration = 1.0
    duration_pts = 3
    all_transition = [-1,-1,-1,-1,13,31,32,38]
    rd_transition = all_transition[random.randint(0, len(all_transition)-1)]
    for i in range(len(s1)):
        vit = {
            "res":s1[i],
            "type":"video",
            "startTime":start_pts,
            "duration":duration_pts,
            "positionType":"relative",
            "positionX":0,
            "positionY":0,
            "params": {
                "width":img.width,
                "height":img.height
            }
        }
        if start_pts > 0 and rd_transition >= 0:
            vit["params"]["transition"] = "random"
            vit["params"]["transitionParam"] = {
                "0:SubTransition": rd_transition
            }
            vit["params"]["transitionDuration"] = transtion_duration
        imgLayer.append(vit)
        # if i < len(txts) and addRandomText:
        #     txt = txts[i]
        #     tit = txtConfig(txt, img.width, img.height, duration_pts)
        #     if i == len(s1)-1:
        #         tit["startTime"] = tit["startTime"] - (i-1)*transtion_duration
        #         tit["duration"] = tit["duration"] - transtion_duration
        #     elif i > 0:
        #         tit["startTime"] = tit["startTime"] - (i-1)*transtion_duration
        #         tit["duration"] = tit["duration"] - 2*transtion_duration
        #     txtLayer.append(tit)
        start_pts += duration_pts
    musicLayer = []
    otherLayer = []
    if addRandomText:
        lyric, mp3, mp3_duration = ttsUtils.randomTTS(tag, start_pts)
        for it in lyric:
            txtLayer.append(txtConfig(it["text"], img.width, img.height, float(it["start"]), float(it["end"])-float(it["start"])))
        if mp3:
            otherLayer.append({
                "res":mp3,
                "type":"audio",
                "startTime":0,
                "duration":mp3_duration,
                "params": {  
                    "volume": 1
                }
            })
    musicLayer.append({
            "res":randomMusicPath(start_pts),
            "type":"audio",
            "startTime":0,
            "duration":start_pts,
            "params": {  
                "volume": 1 if len(otherLayer) == 0 else 0.1
            }
        })
    config = {
        "width": img.width,
        "height": img.height,
        "layer": [
            imgLayer,
            txtLayer,
            musicLayer,
            otherLayer
        ]
    }
    templateDir = genTemplate(config)
    return templateDir

def randomImageCntToVideo(dir, cnt):
    s = []
    for root,dirs,files in os.walk(dir):
        for file in files:
            if file.find(".") <= 0:
                continue
            name = file[0:file.index(".")].lower()
            ext = file[file.index("."):].lower()
            if ext in [".jpg", ".png", ".jpeg", ".bmp"]:
                s.append(os.path.join(root, file))
        if root != files:
            break
    templates = []
    while len(s) > cnt:
        s1 = []
        allcnt = len(s)
        for i in range(cnt):
            rd_idx = random.randint(0, allcnt-1)
            tmp_s = s[rd_idx]
            s.remove(tmp_s)
            allcnt -= 1
            s1.append(tmp_s)
        templates.append(imgsToTemplate(s1), True)
        
    data = []
    idx = 0
    outDir = os.path.join(dir, "out")
    if os.path.exists(outDir):
        shutil.rmtree(outDir)
    os.makedirs(outDir)

    for tp in templates:
        data.append({
                "input":[],
                "template": tp,
                "params":{},
                "output": os.path.join(outDir, f"out_{idx}.mp4")})
        idx+=1
    try:
        genertor_template.executeTemplate(data, "")
        utils.logInfo("=== process success", True) 
    except subprocess.CalledProcessError as e:
        utils.logInfo("====================== process error ======================", True)
        utils.logInfo(e)
        utils.logInfo("======================      end      ======================")
    finally:
        for tp in templates:
            shutil.rmtree(tp)
        
# randomImageCntToVideo("E:\ins1", 3)