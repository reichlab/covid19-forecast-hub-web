from zoltpy import util
from zoltpy.connection import ZoltarConnection

import yaml

res_models = []
file_name = '_data/community.yml'
conn = util.authenticate()

project_name = 'COVID-19 Forecasts'
project = None

props = ['name', 'abbreviation', 'description', 'home_url']
# models = util.print_models(conn, project_name = project_name)
# print(project.models)

def parse_model(model):
    result = {}
    for prop in props:
        result[prop] = model[prop]
    return result
    pass

def gen_community():
    # find project
    for proj in conn.projects:
        if proj.name == project_name:
            project = proj
            break
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
