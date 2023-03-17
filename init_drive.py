from pathlib import Path

import pandas

from automation.Base import Base

root_name = "自動化"
sites = [
    "なんJ PRIDE",
    "なんJ（まとめては）いかんのか？",
    "なんじぇいスタジアム＠なんJまとめ",
    "MLB NEWS@まとめ",
    "日刊やきう速報",
]
# create local path

root_id = Base().create_driver_directory(root_name)
result = {"name": [], "id": []}
for x in sites:
    Path(f"{root_name}/{x}").mkdir(parents=True, exist_ok=True)
    id = Base().create_driver_directory(x, root_id)
    result["id"].append(id)
    result["name"].append(x)
df = pandas.DataFrame(result)
df.to_csv("drive_info.csv", mode="w", header=True, index=False, encoding="utf-8")
