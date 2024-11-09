import json


def parse_game_config(path="/data/hjj/game/data_clean/all_game_config_1024.json"):
    with open(path, 'r', encoding='utf8') as f:
        data = json.load(f)
    return data


def parse_action(jsonfile):
    with open(jsonfile, 'r', encoding='utf8') as f:
            raw_data = json.loads(f.read())
        
    action = raw_data["actions"][0]["action"]
        
    if isinstance(action, list):
        action = action[0]
    
    return raw_data, action