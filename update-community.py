from zoltpy import util
from zoltpy.connection import ZoltarConnection

import yaml
from datetime import date

res_models = []
file_name = '_data/community.yml'
conn = util.authenticate()

project_name = 'COVID-19 Forecasts'
project = None

date_format = "%A, %d %B %Y"

props = ['name', 'abbreviation', 'description', 'home_url', 'url']
# models = util.print_models(conn, project_name = project_name)
# print(project.models)


def fetch_forecast_dates(con, forecasts):
    dates = []
    for f in forecasts:
        dates.append(date.fromisoformat(con.json_for_uri(f)['time_zero']['timezero_date']))
    return dates
    pass

def parse_model(model):
    result = {}
    for prop in props:
        result[prop] = model[prop]
    result['forecasts'] = len(model['forecasts'])
    dates = fetch_forecast_dates(conn, model['forecasts'])
    result['latest_forecast'] = max(dates).strftime(date_format)
    result['earliest_forecast'] = min(dates).strftime(date_format)
    result['actions'] = []
    action = {}
    action['label'] = 'Website'
    action['type'] = 'primary'
    action['url'] = result['url']
    result['actions'].append(action)
    # print('latest:', max(dates).strftime(date_format))

    return result
    pass

def gen_community():
    # find project
    for proj in conn.projects:
        if proj.name == project_name:
            project = proj
            break
    # print(project.json)
    # get model json and parse it to a dictionary
    for m in project.models:
        model = m.json
        # print(model)
        # print(conn.json_for_uri(model['url']))
        res_models.append(parse_model(model))
    
    # write the data to /_data/community.yml
    with open(file_name, 'w') as file:
        documents = yaml.dump(res_models, file)
        print('Generated community file')
    pass

if __name__ == '__main__':
    gen_community()
