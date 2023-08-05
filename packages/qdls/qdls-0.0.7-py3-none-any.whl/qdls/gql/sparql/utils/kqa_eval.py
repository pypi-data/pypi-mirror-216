
import rdflib
from rdflib import URIRef, BNode, Literal, XSD
from rdflib.plugins.stores import sparqlstore
from itertools import chain
import os, sys 
try:
    from q_snippets.data import load_json, save_json
except:
    from qdls.data import load_json, save_json
from qdls.gql.sparql.utils.syntax import syntax_check
from qdls.utils import print_string
from multiprocessing import Pool

# FILE_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJ_DIR = FILE_DIR[:FILE_DIR.index('src')]
# PROJ_DIR = "/home/qing/workspace/archive/ACL23"
# sys.path.append(PROJ_DIR)


import json 
import re 
from datetime import date
from tqdm import tqdm

class ValueClass():
    def __init__(self, type, value, unit=None):
        """
        When type is
            - string, value is a str
            - quantity, value is a number and unit is required
            - year, value is a int
            - date, value is a date object
        """
        self.type = type
        self.value = value
        self.unit = unit

    def isTime(self):
        return self.type in {'year', 'date'}

    def can_compare(self, other):
        if self.type == 'string':
            return other.type == 'string'
        elif self.type == 'quantity':
            # NOTE: for two quantity, they can compare only when they have the same unit
            return other.type == 'quantity' and other.unit == self.unit
        else:
            # year can compare with date
            return other.type == 'year' or other.type == 'date'

    def contains(self, other):
        """
        check whether self contains other, which is different from __eq__ and the result is asymmetric
        used for conditions like whether 2001-01-01 in 2001, or whether 2001 in 2001-01-01
        """
        if self.type == 'year': # year can contain year and date
            other_value = other.value if other.type == 'year' else other.value.year
            return self.value == other_value
        elif self.type == 'date': # date can only contain date
            return other.type == 'date' and self.value == other.value
        else:
            raise Exception('not supported type: %s' % self.type)


    def __eq__(self, other):
        """
        2001 and 2001-01-01 is not equal
        """
        assert self.can_compare(other)
        return self.type == other.type and self.value == other.value

    def __lt__(self, other):
        """
        Comparison between a year and a date will convert them both to year
        """
        assert self.can_compare(other)
        if self.type == 'string':
            raise Exception('try to compare two string')
        elif self.type == 'quantity':
            return self.value < other.value
        elif self.type == 'year':
            other_value = other.value if other.type == 'year' else other.value.year
            return self.value < other_value
        elif self.type == 'date':
            if other.type == 'year':
                return self.value.year < other.value
            else:
                return self.value < other.value

    def __gt__(self, other):
        assert self.can_compare(other)
        if self.type == 'string':
            raise Exception('try to compare two string')
        elif self.type == 'quantity':
            return self.value > other.value
        elif self.type == 'year':
            other_value = other.value if other.type == 'year' else other.value.year
            return self.value > other_value
        elif self.type == 'date':
            if other.type == 'year':
                return self.value.year > other.value
            else:
                return self.value > other.value

    def __str__(self):
        if self.type == 'string':
            return self.value
        elif self.type == 'quantity':
            if self.value - int(self.value) < 1e-5:
                v = int(self.value)
            else:
                v = self.value
            return '{} {}'.format(v, self.unit) if self.unit != '1' else str(v)
        elif self.type == 'year':
            return str(self.value)
        elif self.type == 'date':
            return self.value.isoformat()


