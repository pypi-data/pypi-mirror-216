import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.cdn.cdn_crud.cdn import CdnCrud
from e2e_cli.cdn.cdn_actions.cdn_action import CdnActions

class cdn_Routing:
    def __init__(self, arguments):
        self.arguments = arguments
        
        
    def route(self, Parsing_Errors):
        if (self.arguments.args.action is None) and (self.arguments.args.cdn_commands is None):
            if(Parsing_Errors):
                Py_version_manager.py_print("Parsing Errors :")
                Py_version_manager.py_print(*Parsing_Errors, sep="\n")
                Py_version_manager.py_print("")
            subprocess.call(['e2e_cli', 'cdn', '-h'])


        elif (self.arguments.args.cdn_commands is not None) and (self.arguments.args.action is not None):
              Py_version_manager.py_print("Only one action at a time !!")


        elif(self.arguments.args.cdn_commands is not None):
            cdn_operations = CdnCrud(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if(cdn_operations.possible):
                operation = cdn_operations.caller(
                    self.arguments.args.cdn_commands)
                if operation:
                    try:
                        operation()
                    except KeyboardInterrupt:
                        Py_version_manager.py_print(" ")


        elif(self.arguments.args.action is not None):
            cdn_operations = CdnActions(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if(cdn_operations.possible):
                operation = cdn_operations.caller(
                    self.arguments.args.action)
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