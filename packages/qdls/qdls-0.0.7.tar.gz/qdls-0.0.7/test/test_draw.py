import os,sys
PROJ_DIR="/Users/qing/Library/Mobile Documents/com~apple~CloudDocs/workspace/Code/qdls"
sys.path.append(PROJ_DIR)

def test_syntax():
    from src.qdls.gql.sparql.utils.syntax import syntax_check

    # s1 = "select ?x {?e ?p 'asd'}"
    s = "SELECT DISTINCT?qpv WHERE {?e_1 <pred:name> \"Mrs. Miniver\".?e_2 <pred:name> \"Academy Award for Best Writing, Adapted Screenplay\".?e_1 <award_received>?e_2. [ <pred:fact_h>?e_1 ; <pred:fact_r> <award_received> ; <pred:fact_t>?e_2 ] <winner>?qpv.  }"

    flag, tree, parser = syntax_check(s)

    print(flag)
    print(type(tree))
    print("error msg:", tree)

def test_config():
    import omegaconf

    config = omegaconf.OmegaConf.load("example_config.yaml")
    print(config)
    print(type(config))
    from src.qdls.utils import config2dict, print_config
    d = config2dict(config)
    print(d)
    print_config(config, 'test pc')


if __name__ == '__main__':
    test_config()