class DataForSPARQL(object):
    def __init__(self, kb_path):
        kb = json.load(open(kb_path))
        self.concepts = kb['concepts']
        self.entities = kb['entities']

        # replace adjacent space and tab in name, which may cause errors when building sparql query
        for con_id, con_info in self.concepts.items():
            con_info['name'] = ' '.join(con_info['name'].split())
        for ent_id, ent_info in self.entities.items():
            ent_info['name'] = ' '.join(ent_info['name'].split())

        # get all attribute keys and predicates
        self.attribute_keys = set()
        self.predicates = set()
        self.key_type = {}
        for ent_id, ent_info in self.entities.items():
            for attr_info in ent_info['attributes']:
                self.attribute_keys.add(attr_info['key'])
                self.key_type[attr_info['key']] = attr_info['value']['type']
                for qk in attr_info['qualifiers']:
                    self.attribute_keys.add(qk)
                    for qv in attr_info['qualifiers'][qk]:
                        self.key_type[qk] = qv['type']
        for ent_id, ent_info in self.entities.items():
            for rel_info in ent_info['relations']:
                self.predicates.add(rel_info['predicate'])
                for qk in rel_info['qualifiers']:
                    self.attribute_keys.add(qk)
                    for qv in rel_info['qualifiers'][qk]:
                        self.key_type[qk] = qv['type']
        self.attribute_keys = list(self.attribute_keys)
        self.predicates = list(self.predicates)
        # Note: key_type is one of string/quantity/date, but date means the key may have values of type year
        self.key_type = { k:v if v!='year' else 'date' for k,v in self.key_type.items() }

        # parse values into ValueClass object
        for ent_id, ent_info in self.entities.items():
            for attr_info in ent_info['attributes']:
                attr_info['value'] = self._parse_value(attr_info['value'])
                for qk, qvs in attr_info['qualifiers'].items():
                    attr_info['qualifiers'][qk] = [self._parse_value(qv) for qv in qvs]
        for ent_id, ent_info in self.entities.items():
            for rel_info in ent_info['relations']:
                for qk, qvs in rel_info['qualifiers'].items():
                    rel_info['qualifiers'][qk] = [self._parse_value(qv) for qv in qvs]

    def _parse_value(self, value):
        if value['type'] == 'date':
            x = value['value']
            p1, p2 = x.find('/'), x.rfind('/')
            y, m, d = int(x[:p1]), int(x[p1+1:p2]), int(x[p2+1:])
            result = ValueClass('date', date(y, m, d))
        elif value['type'] == 'year':
            result = ValueClass('year', value['value'])
        elif value['type'] == 'string':
            result = ValueClass('string', value['value'])
        elif value['type'] == 'quantity':
            result = ValueClass('quantity', value['value'], value['unit'])
        else:
            raise Exception('unsupport value type')
        return result

    def get_direct_concepts(self, ent_id):
        """
        return the direct concept id of given entity/concept
        """
        if ent_id in self.entities:
            return self.entities[ent_id]['instanceOf']
        elif ent_id in self.concepts:
            return self.concepts[ent_id]['instanceOf']
        else:
            raise Exception('unknown id')

    def get_all_concepts(self, ent_id):
        """
        return a concept id list
        """
        ancestors = []
        q = Queue()
        for c in self.get_direct_concepts(ent_id):
            q.put(c)
        while not q.empty():
            con_id = q.get()
            ancestors.append(con_id)
            for c in self.concepts[con_id]['instanceOf']:
                q.put(c)

        return ancestors

    def get_name(self, ent_id):
        if ent_id in self.entities:
            return self.entities[ent_id]['name']
        elif ent_id in self.concepts:
            return self.concepts[ent_id]['name']
        else:
            return None

    def is_concept(self, ent_id):
        return ent_id in self.concepts

    def get_attribute_facts(self, ent_id, key=None, unit=None):
        if key:
            facts = []
            for attr_info in self.entities[ent_id]['attributes']:
                if attr_info['key'] == key:
                    if unit:
                        if attr_info['value'].unit == unit:
                            facts.append(attr_info)
                    else:
                        facts.append(attr_info)
        else:
            facts = self.entities[ent_id]['attributes']
        facts = [(f['key'], f['value'], f['qualifiers']) for f in facts]
        return facts

    def get_relation_facts(self, ent_id):
        facts = self.entities[ent_id]['relations']
        facts = [(f['predicate'], f['object'], f['direction'], f['qualifiers']) for f in facts]
        return facts



# kb = DataForSPARQL(os.path.join(PROJ_DIR, 'data/dataset/kb.json'))
# kb = DataForSPARQL("/Users/qing/Downloads/kb.json")

def legal(s):
    # convert predicate and attribute keys to legal format
    return s.replace(' ', '_')

