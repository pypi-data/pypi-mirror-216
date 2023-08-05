import os,sys
PROJ_DIR="/Users/qing/Library/Mobile Documents/com~apple~CloudDocs/workspace/Code/qdls/src"
# sys.path.append(PROJ_DIR)
sys.path.insert(0, PROJ_DIR)


# from src.qdls.reg import registry 
# import qdls
# print(dir(qdls.__all__))

from qdls.reg.register import registers, import_all_modules_for_register
print(registers.model._dict)
import_all_modules_for_register( only_data=False)
print(registers.model._dict)

print(registers.collator._dict)
print(registers.process_function._dict)
print("data module", registers.datamodule._dict)
# import pdb;pdb.set_trace();

@registers.process_function.register("my_test")
def my_test():
    print("This is my test function.")
    return 

from qdls.utils import print_string

registers.process_function.get("my_test")()
print_string(registers.process_function.keys())


print_string("This is direct import.")

from qdls.reg.process_functions.kqa import kqa_test_function

kqa_test_function()
 