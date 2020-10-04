======
MMP_KG
======

A package to create and analyse a matched molecular pair database in Neo4J


Description
===========

MMP_KG contains functionality to create a Neo4J database of chemical matched molecular pair data using MMPDB.

Requirements
===========
- Python >3.6
- Neo4J >3.6.1
- RDKit http://rdkit.org/ 
- MMPDB https://github.com/rdkit/mmpdb
- numpy
- pandas

See requirements.txt for more info

Licence
====
This package is distributed under the GLPV3 licence. See https://github.com/bramble50/mmp_kg/blob/master/LICENSE.txt for more details.


Usage
====
The package has a core entry point: `create_graph`. This entry point does two things.
1. Creates a MMP SQLlite database given a ChEMBL database
2. Takes the MMPDB SQLlite database and transforms it into a MMPKG Neo4J database

* Clone the repo into wherever you want on your local file system
* Currently you will need to configure the config.py file before installation. This is found in `/src/mmp_kg/config.py`. Here you need to configure a path to a Neo4J installation, and the path to a ChEMBL SQLlite database file.
* Then you can install using `pip install .` in the main mmp_kg repo directory.

Now you will be able to use the command line entry point `create_graph`. This entry point takes a list of ChEMBL doc_id's and will take all molecules, assays, and assay data and transform it into a MMPKG database.

Example usage: `create_graph my_graph.db --doc_id XXXXX --mmpdb_file /path/to/mmpdb.db`

If you already have a MMP database then you can use the `--skip_mmpdb` option to skip the creation of the MMP database. To use this option you must still specify the filepath to the database using the `--mmpdb_file` argument. 

Note
====

This project has been set up using PyScaffold 3.2.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
