import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.bucket_store.bucket_crud.bucket_storage import BucketCrud
from e2e_cli.bucket_store.bucket_actions.bucket_actions import BucketActions

class BucketRouting:
    def __init__(self, arguments):
        self.arguments = arguments
        
        
    def route(self, Parsing_Errors):
        if (self.arguments.args.bucket_commands is None) and (self.arguments.args.action is None):
            if(Parsing_Errors):
                Py_version_manager.py_print("Parsing Errors :")
                Py_version_manager.py_print(*Parsing_Errors, sep="\n")
                Py_version_manager.py_print("")
            subprocess.call(['e2e_cli', 'bucket', '-h'])


        elif (self.arguments.args.bucket_commands is not None) and (self.arguments.args.action is not None):
              Py_version_manager.py_print("Only one action at a time !!")


        elif(self.arguments.args.bucket_commands is not None):
            bucket_operations = BucketCrud(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if(bucket_operations.possible):
                operation = bucket_operations.caller(
                    self.arguments.args.bucket_commands)
                if (operation):
                    try:
                        operation()
                    except KeyboardInterrupt:
                        Py_version_manager.py_print(" ")


        elif(self.arguments.args.action is not None):
            bucket_operations=BucketActions(alias=self.arguments.args.alias, inputs=self.arguments.inputs)     
            if(bucket_operations.possible):
                operation = bucket_operations.caller(
                    self.arguments.args.action)
                if (operation):
                    try:
                        operation()
                    except KeyboardInterrupt:
                        Py_version_manager.py_print(" ")

                else:
                    Py_version_manager.py_print("command not found")
                    if(Parsing_Errors):
                        Py_version_manager.py_print("Parsing Errors :")
                        Py_version_manager.py_print(*Parsing_Errors, sep="\n")


        else:
            Py_version_manager.py_print("command not found")
            if(Parsing_Errors):
                Py_version_manager.py_print("Parsing Errors :")
                Py_version_manager.py_print(*Parsing_Errors, sep="\n")