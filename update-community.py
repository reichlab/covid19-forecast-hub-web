from datetime import date

import yaml
from zoltpy import util


FILE_NAME = '_data/community.yml'
PROJECT_NAME = 'COVID-19 Forecasts'
DATE_FORMAT = "%A, %d %B %Y"
ZOLTAR_HOST_URL = 'https://zoltardata.com'
DAYS_OLD = 16


def get_public_url(url):
    parts = url.strip('/').split('/')
    resource = parts[-2]
    res_id = parts[-1]
    return '%s/%s/%s' % (ZOLTAR_HOST_URL, resource, res_id)


def parse_model(model):
    """
    Example return value:

    {'name': 'DELPHI',
     'abbreviation': 'CovidAnalytics-DELPHI',
     'description': 'This model predicts based on an SEIR model augmented with underdetection and interventions. ... ',
     'home_url': 'https://www.covidanalytics.io/',
     'team_name': 'CovidAnalytics at MIT',
     'forecasts': 116,
     'latest_forecast': 'Monday, 04 July 2022',
     'earliest_forecast': 'Wednesday, 22 April 2020',
     'dates': [datetime.date(2021, 3, 29), datetime.date(2020, 4, 22), ..., datetime.date(2022, 5, 30)],
     'url': 'https://zoltardata.com/model/196',
     'actions': [{'label': 'Website', 'url': 'https://www.covidanalytics.io/', 'new_window': True},
                 {'label': 'Forecast data', 'type': 'url', 'url': 'https://zoltardata.com/model/196', 'new_window': True}]}
    """
    result = {'name': model.json['name'], 'abbreviation': model.json['abbreviation'],
              'description': model.json['description'], 'home_url': model.json['home_url'],
              'team_name': model.json['team_name'], 'forecasts': len(model.json['forecasts'])}

    if result['forecasts'] == 0:
        return None

    dates = [forecast.timezero.timezero_date for forecast in model.forecasts]  # one query
    result['latest_forecast'] = max(dates).strftime(DATE_FORMAT)
    result['earliest_forecast'] = min(dates).strftime(DATE_FORMAT)
    result['dates'] = dates
    result['url'] = get_public_url(model.json['url'])
    result['actions'] = [{'label': 'Website', 'url': result['home_url'], 'new_window': True},
                         {'label': 'Forecast data', 'type': 'url', 'url': result['url'], 'new_window': True}]
    return result


def parse_teams(teams):
    res = []
    for team in teams:
        max_model = list(filter(lambda _: (date.today() - max(_['dates'])).days < DAYS_OLD, teams[team]))
        if max_model:
            max_model = max(max_model, key=lambda _: _['forecasts'])
            res.append(max_model)
    return res


def gen_community():
    # get project
    conn = util.authenticate()
    projects = [project for project in conn.projects if project.name == PROJECT_NAME]
    if len(projects) != 1:
        raise RuntimeError(f"did not find the project. name={PROJECT_NAME!r}, projects={projects}")

    project = projects[0]

    # get model and convert it to a dictionary
    team_d = {}
    for model in project.models:
        model = parse_model(model)
        if model is not None:
            if model['team_name'] not in team_d:
                team_d[model['team_name']] = []
            team_d[model['team_name']].append(model)

    # write the data to /_data/community.yml
    res_models = sorted(parse_teams(team_d), key=lambda x: max(x['dates']), reverse=True)
    with open(FILE_NAME, 'w') as file:
        yaml.dump(res_models, file)


if __name__ == '__main__':
    gen_community()
