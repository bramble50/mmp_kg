# -*- coding: utf-8 -*-
"""

"""
import logging

import os
import docker
from mmp_kg import config
from subprocess import Popen
    
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
    
def create_database_locally_dep(path_to_neo4j=config.path_to_neo4j, database_file, nodes, edges):
    """Using the depreciated neo4j import tool to create the graph.db file"""
    neo4j_tool = os.path.join(path_to_neo4j, 'bin/neo4j-import')
    process = Popen([neo4j_tool, 
                     'import', 
                     '--into',
                     database_file,
                     '--id-type',
                     'string',
                     '--nodes:Compound', compound_node_file,
                     '--nodes:Fragment', fragment_node_file,
                     '--relationships:IS_MMP_OF', c_c_relationship_file,
                     '--relationships:IS_FRAGMENT_OF', c_f_relationship_file,
                     '--relatoinships:IS_FRAGMENT_MMP_OF', f_f_relationship_file,
                    ], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
          
    
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