"""
JAC - jdechalendar@stanford.edu
"""
import os
import json
from . import GLMparser

config = {}
config['UPLOAD_FOLDER'] = 'uploads'
fixed_nodes_json_file = 'fixed_nodes.json'
graph_json_file = 'graph.json'


def get_glm_file_name(session):
    return session['glm_name'] if 'glm_name' in session else None


def getCsvFile():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),                         config['UPLOAD_FOLDER'], "curr.csv")


def getGlmFile():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),                         config['UPLOAD_FOLDER'], "ll
                        .glm")


def getDefaultGlmName():
    return ''


def getDefaultFixedNodesJson():
    return json.loads('{"names":[], "x":[], "y":[]}')


def getDefaultGraphJson():
    return json.loads('{"nodes":[],"links":[]}')


def renderMain(method, files, glm_name):
    csvFile = getCsvFile()
    glmFile = getGlmFile()
    glm_name = glm_name if glm_name else getDefaultGlmName()
    fixedNodesJSON = getDefaultFixedNodesJson()
    graphJSON = getDefaultGraphJson()

    if method == 'POST':
        if (('fixedNodes' in files) and files['fixedNodes']
            and (files['fixedNodes'].filename
                 .rsplit('.', 1)[1] == 'csv')):
            try:
                with open(graph_json_file) as json_data:
                    graphJSON = json.load(json_data)
            except:
                print(f'Unable to open {graph_json_file}')
                pass

            print(f'Reading the csv file: {files["fixedNodes"].filename}')
            #session['csv'] = 1
            files['fixedNodes'].save(csvFile)

            if os.path.isfile(csvFile):
                fixedNodesJSON = parseFixedNodes(csvFile)
                with open(fixed_nodes_json_file, 'w') as outfile:
                    print(f'Writing to {fixed_nodes_json_file}')
                    outfile.write(fixedNodesJSON)

        if (('glm_file' in files) and files['glm_file']
            and (files['glm_file'].filename
                 .rsplit('.', 1)[1] == 'glm')):
            try:
                with open(fixed_nodes_json_file) as json_data:
                    fixedNodesJSON = json.load(json_data)
            except:
                pass

            print(f'Reading the glm file: {files["glm_file"].filename}')
            glm_name = files['glm_file'].filename
            files['glm_file'].save(glmFile)

            parseGlmFile(glmFile)

    return {"glm_name": glm_name}


def parseGlmFile(glmFile):
    if os.path.isfile(glmFile):
        objs, modules, commands = GLMparser.readGLM(glmFile)
        graphJSON = GLMparser.createD3JSON(objs)
        with open(graph_json_file, 'w') as outfile:
            print(f'Writing to {graph_json_file}: {graphJSON}')
            outfile.write(graphJSON)


def getGraphata(glm_name):
    print(f'getGraphata glm file name: {glm_name}')
    csvFile = getCsvFile()
    glm_name = glm_name if glm_name else getDefaultGlmName()
    fixedNodesJSON = getDefaultFixedNodesJson()
    graphJSON = getDefaultGraphJson()

    try:
        with open(fixed_nodes_json_file) as json_data:
            fixedNodesJSON = json.load(json_data)
    except:
        print(f'No data found in {fixed_nodes_json_file}')
        pass

    try:
        with open(graph_json_file) as json_data:
            graphJSON = json.load(json_data)
    except:
        print(f'No data found in {graph_json_file}')
        pass

    resp = {"file": glm_name, "graph":
            graphJSON, "fixedNodes": fixedNodesJSON}

    return resp


def parseFixedNodes(nodesFile):
    with open(nodesFile) as fr:
        lines = fr.readlines()
    names = []
    x = []
    y = []
    for line in lines:
        bla = line.split(',')
        if len(bla) == 3:
            names.append(bla[0])
            x.append(float(bla[1]))
            y.append(float(bla[2]))

    return json.dumps({'names': names, 'x': x, 'y': y})