class SparqlEngine():
    gs1 = None
    PRED_INSTANCE = 'pred:instance_of'
    PRED_NAME = 'pred:name'

    PRED_VALUE = 'pred:value'       # link packed value node to its literal value
    PRED_UNIT = 'pred:unit'         # link packed value node to its unit

    PRED_YEAR = 'pred:year'         # link packed value node to its year value, which is an integer
    PRED_DATE = 'pred:date'         # link packed value node to its date value, which is a date

    PRED_FACT_H = 'pred:fact_h'     # link qualifier node to its head
    PRED_FACT_R = 'pred:fact_r'
    PRED_FACT_T = 'pred:fact_t'

    SPECIAL_PREDICATES = (PRED_INSTANCE, PRED_NAME, PRED_VALUE, PRED_UNIT, PRED_YEAR, PRED_DATE, PRED_FACT_H, PRED_FACT_R, PRED_FACT_T)
    def __init__(self, data, ttl_file=''):
        self.nodes = nodes = {}
        for i in chain(data.concepts, data.entities):
            nodes[i] = URIRef(i)
        for p in chain(data.predicates, data.attribute_keys, SparqlEngine.SPECIAL_PREDICATES):
            nodes[p] = URIRef(legal(p))
        
        self.graph = graph = rdflib.Graph()

        for i in chain(data.concepts, data.entities):
            name = data.get_name(i)
            graph.add((nodes[i], nodes[SparqlEngine.PRED_NAME], Literal(name)))

        for ent_id in tqdm(data.entities, desc='Establishing rdf graph'):
            for con_id in data.get_all_concepts(ent_id):
                graph.add((nodes[ent_id], nodes[SparqlEngine.PRED_INSTANCE], nodes[con_id]))
            for (k, v, qualifiers) in data.get_attribute_facts(ent_id):
                h, r = nodes[ent_id], nodes[k]
                t = self._get_value_node(v)
                graph.add((h, r, t))
                fact_node = self._new_fact_node(h, r, t)

                for qk, qvs in qualifiers.items():
                    for qv in qvs:
                        h, r = fact_node, nodes[qk]
                        t = self._get_value_node(qv)
                        if len(list(graph[t])) == 0:
                            print(t)
                        graph.add((h, r, t))

            for (pred, obj_id, direction, qualifiers) in data.get_relation_facts(ent_id):
                if direction == 'backward':
                    if data.is_concept(obj_id):
                        h, r, t = nodes[obj_id], nodes[pred], nodes[ent_id]
                    else:
                        continue
                else:
                    h, r, t = nodes[ent_id], nodes[pred], nodes[obj_id]
                graph.add((h, r, t))
                fact_node = self._new_fact_node(h, r, t)
                for qk, qvs in qualifiers.items():
                    for qv in qvs:
                        h, r = fact_node, nodes[qk]
                        t = self._get_value_node(qv)
                        graph.add((h, r, t))

        if ttl_file:
            print('Save graph to {}'.format(ttl_file))
            graph.serialize(ttl_file, format='turtle')


    def _get_value_node(self, v):
        # we use a URIRef node, because we need its reference in query results, which is not supported by BNode
        if v.type == 'string':
            node = BNode()
            self.graph.add((node, self.nodes[SparqlEngine.PRED_VALUE], Literal(v.value)))
            return node
        elif v.type == 'quantity': 
            # we use a node to pack value and unit
            node = BNode()
            self.graph.add((node, self.nodes[SparqlEngine.PRED_VALUE], Literal(v.value, datatype=XSD.double)))
            self.graph.add((node, self.nodes[SparqlEngine.PRED_UNIT], Literal(v.unit)))
            return node
        elif v.type == 'year':
            node = BNode()
            self.graph.add((node, self.nodes[SparqlEngine.PRED_YEAR], Literal(v.value)))
            return node
        elif v.type == 'date':
            # use a node to pack year and date
            node = BNode()
            self.graph.add((node, self.nodes[SparqlEngine.PRED_YEAR], Literal(v.value.year)))
            self.graph.add((node, self.nodes[SparqlEngine.PRED_DATE], Literal(v.value, datatype=XSD.date)))
            return node

    def _new_fact_node(self, h, r, t):
        node = BNode()
        self.graph.add((node, self.nodes[SparqlEngine.PRED_FACT_H], h))
        self.graph.add((node, self.nodes[SparqlEngine.PRED_FACT_R], r))
        self.graph.add((node, self.nodes[SparqlEngine.PRED_FACT_T], t))
        return node



def query_virtuoso(q, virtuoso_address, virtuoso_graph_uri):
    endpoint = virtuoso_address
    store=sparqlstore.SPARQLUpdateStore(endpoint)
    gs = rdflib.ConjunctiveGraph(store)
    gs.open((endpoint, endpoint))
    gs1 = gs.get_context(rdflib.URIRef(virtuoso_graph_uri))
    res = gs1.query(q)
    return res

