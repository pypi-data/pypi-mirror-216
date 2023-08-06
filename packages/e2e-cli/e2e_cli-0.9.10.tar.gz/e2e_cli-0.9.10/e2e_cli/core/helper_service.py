import traceback, json, re
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from e2e_cli.core.py_manager import Py_version_manager

def status_error_check(status):
        try:
                if(status['errors']):
                        Py_version_manager.py_print("errors : ", status['errors'])
                        return False
                else:
                        return True
        except Exception :
               return False    

def status_msg_check(status):
            Py_version_manager.py_print("message : ", status['message'])
            
def status_code_check(status, error_result):
        a= str(status['code'])
        msg= status['message'].lower()
        if(error_result==True):
             if( a[0]=="2" and len(a)==3):
               pass
             elif( a[0]=="5" and len(a)==3):
                if("success" in msg) and ("unsuccess" not in msg):
                      Py_version_manager.py_print("issue with response in no error status code -> ", status['code'])
                elif("server" in msg)or ("error" in msg) or ("wrong" in msg) or ("issue" in msg) or ("failed" in msg):
                      pass
             else: 
                Py_version_manager.py_print("issue with response in no error status code -> ", status['code'])
        elif(error_result==False):
             if( a[0]=="2" and len(a)==3):
                Py_version_manager.py_print("issue with response in errors status code -> ", status['code'])

def status_data_check(status, req):
        EMPTY_DATA_ALLOWED=["DELETE"]

        if(status['data']):
            return True   
        else:
            if req in EMPTY_DATA_ALLOWED:
                   return True
            Py_version_manager.py_print("Your requested data seems to be empty")
            return False 
              


class Checks:

    @classmethod
    def is_int(self, id):
        try:
            int(id)
            return True
        except:
            return False

    @classmethod
    def bucket_name_validity(self, bucket_name):
        return (bool(re.findall("[A-Z]", bucket_name)) or bool(re.findall('[!@#$%^&*)(_+=}{|/><,.;:"?`~]', bucket_name)) or bool(re.findall("'", bucket_name)) or bool(re.search("]", bucket_name)) or bool(re.search("[[]", bucket_name)))

    @classmethod
    def status_result(self, status, req=""):
        status_msg_check(status) 
        error_result=status_error_check(status)  
        # code_result=status_code_check(status, error_result)
        # data_result=status_data_check(status, req)

        return error_result
        

    @classmethod
    def manage_exception(self, e):
                    Py_version_manager.py_print(e)    
                    traceback.print_exc()                 
    
    @classmethod
    def show_json(self, status, e=None):
        if(e!=None):
                Py_version_manager.py_print("Errors while reading json ",e)
        Py_version_manager.py_print(json.dumps(status, sort_keys=True, indent=4))


    @classmethod
    def take_input(self, inputs, value):
        if(value in inputs):
            # print("gfhg")
            return inputs.__dict__[value]
        else:
            return Py_version_manager.py_input("Please enter "+ value+ " : ")
        

class ApiFilter():
    def __init__(self, inputs, required, optional):
        if ("info" in inputs):
            self.api_inputs_info(required, optional)
        else:
            self.inputs_and_required_check(inputs, required)
            self.inputs_and_optional_check(inputs, optional)
        
    def inputs_and_required_check(self, inputs, required):
            """Note here type_check variable is used to check data type like int, bool and validity of the input given ex-bucket_name"""
            for input in required:
                type_check = required[input]
                value = inputs.get(input)
                if (not value):
                    inputs[input]= Py_version_manager.py_input(f"Please enter {input} : ")
                try:
                    if(type_check):
                        inputs[input] = type_check(value)
                except Exception as e:
                    import sys
                    sys.exit(f"TypeError/ValueError for {input} : {e}")

    def inputs_and_optional_check(self, inputs, optional):
            """Note here type_check variable is used to check data type like int, bool and validity of the input given ex-bucket_name"""
            for input in optional:
                type_check = optional[input]
                value = inputs.get(input)
                if (value):
                    try:
                        if(type_check):
                            inputs[input] = type_check(value)
                    except Exception as e:
                        inputs[input]=Py_version_manager.py_input(f"Please enter valid {input} : ")

    def api_inputs_info(self, required, optional):
        Py_version_manager.py_print("required inputs :")
        Py_version_manager.py_print(*required.keys(), sep="\n")
        Py_version_manager.py_print()
        Py_version_manager.py_print("optional inputs :")
        Py_version_manager.py_print(*optional.keys(), sep="\n")


def inputs_and_required_check(inputs, required):
            """Note here type_check variable is used to check data type like int, bool and validity of the input given ex-bucket_name"""
            for input in required:
                type_check = required[input]
                value = inputs.get(input)
                if (not value):
                    inputs[input]= Py_version_manager.py_input(f"Please enter {input} : ")
                try:
                    if(type_check):
                        inputs[input] = type_check(value)
                except Exception as e:
                    import sys
                    sys.exit(f"TypeError/ValueError for {input} : {e}")


def inputs_and_optional_check(inputs, optional):
            """Note here type_check variable is used to check data type like int, bool and validity of the input given ex-bucket_name"""
            for input in optional:
                type_check = optional[input]
                value = inputs.get(input)
                if (value):
                    try:
                        if(type_check):
                            inputs[input] = type_check(value)
                    except Exception as e:
                        inputs[input]=Py_version_manager.py_input(f"Please enter valid {input} : ")