# -*- coding: utf-8 -*-
"""

"""
import logging

import os
from mmp_kg import config
from mmp_kg.connectors import get_dbase
from subprocess import Popen, PIPE

def run_smiles_fragment(assay_data):
    """
    """
    smiles_file = os.path.join(config.temp_dir, "/smiles.csv")
    fragment_file = os.path.join(config.temp_dir, "/smiles.fragment")
    cpu_cores = config.cpu_cores
    #Drop duplicates
    smiles = assay_data[['canonical_smiles','molregno']].drop_duplicates(['molregno'])
    #Write to CSV
    smiles.to_csv(f'{temp_dir}/smiles.csv', header=False, index=False)
    
    process = Popen(['mmpdb', 
                     'fragment', 
                     f'{smiles_file}',
                     '-o',
                     f'{fragment_file}',
                     '--delimiter',
                     'comma',
                     '-j',
                     f'{cpu_cores}' 
                    ], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    
    return stdout, stderr

def run_mmpdb(assay_data):
    fragment_file = os.path.join(config.temp_dir, "/smiles.fragment")
    properties_file = os.path.join(config.temp_dir, "/properties.csv")
    database_output = config.mmpdb_database
    cpu_cores = config.cpu_cores
    
    assay_pivot = pd.DataFrame(assay_data.pivot_table(index='molregno', 
                                                      values='standard_value', 
                                                      columns='assay_concat', 
                                                      fill_value='*'
                                                     ).to_records())
    assay_pivot.rename(columns={'molregno':'ID'}, inplace=True)
    assay_pivot.to_csv(properties_file, sep='\t', index=False)
    
    process = Popen(['mmpdb', 
                     'index', 
                     f'{fragment_file}',
                     '--properties',
                     f'{properties_file}',
                     '-o',
                     f'{database_output}'
                    ], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    
    return stdout, stderr

def get_export_mmpkg_files(node_edge_list_dict=config.node_edge_list_dict):
    
    mmpdb = get_dbase('mmpdb')
    node_edge_list = [d['name'] for d in node_edge_list_dict]
    
    for ne in node_edge_list:
        logging.info(f'getting {ne}...')
        dataframe = mmpdb.make_query(template=ne)
        dataframe.to_csv(f'{config.temp_dir}/{ne}.csv', index=False)