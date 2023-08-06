import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.vpc.vpc import vpc_Crud

class vpc_Routing:
    def __init__(self, arguments):
        self.arguments = arguments
        
        
    def route(self, Parsing_Errors):
        if (self.arguments.args.vpc_commands is None):
            if(Parsing_Errors):
                Py_version_manager.py_print("Parsing Errors :")
                Py_version_manager.py_print(*Parsing_Errors, sep="\n")
                Py_version_manager.py_print("")
            subprocess.call(['e2e_cli', 'vpc', '-h'])


        # elif (self.arguments.args.vpc_commands is not None) and (self.arguments.args.action is not None):
        #     Py_version_manager.py_print("Only one action at a time !!")


        elif (self.arguments.args.vpc_commands is not None):
            vpc_operations = vpc_Crud(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if(vpc_operations.possible):  
                operation = vpc_operations.caller(
                    self.arguments.args.vpc_commands)
                if operation:
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