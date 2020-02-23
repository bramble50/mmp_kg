# -*- coding: utf-8 -*-
"""
Holds all key chembl queries
"""
import logging
import sqlalchemy as sql
import pandas as pd
from mmp_kg import config
from mmp_kg.connectors.base_con import ChemDb

class ChemSqlDb(ChemDb):
    def __init__(self):
        self.db_path = config.chembl_sqlite_db
        self.name = self.source_name()

    @staticmethod
    def source_name():
        return 'chembl'

    def get_connection(self):
        path_to_db = self.db_path
        connection = sql.create_engine(f'sqlite:///{path_to_db}')
        return connection

    def make_query(self, template: str, **kwargs):
        sql = query_template_dict[template](**kwargs)
    
        conn = self.get_connection()
        df = pd.read_sql_query(sql, conn)

        # Add details of query to the dataframe
        query_params = kwargs
        query_params['template'] = template
        df['query'] = str(query_params)
        df['source'] = self.name

        # Log
        logging.info(f'Found {len(df)} records for {template}')

        return df
    
    @staticmethod
    def get_available_query_templates():
        return list(query_template_dict.keys())


def return_identity(x):
    return x
    
def get_adme_assays_for_docid(doc_id):
    """ get all assays for a single chembl document id"""
    query = f'''SELECT *
               FROM ASSAYS a
               WHERE a.doc_id = {doc_id}
               AND a.assay_type = 'A'
            '''
    return query

def get_assay_compounds(assay_id_list):
    if len(assay_id_list) > 1:
        assay_ids = tuple(assay_id_list)
        opperator = 'IN'
    else:
        assay_ids = assay_id_list[0]
        opperator = '='
    ''' get all compounds for a list of assay ids'''
    query = f'''SELECT cs.molregno, cs.canonical_smiles, act.standard_relation, 
               act.standard_value, act.standard_units, act.standard_type, 
               a.assay_id, a.description, a.assay_organism, a.assay_strain,
               a.assay_cell_type, a.tid, a.assay_type, a.tissue_id, a.variant_id, 
               a.assay_id || ' ' || act.standard_type ||' ' || act.standard_units || ' ' || a.assay_organism as assay_concat
               FROM activities act
               JOIN compound_structures cs ON act.molregno = cs.molregno
               JOIN assays a ON a.assay_id = act.assay_id
               WHERE act.assay_id {opperator} {assay_ids}
               '''
    return query

query_template_dict = {
    'adme_assays_for_docid': lambda doc_id: get_adme_assays_for_docid(doc_id),
    'get_assay_compounds_from_assay_ids': lambda assay_id_list: get_assay_compounds(assay_id_list),
    'custom_query': lambda sql: return_identity(sql),
}