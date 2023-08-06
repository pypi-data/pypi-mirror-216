import sys
import os
import subprocess
import json
import random
from pathlib import Path
import shutil
import zipfile
import stat
import requests
import hashlib
import logging
from ttauto_crawler import utils

def getOssResource(rootDir, url, md5, name):
    localFile = os.path.join(rootDir, name)
    localFileIsRemote = False
    if os.path.exists(localFile):
        with open(localFile, 'rb') as fp:
            file_data = fp.read()
            fp.close()
        file_md5 = hashlib.md5(file_data).hexdigest()
        if file_md5 == md5:
            localFileIsRemote = True

    if localFileIsRemote == False: #download
        if os.path.exists(localFile):
            os.remove(localFile)
        s = requests.session()
        s.keep_alive = False
        utils.logInfo(f"download {url} ")
        file = s.get(url, verify=False)
        with open(localFile, "wb") as c:
            c.write(file.content)
            c.close()
        s.close()
        fname = name[0:name.index(".")]
        fext = name[name.index("."):]
        unzipDir = os.path.join(rootDir, fname)
        if os.path.exists(unzipDir):
            shutil.rmtree(unzipDir)
        utils.logInfo(f"unzip {url} -> {unzipDir}")

def readDirChecksum(dir):
    f = os.path.join(dir, "checksum.txt")
    txt = ""
    if os.path.exists(f):
        with open(f, "r", encoding="UTF-8") as f1:
            txt = f1.read()
            f1.close()
    return txt
        
def writeDirChecksum(dir, zipFile):
    if os.path.exists(zipFile) == False:
        return
    with open(zipFile, 'rb') as fp:
        fdata = fp.read()
        fp.close()
    fmd5 = hashlib.md5(fdata).hexdigest()

    with open(os.path.join(dir, "checksum.txt"), "w") as f:
        f.write(fmd5)
        f.close()

def checkFileMd5(rootDir):
    data = {
    }
    for key in data:
        fpath = os.path.join(rootDir, key)
        if os.path.exists(fpath):
            with open(fpath, 'rb') as fp:
                fdata = fp.read()
                fp.close()
            fmd5 = hashlib.md5(fdata).hexdigest()
            fname = key[0:key.index(".")]
            fext = key[key.index("."):]
            fdirpath = os.path.join(rootDir, fname)
            if os.path.exists(fdirpath) and fmd5 != readDirChecksum(fdirpath):
                utils.logInfo(f"remove old {fdirpath}")
                shutil.rmtree(fdirpath)
        
def updateBin(rootDir):
    getOssResource(rootDir, "https://m.mecordai.com/res/ffmpeg.zip", "a9e6b05ac70f6416d5629c07793b4fcf", "ffmpeg.zip.py")
    getOssResource(rootDir, "https://m.mecordai.com/res/tts_20230621.zip", "0e994d11cb66bd961ca215e0e2f4b137", "tts.zip.py")
    getOssResource(rootDir, "https://m.mecordai.com/res/music-cn_20230426.zip", "205e90cf47eb0587f4ac0cf05d0f30a7", "music-cn.zip.py")
    checkFileMd5(rootDir)

    for root,dirs,files in os.walk(rootDir):
        for file in files:
            if file.find(".") <= 0:
                continue
            name = file[0:file.index(".")]
            ext = file[file.index("."):]
            if ext == ".zip.py" and os.path.exists(os.path.join(root, name)) == False:
                utils.logInfo(f"unzip {os.path.join(root, name)}")
                with zipfile.ZipFile(os.path.join(root, file), "r") as zipf:
                    zipf.extractall(os.path.join(root, name))
                writeDirChecksum(os.path.join(root, name), os.path.join(root, file))
        if root != files:
            break

def realBinPath(searchPath):
    binDir = ""
    if len(searchPath) <= 0 or os.path.exists(searchPath) == False:
        binDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
        updateBin(binDir)
    else:
        binDir = searchPath
    return binDir

def ffmpegPath(searchPath):
    return os.path.join(realBinPath(searchPath), "ffmpeg")
def musicPath(searchPath):
    return os.path.join(realBinPath(searchPath), "music-cn")
def ttsPath(searchPath):
    return os.path.join(realBinPath(searchPath), "tts")