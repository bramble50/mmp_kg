#The filepath to your chembl sqllite database:
chembl_sqlite_db = "/Users/matthew/code/databases/chembl_25/chembl_25_sqlite/chembl_25.db"

#for parts of the code that can be parallised specify the cpu core limit
cpu_cores = 8

# Temp directory
temp_dir = "."

# Neo4J path - the directory where your neo4j installation is located 
#(if you don't have a neo4j installation set as "None")
path_to_neo4j = "/Users/matthew/downloads/neo4j-community-3.5.14/"


# The list of edges and nodes you can create
# names must match the query name in mmp_kg.connectors.mmpdb_sql.py
node_edge_list_dict = [{'type':'nodes', 
                        'label':'Compound', 
                        'name':'get_compound_nodes'},
                       {'type':'nodes', 
                        'label':'Fragment', 
                        'name':'get_fragment_nodes'},
#                       {'type':'nodes',
#                        'label':'Environment',
#                        'name':'get_environment_nodes'},
#                       {'type':'edges',
#                        'label':'IS_IN_ENVIRONMENT',
#                        'name':'get_fragment_environment_edges'},
#                       {'type':'edges',
#                        'label':'MMP_RULE_ENVIRONMENT',
#                        'name':'get_fragment_fragment_edges'},
                       {'type':'edges',
                        'label':'IS_MMP_OF',
                        'name':'get_compound_compound_edges'},
                       {'type':'edges',
                        'label':'IS_FRAGMENT_OF',
                        'name':'get_compound_fragment_edges'},
                      ]
