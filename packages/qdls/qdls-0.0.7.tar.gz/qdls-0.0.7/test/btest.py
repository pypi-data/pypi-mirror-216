
from qdls.gql.cypher.utils.kqa_eval import cypher_exec_eval
from argparse import Namespace

path = "/Users/qing/Downloads/sampled_50.json"

# config = Namespace(neo4j_uri="neo4j://172.23.148.83:28892", neo4j_user="neo4j", neo4j_passwd="kqa", timeout=10)
# cypher_exec_eval(path, key='cypher', nproc=1, config=config)

#############################################

# 需要先修改 rdflib 
from qdls.gql.sparql.utils.kqa_eval import sparql_exec_acc, DataForSPARQL


virtuoso_address = "http://172.23.148.83:28890/sparql"
virtuoso_graph_uri = 'kqaspcy'
config = Namespace(
    virtuoso_address = virtuoso_address,
    virtuoso_graph_uri=virtuoso_graph_uri,
)

kb = DataForSPARQL("/Users/qing/Downloads/kb.json")
# sparql_exec_acc(path, key='sparql', nproc=1, config=config)

sparql_exec_acc(path, key='sparql', nproc=1, config=config, kb=kb)