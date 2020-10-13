import glob
import json
import re

regexp = re.compile(r'^[\d]+\-[\d]+\-[\d]+$')

reps = glob.glob("reports/*-weekly-report.html")
result = {}
# print(reps)
for rep in reps:
    rep = rep.split('/')[-1]
    parts = rep.split('.')[0].split('-')
    print(rep, '-'.join(parts[:3]))
    if len(parts) < 5:
        continue
    if not regexp.search('-'.join(parts[:3])):
        continue
    date = '-'.join(parts[:3])
    if len(parts)==5:
        state="national"
    elif len(parts)==6:
        state = parts[3]
    else:
        continue
    if state not in result:
        result[state] = []
    result[state].append(date)

json.dump(result, open("reports/reports.json", "w"))