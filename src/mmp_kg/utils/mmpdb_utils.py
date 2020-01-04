# -*- coding: utf-8 -*-
"""

"""
import logging

import os
from mmp_kg import config
from mmp_kg.connectors import get_dbase
from mmp_kg.utils.other_utils import run_and_log_process
import pandas as pd

from io import StringIO

def run_smiles_fragment(assay_data):
    """
    """
    smiles_file = os.path.join(config.temp_dir, "smiles.csv")
    fragment_file = os.path.join(config.temp_dir, "smiles.fragment")
    cpu_cores = config.cpu_cores
    #Drop duplicates
    smiles = assay_data[['canonical_smiles','molregno']].drop_duplicates(['molregno'])
    #Write to CSV
    smiles.to_csv(smiles_file, header=False, index=False)
    
    command = ['mmpdb', 
               'fragment', 
               f'{smiles_file}',
               '-o',
               f'{fragment_file}',
               '--delimiter',
               'comma',
               '-j',
               f'{cpu_cores}' 
              ]
    
    rc = run_and_log_process(command)
    
    return rc


def run_mmpdb(assay_data, output_filename = None):
    if output_filename = None:
        database_output = os.path.join(config.temp_dir, "mmp_db.mmpdb")
    else:
        database_output = os.path.join(config.temp_dir, output_path)
    fragment_file = os.path.join(config.temp_dir, "smiles.fragment")
    properties_file = os.path.join(config.temp_dir, "properties.csv")
    
    cpu_cores = config.cpu_cores
    
    assay_pivot = pd.DataFrame(assay_data.pivot_table(index='molregno', 
                                                      values='standard_value', 
                                                      columns='assay_concat', 
                                                      fill_value='*'
                                                     ).to_records())
    assay_pivot.rename(columns={'molregno':'ID'}, inplace=True)
    assay_pivot.to_csv(properties_file, sep='\t', index=False)
    command = ['mmpdb', 
               'index', 
               f'{fragment_file}',
               '--properties',
               f'{properties_file}',
               '-o',
               f'{database_output}'
              ]
    
    rc = run_and_log_process(command)
    
    return rc



def get_export_mmpkg_files(node_edge_list_dict=config.node_edge_list_dict, path_to_db = None):
    if path_to_db = None:
        try:
            path_to_db = os.path.join(config.temp_dir, "mmp_db.mmpdb"
        except Exception:
            logging.exception("No mmp database can be found...")
                          
    mmpdb = get_dbase('mmpdb')
    node_edge_list = [d['name'] for d in node_edge_list_dict]
    
    for ne in node_edge_list:
        logging.info(f'getting {ne}...')
        dataframe = mmpdb.make_query(template=ne, path_to_db)
        dataframe.to_csv(f'{config.temp_dir}/{ne}.csv', index=False)