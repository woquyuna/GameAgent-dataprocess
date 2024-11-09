import os
import glob
import json
import copy
import cv2
import numpy as np
from utils.utils import parse_action,parse_game_config
from prompt.prompts import default_Q_prompts

config_path = "config/ZH_wzry.json"   

config = parse_game_config(config_path)  # main config
# repeat_config = parse_game_config("/data/hjj/game/data_clean/all_game_config_1028.json") # sample repeater

game = config["data_root_path"]     # path
full_game = config["full_game"]     # full game name in prompt
intent = config.get("intent", "")

sub_stage_dicts = config["stages"]   # all stages

for sub_stage in sub_stage_dicts.keys():
    
    sub_stage_dict = sub_stage_dicts[sub_stage]
    if sub_stage_dict["action_type"] != "point":
        print("{} type is {}, not point\n".format(os.path.join(game, "raw", sub_stage), sub_stage_dict["action_type"]))
        continue
    en_stage = sub_stage_dict["en_stage"]
    button = sub_stage_dict["button"]
    repeat = 1
    
    Q_prompt = default_Q_prompts
    Q_template = {"role":"user",
                "content": Q_prompt.format(full_game, intent)}
    
    A_prompt = """1.{}\n2.{}""".format(sub_stage_dict["answer_status"], sub_stage_dict["answer_action"])
    A_template = {"role":"assistant",
                "content": A_prompt}

    train_images = glob.glob(os.path.join(game, 'raw', sub_stage, "*_screen.jpg"))
    train_jsons = glob.glob(os.path.join(game, 'raw', sub_stage, "*_action.json"))
    
    train_images.sort()
    train_jsons.sort()
    

    dump_data_list = []
    glob_idx = 0

    for r in range(repeat):
        for i,raw in enumerate(train_jsons):
            glob_idx += 1
            dump_data = {"id":"eval_{}_{}_{}".format(game, sub_stage, glob_idx)}
            
            raw_data, action = parse_action(train_jsons[i])
            
            label = f"<ref>{button}</ref>" 
            rx = raw_data["actions"][0]["coordinates"]["rx"]
            ry = raw_data["actions"][0]["coordinates"]["ry"]
            
            # print(train_images[i])
            img = cv2.imdecode(np.fromfile(train_images[i],dtype=np.uint8),-1)
            H,W = img.shape[:2]
            
            if W > H:   # horizon
                if W > 1200:
                    img = cv2.resize(img, (round(1200*H/W), 1200), interpolation=cv2.INTER_LINEAR)
            else:        # vertical
                if H > 925:
                    img = cv2.resize(img, (925, round(925*W/H)), interpolation=cv2.INTER_LINEAR)
            
            rx = int(rx * 1000)
            ry = int(ry * 1000)
            coord = "<point>{} {}</point>".format(rx, ry)

            output_dir = os.path.join(game, "eval")
            os.makedirs(output_dir, exist_ok=True)
            image_filename = f"{en_stage}_global{glob_idx}_" + os.path.basename(train_images[i])
            cv2.imencode('.jpg', img)[1].tofile(os.path.join(output_dir, image_filename))

            dump_data["image"] = os.path.join(output_dir, image_filename)
            
            qt = copy.deepcopy(Q_template)     # question template
            at = copy.deepcopy(A_template)       # answer template
            at["content"] = at["content"].format(label, coord)
            
            msgs = [qt, at]
            dump_data["conversations"] = msgs
            dump_data_list.append(dump_data)
    print(os.path.join(game, "raw", sub_stage))
    print("Number of cases:{}\n".format(len(dump_data_list)))

    json_filename = "EVAL_{}_{}.json".format(os.path.basename(game), sub_stage)
    with open(os.path.join(game, json_filename), "w", encoding="utf-8") as f:
        json.dump(dump_data_list, f, ensure_ascii=False, indent=4)




            