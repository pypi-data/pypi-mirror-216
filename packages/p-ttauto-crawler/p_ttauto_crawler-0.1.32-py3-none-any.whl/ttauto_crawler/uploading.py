import sys
import os
import time
import requests
import zipfile
import json
from ttauto_crawler import utils
from urllib.parse import *

splitZipCount = 200

def curOutputDir(curGroupId):
    s = os.path.join(utils.largeDiskPath(), ".out", str(curGroupId))
    if os.path.exists(s) == False:
        os.makedirs(s)
    return s
    
def notifyMessage(curGroupId, ossurl, count):
    try:
        param = {
            "id": curGroupId,
            "video_path": ossurl,
            "video_num": count
        }
        s = requests.session()
        s.headers.update({'Connection':'close'})
        res = s.post(f"https://beta.2tianxin.com/common/admin/tta/set_task_complete", json.dumps(param), verify=False)
        if res.status_code == 200:
            utils.logInfo(f"notifyMessage success", True)
        else:
            resContext = res.content.decode(encoding="utf8", errors="ignore")
            utils.logInfo(f"notifyMessage fail! code={res.status_code}, context={resContext}", True)
            utils.logInfo(f"report error!, postdata = {json.dumps(param)}", True)
        s.close()
    except Exception as e:
        utils.logInfo(f"notifyMessage exception :{e}", True)

def upload(processed_dir, curGroupId):
    successCount = 0
    splitCount = 0
    packageIndex = 0
    dist = os.path.join(os.path.dirname(processed_dir), f"{curGroupId}_{packageIndex}.zip")
    zip = zipfile.ZipFile(dist, "w", zipfile.ZIP_DEFLATED) 
    for rt,dirs,files in os.walk(processed_dir):
        for file in files:
            if str(file).startswith("~$"):
                continue
            filepath = os.path.join(rt, file)
            if os.stat(filepath).st_size < 250000:
                #recheck upload file size , must be large than 250k
                continue
            writepath = os.path.relpath(filepath, processed_dir)
            zip.write(filepath, writepath)
            splitCount+=1
            successCount+=1
            if splitCount >= splitZipCount and (len(files) - successCount > (splitZipCount / 2)):
                zip.close()
                onePackage_ossurl = utils.ftpUpload(dist)[0]
                utils.logInfo(f"=== sending {packageIndex} package ", True)
                notifyMessage(curGroupId, onePackage_ossurl, splitCount)
                packageIndex+=1
                splitCount = 0
                os.remove(dist)
                dist = os.path.join(os.path.dirname(processed_dir), f"{curGroupId}_{packageIndex}.zip")
                zip = zipfile.ZipFile(dist, "w", zipfile.ZIP_DEFLATED)
        if rt != files:
            break
    zip.close()
    if splitCount > 0:
        lastPackage_ossurl = utils.ftpUpload(dist)[0]
        utils.logInfo(f"=== sending last package ", True)
        notifyMessage(curGroupId, lastPackage_ossurl, splitCount)
        os.remove(dist)
    return successCount
