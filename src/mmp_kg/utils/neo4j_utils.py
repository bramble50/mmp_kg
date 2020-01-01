# -*- coding: utf-8 -*-
"""

"""
import logging

import os
import docker
from mmp_kg import config
from subprocess import Popen, PIPE
    
def build_neo4j_image():
    """builds a neo4j docker image running locally"""
    neo4j_data_dir = config.neo4j_data_dir
    neo4j_log_dir = config.neo4j_log_dir
    # docker run --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data --volume=$HOME/neo4j/logs:/logs neo4j:3.5
    client = docker.from_env()

    client.containers.run('neo4j:3.5',
                      ports={'7474':('127.0.0.1', 7474),'7687':('127.0.0.1', 7687)}, 
                      volumes={'/Users/matthew/desktop/neo4j':{'bind':'/data', 'mode': 'rw'},
                               '/Users/matthew/desktop/neo4j/logs':{'bind':'/logs', 'mode': 'rw'}
                              },
                      detach=True,
                      )
    
def create_database_locally_dep(database_file, node_edge_list_dict, path_to_neo4j=None):
    """
    node_edge_list_dict should be of the type e.g. [{'type':'nodes', 
                                                'label':"Compound", 
                                                'file':"get_compound_nodes.csv"
                                                },
                                                {'type':'nodes', 
                                                 'label':'Fragment',
                                                 'file':"get_fragment_nodes.csv"}
                                                ]
    """
    database_file = os.path.join(config.temp_dir, database_file)
    if path_to_neo4j == None:
        path_to_neo4j=config.path_to_neo4j
    else:
        path_to_neo4j
    """Using the depreciated neo4j import tool to create the graph.db file"""
    neo4j_tool = os.path.join(path_to_neo4j, 'bin/neo4j-import')
    process_list = [neo4j_tool, 
                     'import', 
                     '--into',
                     database_file,
                     '--id-type',
                     'string']
    
    for ne in node_edge_list_dict:
            ne_type = ne['type']
            ne_label = ne['label']
            ne_file = ne['name']
            process_list.append(f'--{ne_type}:{ne_label}')
            process_list.append(f'{config.temp_dir}/{ne_file}.csv')
    print(process_list)
    process = Popen(process_list, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr
          
    
def create_database_locally(path_to_neo4j=config.path_to_neo4j):
    """Using the new neo4j CLI tool to import and create the graph.db file"""
    neo4j_tool = os.path.join(path_to_neo4j, 'bin/neo4j-admin')
    process = Popen([neo4j_tool, 
                     'import', 
                     '--nodes',
                     ###TO FINISH
                    ], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    
    return stdout, stderr