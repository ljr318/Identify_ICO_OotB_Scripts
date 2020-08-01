import json
import re

with open('ICO_Website_Urls.json', 'r') as f:
    data = json.load(f)
result_list = []
pattern = re.compile("http://.*?[\/\?]")
for item in data:
    try:
        url = item['ICO URL']
        url = pattern.match(url).group()[:-1]
        item['ICO URL'] = url
        print(url)
        result_list.append(item)
    except Exception as e:
        print(e)

data_str = json.dumps(result_list)
with open('ICO_Sanitized_Urls.json', 'w', encoding='utf-8') as f:
    f.write(data_str)

