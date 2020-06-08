# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = mmp_kg.skeleton:run

Then run `python setup.py install` which will install the command `runner`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

"""

import argparse
import sys
import logging

from mmp_kg import __version__

__author__ = "bramble50"
__copyright__ = "bramble50"
__license__ = "GLPV3"

_logger = logging.getLogger(__name__)

from mmp_kg.connectors import get_dbase
from mmp_kg.utils import mmpdb_utils
from mmp_kg.utils import neo4j_utils
from mmp_kg import config
import pandas as pd

def create_graph_from_chembl(doc_id, graph_file):
    """Create a graph from a chembl document id

    Args:
      doc_id (int): integer
      graph_file (str): string

    Returns:
      graph_db: neo4j graph database object
    """
    dir_path = config.temp_dir
    
    # 1) Set ChEBML as the database to use
    chembl = get_dbase('chembl')
    # 2) Get assays for doc_id
    assays = chembl.make_query(template='adme_assays_for_docid', doc_id=doc_id)
    #assay_ids = tuple(assays['assay_id'].tolist())
    assay_ids = [1369280]
    # 3)Get data for all the assays
    assay_data = chembl.make_query(template='get_assay_compounds_from_assay_ids', assay_id_list=assay_ids)
    # 4) Format the data and write to disk
    assay_pivot = pd.DataFrame(assay_data.pivot_table(index='molregno', 
                                                      values='standard_value', 
                                                      columns='assay_concat', 
                                                      fill_value='*'
                                                     ).to_records())
    assay_pivot.rename(columns={'molregno':'ID'}, inplace=True)
    smiles = assay_data[['canonical_smiles','molregno']].drop_duplicates(['molregno'])
    smiles.to_csv('{0}/smiles.csv'.format(dir_path), header=False, index=False)
    assay_pivot.to_csv('{0}/properties.csv'.format(dir_path), sep='\t', index=False)
    
    # 5) Fragment smiles
    frag_info = mmpdb_utils.run_smiles_fragment(assay_data)
    
    # 6) Create mmpdb database
    mmpdb_utils.run_mmpdb(assay_data)
    
    # 7) Create Neo4J files
    mmpdb_utils.get_export_mmpkg_files()
    
    # 8) Create Neo4J Graph
    neo_info = neo4j_utils.create_database_locally(graph_file, config.node_edge_list_dict)
    
    return(neo_info)

def create_graph_from_mmpdb(graph_file, mmpdb_file):
    """Create a graph from a mmpdb db

    Args:
      mmpdb_file (str): string
      graph_file (str): string

    Returns:
      graph_db: neo4j graph database object
    """
    dir_path = config.temp_dir
    
    # 1) Create Neo4J files
    mmpdb_utils.get_export_mmpkg_files(mmpdb_file)
    
    # 2) Create Neo4J Graph
    neo_info = neo4j_utils.create_database_locally(graph_file, config.node_edge_list_dict)
    
    return(neo_info)

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Creates a mmpkg Neo4J database from assays derived from a given ChEMBL document id")
    parser.add_argument(
        "--version",
        action="version",
        version="mmp_kg {ver}".format(ver=__version__))
    parser.add_argument(
        "--doc_id",
        dest="doc_id",
        help="chembl document id",
        type=int,
        metavar="INT")
    parser.add_argument(
        dest="graph_file",
        help="name of the graph output file",
        type=str,
        metavar="STRING")
    parser.add_argument(
        "--mmpdb_file",
        dest="mmpdb_file",
        help="mmpdb database file path",
        type=str,
        metavar="STRING")
    parser.add_argument(
        "--skip_mmpdb",
        "-s",
        dest="skip_mmpdb",
        help="skips creation of the mmpdb db",
        action="store_const",
        const="skip")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO)
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Creating graph database...")
    if args.skip_mmpdb == 'skip':
        print("skipping creation of MMPDB")
        print(args.graph_file, args.mmpdb_file)
        neo_info = create_graph_from_mmpdb(args.graph_file, args.mmpdb_file)
    else:
        neo_info = create_graph_from_chembl(args.doc_id, args.graph_file)
    if neo_info == 1:
        print("Failed")
    else:
        print("Graph database has been created from {0} and outputted to filename {1}".format(args.doc_id, args.graph_file))
        _logger.info("Done")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()