def get_sparql_answer(sparql, data, config):
    """
    data: DataForSPARQL object, we need the key_type
    """
    try:
        # infer the parse_type based on sparql
        if sparql.startswith('SELECT DISTINCT ?e') or sparql.startswith('SELECT ?e'):
            parse_type = 'name'
        elif sparql.startswith('SELECT (COUNT(DISTINCT ?e)'):
            parse_type = 'count'
        elif sparql.startswith('SELECT DISTINCT ?p '):
            parse_type = 'pred'
        elif sparql.startswith('ASK'):
            parse_type = 'bool'
        else:
            tokens = sparql.split()
            tgt = tokens[2]
            for i in range(len(tokens)-1, 1, -1):
                if tokens[i]=='.' and tokens[i-1]==tgt:      #  key tgt .
                    key = tokens[i-2]
                    break
            key = key[1:-1].replace('_', ' ')
            t = data.key_type[key]
            parse_type = 'attr_{}'.format(t)

        parsed_answer = None

        res = query_virtuoso(sparql, virtuoso_address=config.virtuoso_address, virtuoso_graph_uri=config.virtuoso_graph_uri)

        if res.vars:
            res = [[binding[v] for v in res.vars] for binding in res.bindings]
            if len(res) != 1:
                return None
        else:
            res = res.askAnswer
            assert parse_type == 'bool'
        
        if parse_type == 'name':
            node = res[0][0]
            sp = 'SELECT DISTINCT ?v WHERE {{ <{}> <{}> ?v .  }}'.format(node, SparqlEngine.PRED_NAME)
            res = query_virtuoso(sp, virtuoso_address=config.virtuoso_address, virtuoso_graph_uri=config.virtuoso_graph_uri)
            res = [[binding[v] for v in res.vars] for binding in res.bindings]
            name = res[0][0].value
            parsed_answer = name
        elif parse_type == 'count':
            count = res[0][0].value
            parsed_answer = str(count)
        elif parse_type.startswith('attr_'):
            node = res[0][0]
            v_type = parse_type.split('_')[1]
            unit = None
            if v_type == 'string':
                sp = 'SELECT DISTINCT ?v WHERE {{ <{}> <{}> ?v .  }}'.format(node, SparqlEngine.PRED_VALUE)
            elif v_type == 'quantity':
                # Note: For those large number, ?v is truncated by virtuoso (e.g., 14756087 to 1.47561e+07)
                # To obtain the accurate ?v, we need to cast it to str
                sp = 'SELECT DISTINCT ?v,?u,(str(?v) as ?sv) WHERE {{ <{}> <{}> ?v ; <{}> ?u .  }}'.format(node, SparqlEngine.PRED_VALUE, SparqlEngine.PRED_UNIT)
            elif v_type == 'year':
                sp = 'SELECT DISTINCT ?v WHERE {{ <{}> <{}> ?v .  }}'.format(node, SparqlEngine.PRED_YEAR)
            elif v_type == 'date':
                sp = 'SELECT DISTINCT ?v WHERE {{ <{}> <{}> ?v .  }}'.format(node, SparqlEngine.PRED_DATE)
            else:
                raise Exception('unsupported parse type')
            res = query_virtuoso(sp, virtuoso_address=config.virtuoso_address, virtuoso_graph_uri=config.virtuoso_graph_uri)
            res = [[binding[v] for v in res.vars] for binding in res.bindings]
            # if there is no specific date, then convert the type to year
            if len(res)==0 and v_type == 'date':
                v_type = 'year'
                sp = 'SELECT DISTINCT ?v WHERE {{ <{}> <{}> ?v .  }}'.format(node, SparqlEngine.PRED_YEAR)
                res = query_virtuoso(sp, virtuoso_address=config.virtuoso_address, virtuoso_graph_uri=config.virtuoso_graph_uri)
                res = [[binding[v] for v in res.vars] for binding in res.bindings]
            if v_type == 'quantity':
                value = float(res[0][2].value)
                unit = res[0][1].value
            else:
                value = res[0][0].value
            value = ValueClass(v_type, value, unit)
            parsed_answer = str(value)
        elif parse_type == 'bool':
            parsed_answer = 'yes' if res else 'no'
        elif parse_type == 'pred':
            parsed_answer = str(res[0][0])
            parsed_answer = parsed_answer.replace('_', ' ')
        # return parsed_answer
    except Exception as e:
        print(e)
        parsed_answer = None 
    # print(parsed_answer)
    return parsed_answer

