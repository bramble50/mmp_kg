#The filepath to your chembl sqllite database:
chembl_sqlite_db = "/Users/matthew/code/databases/chembl_25/chembl_25_sqlite/chembl_25.db"

#for parts of the code that can be parallised specify the cpu core limit
cpu_cores = 8

# Temp directory
temp_dir = "."

# Where should the mmpdb sqlite db be stored?
mmpdb_database = "/Users/matthew/desktop/database.mmpdb"

# Neo4J path - the directory where your neo4j installation is located 
#(if you don't have a neo4j installation set as "None")
path_to_neo4j = "/Users/matthew/downloads/neo4j-community-3.5.14/"