import cv2
import os
import glob
import json
from PIL import Image, ImageDraw, ImageFont
import numpy as np


src_root = r"./"

actions = glob.glob(os.path.join(src_root, "*_action.json"))
imgs = glob.glob(os.path.join(src_root, "*_screen.jpg"))

actions.sort()
imgs.sort()

assert len(actions)==len(imgs),"json数量需要与图片数量一致"

for i in range(len(imgs)):
    img = cv2.imdecode(np.fromfile(imgs[i],dtype=np.uint8),-1)
    H,W = img.shape[:2]
    print(H,W)
    action = actions[i]
    with open(action, 'r', encoding='utf8') as f:
        data = json.load(f)
    
    if isinstance(data["actions"], list):
        data = data["actions"][0]
        # label_text = data["actions"][0]["hand"] + " " + data["actions"][0]["action"]
    else:
        data = data["actions"]
        # label_text = data["actions"]["hand"] + " " + data["actions"]["action"]
    if isinstance(data["action"], list):
        label_text = data["hand"] + " " + data["action"][0]
    else:
        label_text = data["hand"] + " " + data["action"]
    
    if "coordinates" in data.keys():
        x = W * data["coordinates"]["rx"]
        y = H * data["coordinates"]["ry"]

        cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
        
        img = Image.fromarray(img)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(r'D:\SIMHEI.TTF', 25)
        draw.text((int(x+5), int(y)), label_text, fill=(0, 0, 255), font=font)
        
        img = np.array(img)
        
        # print(os.path.join(outdir, os.path.basename(imgs[i])))
    new_name = os.path.basename(imgs[i]).replace(".jpg", "_plot.jpg")
    cv2.imencode('.jpg', img)[1].tofile(new_name)

