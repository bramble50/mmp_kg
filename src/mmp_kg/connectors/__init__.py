from mmp_kg.connectors.chembl_sql import ChemSqlDb
from mmp_kg.connectors.mmpdb_sql import MmpSqlDb

source_dict = {
    'chembl': ChemSqlDb(),
    'mmpdb': MmpSqlDb()
              }

def get_dbase(source):
    return source_dict[source]


def get_available_dbases():
    return source_dict.keys()