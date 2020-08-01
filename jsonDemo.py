import json

with open('ICO_Website_Urls.json', 'r') as f:
    data = json.load(f)
result_list = []
for item in data:
    name = item['ICO name']
    item['ICO name'] = name.replace("\n", "").replace(" ", "")
    url = item['ICO URL']
    item['ICO URL'] = url.replace("https", "http")
    result_list.append(item)
data_str = json.dumps(result_list)
with open('ICO_Website_Urls.json', 'w', encoding='utf-8') as f:
    f.write(data_str)

