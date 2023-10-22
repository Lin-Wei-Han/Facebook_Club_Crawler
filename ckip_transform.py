from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger
import pandas as pd
import json
import re

ws_driver = CkipWordSegmenter(model="albert-base")
pos_driver = CkipPosTagger(model="albert-base")

def process_article(article):
    if not article:
        return ""
    ws = ws_driver([article])
    pos = pos_driver(ws)

    short_sentence = []
    stop_words = set(["一點", "分鐘", "更多",'什麼','之外','好幾'])
    for sentence_ws, sentence_pos in zip(ws, pos):
        for word_ws, word_pos in zip(sentence_ws, sentence_pos):
            is_N_or_V = word_pos.startswith("N")
            word_length_limit = len(word_ws) > 1
            if word_ws in stop_words: continue
            if is_N_or_V and word_length_limit:
                short_sentence.append(word_ws)
    # 回傳斷詞後的結果
    return " ".join(short_sentence)


# 斷詞斷句

with open('data/club_posts.json', 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

dataset = pd.DataFrame(json_data)
dataset["article"].fillna("", inplace=True)
dataset["seg_result"] = dataset["article"].apply(lambda x: re.sub("[^\w\s\(\)\*\+\?\.\|]", "", str(x)))

# 分塊執行
chunk_size = 600 
chunks = [dataset[i:i + chunk_size] for i in range(0, len(dataset), chunk_size)]

seg_contents = []
for chunk in chunks:
    seg_result = chunk["seg_result"].apply(process_article)
    seg_contents.append(seg_result)

combined_seg_content = pd.concat(seg_contents)

# Output

with open('data/club_posts.json', 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

for index, row in combined_seg_content.items():
    if pd.isna(row):
        row = ""
    json_data[index].update({"word": row})

with open('data/club_posts.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)