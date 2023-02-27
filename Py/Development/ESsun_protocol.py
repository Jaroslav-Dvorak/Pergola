# import json
#
#
# header = ["Address", "Length", "Name", "WR", "Multiplier", "Unit", "Displayformat", "Symbol", "Min", "Max", "Default", "Remarks"]
# header = {h: i for i, h in enumerate(header)}
#
# with open("EAsun_protocol.json", "r") as f:
#     protocol = f.read()
#     protocol = json.loads(protocol)
#
# print(header)
# print(protocol)
#
# exit()


import pandas as pd
import json

with open("EAsun_protocol.txt", "r", encoding="utf-8") as f:
    raw = f.readlines()

raw = [r.strip() for r in raw]
# print(raw)

par = []
params = []
i = 0
for r in raw:
    par.append(r)

    if i == 7:
        par.append("")
        par.append("")
        par.append("")

    if i == 8:
        params.append(par)
        par = []
        i = 0
        continue
    i += 1

# print(params)
# for p in params:
#     print(p)


with open("EAsun_protocol2.txt", "r", encoding="utf-8") as f:
    raw = f.readlines()

raw = [r.strip() for r in raw]
# print(raw)

par = []
# params = []
i = 0
for r in raw:
    par.append(r)

    if i == 11:
        params.append(par)
        par = []
        i = 0
        continue
    i += 1

# print(params)
# for p in params:
#     print(p)


with open("EAsun_protocol3.txt", "r", encoding="utf-8") as f:
    raw = f.readlines()

raw = [r.strip() for r in raw]
# print(raw)

par = []
# params = []
i = 0
for r in raw:
    par.append(r)
    if i == 5:
        par.append("")

    if i == 10:
        params.append(par)
        par = []
        i = 0
        continue
    i += 1


with open("EAsun_protocol4.txt", "r", encoding="utf-8") as f:
    raw = f.readlines()
raw = [r.strip() for r in raw]

par = []
# params = []
i = 0
for r in raw:
    par.append(r)

    if i == 7:
        par.append("")
        par.append("")
        par.append("")

    if i == 8:
        params.append(par)
        par = []
        i = 0
        continue
    i += 1


# print(params)
for p in params:
    print(str(hex(int(p[0], base=16))))

header = ["Address", "Length", "Name", "WR", "Multiplier", "Unit", "Displayformat", "Symbol", "Min", "Max", "Default", "Remarks"]

df = pd.DataFrame(params)
df.to_csv("EAsun_protocol.csv", header=header, index=False, sep=";")

params = {p[0]: p[1:] for p in params}

for addr, descr in params.items():
    print(addr, descr)


p_json = json.dumps(params, indent=4)
with open("EAsun_protocol.json", "w") as f:
    f.write(p_json)
