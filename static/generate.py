import json
from rich import inspect,print
import re

with open("./static/source.txt", "r", encoding="utf-8") as f:
    data = f.read()

data = data.split("\n\n")

inspect(data)

o = []
for i in range(len(data)):
    print(f"Processing {i}/{len(data)}")
    t = {
        "id": i,
        "text": data[i],
        "author": data[i].split("\n")[0].split(" ")[0],
        "name": data[i].split("\n")[0].split(" ")[1],
        "cut": list(map(lambda x: re.split(r"([，。！？;；])",x),data[i].split("\n")[1:])),
        }
#    inspect(t)
    o.append(t)

with open("./static/preset-text.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(o, ensure_ascii=False))