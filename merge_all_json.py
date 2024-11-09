import glob
import json
import random

mode = "sft"    # sft or eval

# games = ["使命召唤", "和平精英", "穿越火线"]
# json_filename = "zh_PUBGLike_1028_sft.json"

# games = ["英雄联盟", "王者荣耀"]
# json_filename = "ZH_Moba_1031_{}.json".format(mode)

games = ["QQ飞车", "金铲铲", "蛋仔派对"]
json_filename = "zh_qqfc_jcc_dzpd_1107_{}.json".format(mode)

# games = ["开心消消乐", "神庙逃亡2"]
# json_filename = "zh_kxxxl_smtw_1106_{}.json".format(mode)

# games = ["英雄联盟", "王者荣耀", "HonorOfKings", "HonorOfKings_EN", "LOL_WildRift"]
# json_filename = "ZHEN_Moba_1031_{}.json".format(mode)

# games = ["CallOfDuty", "PUBG", "和平精英", "穿越火线", "使命召唤"]
# json_filename = "ZHEN_PUBGlike_1104_{}.json".format(mode)



all_data_list = []

for game in games:
    if mode == "sft":
        json_files = glob.glob("data/{}/*_sft.json".format(game))
    elif mode == "eval":
        json_files = glob.glob("data/{}/EVAL_*.json".format(game))
    json_files.sort()
    # print(len(json_files))

    for json_file in json_files:
        print(json_file)
        with open(json_file,'r', encoding='utf8') as f:
            data_list = json.load(f)
        print(len(data_list))
        all_data_list += data_list
if mode == "sft":
    random.shuffle(all_data_list)
print(len(all_data_list))

with open(json_filename, "w", encoding="utf-8") as f:
    json.dump(all_data_list, f, ensure_ascii=False, indent=4)