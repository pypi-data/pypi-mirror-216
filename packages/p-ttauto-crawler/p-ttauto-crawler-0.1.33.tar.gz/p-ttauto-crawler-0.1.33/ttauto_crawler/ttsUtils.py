import os
import random
from urllib.parse import *
from ttauto_crawler import binary
import mutagen
import shutil
import json

def mp3File(dir, k):
    for ext in ["mp3", "wav"]:
        p = os.path.join(dir, f"{k}.{ext}")
        if os.path.exists(p):
            try:
                mutagen.File(p)
            except:
                try:
                    tryMp3 = p.replace(f".{ext}", ".mp3")
                    shutil.copyfile(p, tryMp3)
                    mutagen.File(tryMp3)
                    os.remove(p)
                    p = tryMp3
                except:
                    os.remove(p)
                    print("wav => mp3 fail")
                    return None
            return p
    return None

def lyricFile(dir, k):
    for ext in ["txt", "config", "lyric"]:
        p = os.path.join(dir, f"{k}.{ext}")
        if os.path.exists(p):
            return p

def allTTSKey(searchName, duration):
    ttsDir = binary.ttsPath("")

    addedKey = []
    txt = []
    for root,dirs,files in os.walk(ttsDir):
        if root == ttsDir:
            continue
        k = os.path.basename(root)
        if k != searchName:
            continue
        for file in files:
            name = file[0:file.index(".")]
            if name not in addedKey:
                addedKey.append(name)
                audio = mp3File(root, name)
                if audio:
                    f = mutagen.File(audio)
                    if f.info.length <= duration:
                        txt.append({
                            "lyric": lyricFile(root, name),
                            "audio": audio,
                            "duration": f.info.length
                        })
                    
    return txt
    
def randomTTS(label = "all", duration = 0):
    if len(label) <= 0:
        label = "all"
    tts_list = allTTSKey(label, duration)
    tts_list_len = len(tts_list)
    if tts_list_len > 0:
        rd_idx = random.randint(0, tts_list_len-1)
        k = tts_list[rd_idx]
        with open(k["lyric"], "r", encoding="UTF-8") as f:
            s = f.read()
            lyric = json.loads(str(s).replace("'","\""))
        return lyric, k["audio"], k["duration"]
    return [], None, 0