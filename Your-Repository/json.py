#exercise 1 

import json

FILE_NAME = "sample-data1.json"

with open(FILE_NAME, "r", encoding="utf-8") as f:
    data = json.load(f)

interfaces = data.get("imdata", [])

title = "Interface Status"
col1 = "DN"
col2 = "Description"
col3 = "Speed"
col4 = "MTU"

rows = []
for item in interfaces:
    attrs = item.get("l1PhysIf", {}).get("attributes", {})
    dn = attrs.get("dn", "")
    descr = attrs.get("descr", "")
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")
    rows.append((dn, descr, speed, mtu))


dn_width = max(len(col1), max((len(r[0]) for r in rows), default=0))
descr_width = max(len(col2), max((len(r[1]) for r in rows), default=0))
speed_width = max(len(col3), max((len(r[2]) for r in rows), default=0))
mtu_width = max(len(col4), max((len(r[3]) for r in rows), default=0))


print(title)
print("=" * (dn_width + descr_width + speed_width + mtu_width + 9))
print(f"{col1:<{dn_width}}  {col2:<{descr_width}}  {col3:<{speed_width}}  {col4:<{mtu_width}}")
print(f"{'-' * dn_width}  {'-' * descr_width}  {'-' * speed_width}  {'-' * mtu_width}")

for dn, descr, speed, mtu in rows:
    print(f"{dn:<{dn_width}}  {descr:<{descr_width}}  {speed:<{speed_width}}  {mtu:<{mtu_width}}")











x = '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y["age"])


""" 
You can convert Python objects of the following types, into JSON strings:

dict
list
tuple
string
int
float
True
False
None 
"""

""" Convert Python objects into JSON strings, and print the values: """

print(json.dumps({"name": "John", "age": 30}))
print(json.dumps(["apple", "bananas"]))

