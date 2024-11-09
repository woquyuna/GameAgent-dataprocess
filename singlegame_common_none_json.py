import os
import glob
import json
import copy
import cv2
from utils.argument import img_argument_center
from utils.utils import parse_action,parse_game_config
from prompt.prompts import default_Q_prompts

config_path = "config/ZH_wzry.json"  

config = parse_game_config(config_path)  # main config
repeat_config = parse_game_config("/data/hjj/game/data_clean/all_game_config_1028.json") # sample repeater

game = config["data_root_path"]     # path
full_game = config["full_game"]     # full game name in prompt
intent = config.get("intent", "")

sub_stage_dicts = config["stages"]   # all stages

for sub_stage in sub_stage_dicts.keys():
    
    sub_stage_dict = sub_stage_dicts[sub_stage]
    if sub_stage_dict["action_type"] != "None":
        print("{} type is {}, not None\n".format(os.path.join(game, "raw", sub_stage), sub_stage_dict["action_type"]))
        continue
    en_stage = sub_stage_dict["en_stage"]
    button = sub_stage_dict["button"]
    language = config.get("language", None)
    if not language:
        repeat = repeat_config[full_game][sub_stage]
    else:
        repeat = repeat_config[full_game+" "+language][sub_stage]
    
    Q_prompt = default_Q_prompts
    Q_template = {"role":"user",
                "content": Q_prompt.format(full_game, intent)}
    
    A_prompt = """1.{}\n2.{}""".format(sub_stage_dict["answer_status"], sub_stage_dict["answer_action"])
    A_template = {"role":"assistant",
                "content": A_prompt}

    train_images = glob.glob(os.path.join(game, 'raw', sub_stage, "*.jpg"))

    dump_data_list = []
    glob_idx = 0

    for r in range(repeat):
        for i,raw in enumerate(train_images):
            glob_idx += 1
            dump_data = {"id":"{}_{}_{}".format(game, sub_stage, glob_idx)}
            
            img, _, _ = img_argument_center(train_images[i], 0.5, 0.5)

            output_dir = os.path.join(game, "argue")
            os.makedirs(output_dir, exist_ok=True)
            image_filename = f"{en_stage}_global{glob_idx}_" + os.path.basename(train_images[i])
            cv2.imencode('.jpg', img)[1].tofile(os.path.join(output_dir, image_filename))

            # 将图像路径保存到 dump_data 中
            dump_data["image"] = os.path.join(output_dir, image_filename)
            
            qt = copy.deepcopy(Q_template)     # question template
            at = copy.deepcopy(A_template)       # answer template
            
            msgs = [qt, at]
            dump_data["conversations"] = msgs
            dump_data_list.append(dump_data)
    print(os.path.join(game, 'raw', sub_stage))
    print("Number of cases:{}\n".format(len(dump_data_list)))

    json_filename = "{}_{}_sft.json".format(os.path.basename(game), sub_stage)
    with open(os.path.join(game, json_filename), "w", encoding="utf-8") as f:
        json.dump(dump_data_list, f, ensure_ascii=False, indent=4)




            