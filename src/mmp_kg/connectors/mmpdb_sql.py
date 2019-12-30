# -*- coding: utf-8 -*-
"""
Holds all key chembl queries
"""
import logging
from mmp_kg import config
from mmp_kg.connectors.base_con import ChemDb

class ChemSqlDb(ChemDb):
    def __init__(self):
        self.db_path = config.mmpdb_database

    @staticmethod
    def source_name():
        return 'mmpdb'

    def get_connection(self):
        path_to_db = self.db_path
        connection = sql.create_engine(f'sqlite:///{path_to_db}')
        return connection

    def make_query(self, template: str, **kwargs):
        sql = query_template_dict[template](**kwargs)
    
        connection = self.get_connection()
        with connection as conn:
            df = pd.read_sql_query(sql, conn)

        # Add details of query to the dataframe
        query_params = kwargs
        query_params['template'] = template
        df['query'] = str(query_params)
        df['source'] = self.name

        # Log
        logging.info(f'{len(df)}')

        return df

def return_identity(x):
    return x

query_template_dict = {
    #Fragment nodes
    'get_fragment_nodes': '''SELECT DISTINCT t2.fragment_id as "fragmentid:ID(Fragment)", t2.smiles 
                             FROM
                             (SELECT re.environment_fingerprint_id, rs.smiles, rs.id as fragment_id
                             FROM rule_environment re
                             JOIN rule r ON re.rule_id = r.id
                             JOIN rule_smiles rs ON rs.id = r.from_smiles_id
                             UNION
                             SELECT re.environment_fingerprint_id, rs.smiles, rs.id as fragment_id
                             FROM rule_environment re
                             JOIN rule r ON re.rule_id = r.id
                             JOIN rule_smiles rs ON rs.id = r.to_smiles_id)t2''',
    #Compound nodes
    'get_compound_nodes': '''SELECT c.id as "compoundid:ID(Compound)", c.clean_smiles as smiles 
                             FROM compound c''',
    #Environment nodes
    'get_environment_nodes': '''SELECT DISTINCT re.environment_fingerprint_id as "environmentid:ID(Environment)",  
                                re.radius as "radius:int", 
                                ef.fingerprint
                                FROM rule_environment re
                                JOIN environment_fingerprint ef ON re.environment_fingerprint_id = ef.id
                                GROUP BY re.environment_fingerprint_id''',
    #Fragment -> Environment edges - IS_IN_ENVIRONMENT
    'get_fragment_environment_edges': '''SELECT DISTINCT t2.environment_fingerprint_id as ":END_ID(Environment)",
                                         t2.id as ":START_ID(Fragment)"
                                         FROM
                                         (SELECT re.environment_fingerprint_id, rs.smiles, rs.id
                                         FROM rule_environment re
                                         JOIN rule r ON re.rule_id = r.id
                                         JOIN rule_smiles rs ON rs.id = r.from_smiles_id
                                         UNION
                                         SELECT re.environment_fingerprint_id, rs.smiles, rs.id
                                         FROM rule_environment re
                                         JOIN rule r ON re.rule_id = r.id
                                         JOIN rule_smiles rs ON rs.id = r.to_smiles_id)t2''',
    #Fragment -> Fragment - MMP_RULE_ENVIRONMENT
    'get_fragment_fragment_edges': '''SELECT r.from_smiles_id as ":START_ID(Fragment)", r.to_smiles_id as ":END_ID(Fragment)",
                                      res.id as "id:int",
                                      res.rule_environment_id as "rule_environment_id:int",
                                      res.property_name_id as "property_name_id:int",
                                      pn.name as "property_name",
                                      res.count as "count:int",
                                      res.avg as "avg:float",
                                      res.std as "std:float",
                                      res.kurtosis as "kurtosis:float",
                                      res.skewness as "skewness:float",
                                      res.min as "min:float",
                                      res.q1 as "q1:float",
                                      res.median as "median:float",
                                      res.max as "max:float",
                                      res.paired_t as "paired_t:float", 
                                      res.p_value as "p_value:float",
                                      re.environment_fingerprint_id as "environment_fingerprint_id:int",
                                      re.radius as "radius:int", ef.fingerprint
                                      FROM rule_environment_statistics res
                                      JOIN rule_environment re ON re.id = res.rule_environment_id
                                      JOIN rule r ON re.rule_id = r.id
                                      JOIN environment_fingerprint ef ON re.environment_fingerprint_id = ef.id
                                      JOIN property_name pn ON res.property_name_id = pn.id
                                      ORDER BY res.count desc''',
    #Compound <-> Compound - IS_MMP_OF
    'get_compound_compound_edges': '''SELECT DISTINCT c.compound1_id as ":START_ID(Compound)",
                                      c.compound2_id as ":END_ID(Compound)"
                                      FROM pair c
                                      JOIN compound AS cp1 ON cp1.id = c.compound1_id
                                      JOIN compound AS cp2 ON cp2.id = c.compound2_id'''
    #Compound -> Fragment - IS_FRAGMENT_OF
    'get_compound_fragment_edges': '''SELECT p.compound1_id as ":START_ID(Compound)", 
                                      r.from_smiles_id as ":END_ID(Fragment)"
                                      FROM pair p
                                      JOIN rule_environment re ON p.rule_environment_id = re.id
                                      JOIN rule r ON re.rule_id = r.id
                                      JOIN rule_smiles rs ON rs.id = r.from_smiles_id
                                      UNION
                                      SELECT p.compound2_id as "compound_id", r.to_smiles_id as "fragment_id"
                                      FROM pair p
                                      JOIN rule_environment re ON p.rule_environment_id = re.id
                                      JOIN rule r ON re.rule_id = r.id
                                      JOIN rule_smiles rs ON rs.id = r.to_smiles_id'''
    #Custom query
    'custom_query': lambda sql: return_identity(sql),
}