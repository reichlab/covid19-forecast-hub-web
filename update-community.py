from zoltpy import util
from zoltpy.connection import ZoltarConnection

import yaml
from datetime import date, datetime, timedelta

res_models = []
team_d = {}
file_name = '_data/community.yml'
conn = util.authenticate()

project_name = 'COVID-19 Forecasts'
project = None

date_format = "%A, %d %B %Y"

props = ['name', 'abbreviation', 'description', 'home_url', 'team_name']
# models = util.print_models(conn, project_name = project_name)
# print(project.models)
base = 'https://zoltardata.com'

def get_public_url(url):
    parts = url.strip('/').split('/')
    resource = parts[-2]
    res_id = parts[-1]
    return '%s/%s/%s' % (base, resource, res_id)

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
    if result['forecasts'] == 0:
        return None
    dates = fetch_forecast_dates(conn, model['forecasts'])
    result['latest_forecast'] = max(dates).strftime(date_format)
    result['earliest_forecast'] = min(dates).strftime(date_format)
    result['dates'] = dates
    result['url'] = get_public_url(model['url'])
    result['actions'] = []
    action = {}
    action['label'] = 'Website'
    # action['type'] = 'primary'
    action['url'] = result['home_url']
    action['new_window'] = True
    # action['new_line'] = True
    result['actions'].append(action)
    result['actions'].append({'label':'Forecast data', 'type':'url', 'url': result['url'], 'new_window': True})
    # print('latest:', max(dates).strftime(date_format))

    return result
    pass


def parse_teams(teams):
    res = []
    for team in teams:
        # print(teams[team][0]['team_name'])
        # print(list(map(lambda x: (date.today() - max(x['dates'])).days, teams[team])))
        max_model = list(filter(lambda x: (date.today() - max(x['dates'])).days < 14 , teams[team]))
        if(len(max_model) > 0):
            max_model = max(max_model, key= lambda x: x['forecasts'])
            res.append(max_model)
        pass
    return res

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
        # break
        # print(conn.json_for_uri(model['url']))
        m = parse_model(model)
        # print(m)
        if m is not None:
            if m['team_name'] not in team_d:
                team_d[m['team_name']] = []
            team_d[m['team_name']].append(m)
        # res_models.append()
    # filter out teams that have no forecasts
    teams_final = list(filter(lambda x: x is not None,parse_teams(team_d)))
    res_models = sorted(parse_teams(team_d), key=lambda x: max(x['dates']), reverse=True)
    
    # write the data to /_data/community.yml
    with open(file_name, 'w') as file:
        documents = yaml.dump(res_models, file)
        print('Generated community file')
    pass

if __name__ == '__main__':
    gen_community()
