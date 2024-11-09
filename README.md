# Game Agent Data Processing

This repository contains code for processing game agent data to generate Question-Answer (QA) pairs. The QA pairs can be used for training AI models, improving game interactions, or enhancing player experiences, Who cares?.(Generated by GPT4o)

## Usage
### Pre
Configure specific prompt of every stage/page for the game in **config/xxx.json** like example.

### generate repeater for resize&crop argumentation
configrate the number for every stage of the game in config/**.json
```
python generate_repeater_config.py
```

### generate sft QA pair for every stage
```
python singlegame_common_point_json
python singlegame_common_none_json
```

### generate eval QA pair
```
python singlegame_eval_point_json
python singlegame_eval_none_json
```