def whether_equal(answer, pred):
    """
    check whether the two arguments are equal as attribute value
    answer type should be str 
    """
    def truncate_float(x):
        # convert answer from '100.0 meters' to '100 meters'
        try:
            v, *u = x.split()
            v = float(v)
            if v - int(v) < 1e-5:
                v = int(v)
            if len(u) == 0:
                x = str(v)
            else:
                x = '{} {}'.format(str(v), ' '.join(u))
        except:
            pass
        return x

    def equal_as_date(x, y):
        # check whether x and y are equal as type of date or year
        try:
            x_split = x.split('-')
            y_split = y.split('-')
            if len(x_split) == 3:
                x = date(int(x_split[0]), int(x_split[1]), int(x_split[2]))
            else:
                x = int(x)
            if len(y_split) == 3:
                y = date(int(y_split[0]), int(y_split[1]), int(y_split[2]))
            else:
                y = int(y)
            if isinstance(x, date) and isinstance(y, date):
                return x == y
            else:
                x = x.year if isinstance(x, date) else x
                y = y.year if isinstance(y, date) else y
                return x == y
        except:
            return False

    answer = truncate_float(answer)
    pred = truncate_float(pred)
    if equal_as_date(answer, pred):
        return True
    else:
        return answer == pred


def post_process(text):
    """
    针对BART生成结果的预处理
    字符串提取出来，其余部分是chunks， 需要增加?和.前的空格， 最后再组装起来即可
    !!!!!!!!!  只需要处理生成的， trainset里的就不用处理了
    """
    pattern = re.compile(r'".*?"')    # 匹配字符串？
    nes = []
    for item in pattern.finditer(text):
        nes.append((item.group(), item.span()))
    pos = [0]
    for name, span in nes:
        pos += [span[0], span[1]]
    pos.append(len(text))
    assert len(pos) % 2 == 0
    assert len(pos) / 2 == len(nes) + 1
    chunks = [text[pos[i]: pos[i+1]] for i in range(0, len(pos), 2)]
    for i in range(len(chunks)):
        chunks[i] = chunks[i].replace('?', ' ?').replace('.', ' .')           # 增加空格
    bingo = ''
    for i in range(len(chunks) - 1):
        bingo += chunks[i] + nes[i][0]
    bingo += chunks[-1]
    return bingo

def pseudo_post_process(text):
    return text 

def exec_sparql(sparql, answer, config, kb, process_fn=pseudo_post_process):
    sparql = process_fn(sparql)
    # print("==>", sparql)
    pred_answer = get_sparql_answer(sparql, kb, config)
    is_match = whether_equal(answer, pred_answer)
    # print(sparql)
    # print(is_match, pred_answer, answer)
    return is_match, pred_answer


def sparql_exec_acc(path, key='pred', nproc=1, resave=False, config=None, kb=None, process_fn=pseudo_post_process):
    """ path: 可以是字符串（读取文件）也可以是读取后的对象list 
        key: 每一个sample字典中, 预测的sparql语句的key
        nproc: 并行处理的进程数
        resave: bool or string  是否重新保存结果, 保存在原目录, 文件名前加上exec_
        config: 配置文件, 主要是virtuoso的 address 和 graph uri
        kb: 知识库
        process_fn: 对sparql进行处理的函数
    """
    data = load_json(path) if type(path) is str else path 
    Results = []
    if nproc > 1:
        with Pool(nproc) as pool:
            R = {}
            for sample in data:
                assert key in sample, f"key `{key}` not in provided data, sample.keys()={sample.keys()}"
                sparql = sample[key]
                answer = sample['answer']
                future = pool.apply_async(exec_sparql, (sparql, answer, config, kb, process_fn))
                R[future] = sample
            
            for future in tqdm(R):
                try:
                    res = future.get(timeout=3)
                except:
                    res = False, 'timeout'  
                Results.append(res)
    else:
        print_string("sequential processing")
        for sample in tqdm(data):
            assert key in sample, f"key `{key}` not in provided data, sample.keys()={sample.keys()}"
            sparql = sample[key]
            answer = sample['answer']
            Results.append(exec_sparql(sparql, answer, config, kb, process_fn))

    cnt = len(data)
    correct, wrong = 0, 0
    for is_match, pred in Results:
        if is_match:
            correct += 1
        else:
            wrong += 1
 

    acc = 100 *  correct/ cnt
    print(f"{correct} of {cnt} is correct, {acc:.3f};  {wrong} wrong")

    if resave:
        if type(resave) is not str:
            assert type(path) is str, "resave=True, path should be a string, or set resave=filepath"
        else:
            path = resave

        for sample, exec_res in zip(data, Results):
            sample['exec'] = exec_res
        
        new_filename = "exec_" + os.path.basename(path)
        new_path = os.path.join(os.path.dirname(path), new_filename)
        save_json(data, new_path)

    return acc, Results



if __name__ == '__main__':
    pass 