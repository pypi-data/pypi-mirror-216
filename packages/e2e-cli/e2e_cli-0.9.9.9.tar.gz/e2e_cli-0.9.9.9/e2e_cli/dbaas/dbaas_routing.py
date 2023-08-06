import subprocess

from e2e_cli.dbaas.dbaas_crud.dbaas import DBaaSCrud
from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.dbaas.dbaas_actions.dbaas_action import DBaasAction



class DBaaSRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, Parsing_Errors):
        if (self.arguments.args.dbaas_commands is None) and (self.arguments.args.action is None):
            if(Parsing_Errors):
                Py_version_manager.py_print("Parsing Errors :")
                Py_version_manager.py_print(*Parsing_Errors, sep="\n")
                Py_version_manager.py_print("")
            subprocess.call(['e2e_cli','dbaas', '-h'])


        elif (self.arguments.args.dbaas_commands is not None) and (self.arguments.args.action is not None):
              Py_version_manager.py_print("Only one action at a time !!")


        elif (self.arguments.args.dbaas_commands is not None):
            dbaas_class_object = DBaaSCrud(alias=self.arguments.args.alias, inputs=self.arguments.inputs)

            if self.arguments.args.dbaas_commands == 'create':
                try:
                    dbaas_class_object.create_dbaas()
                except KeyboardInterrupt:
                    Py_version_manager.py_print(" ")

            elif self.arguments.args.dbaas_commands == 'list' or self.arguments.args.dbaas_commands == 'ls':
                try:
                    dbaas_class_object.list_dbaas()
                except KeyboardInterrupt:
                    Py_version_manager.py_print(" ")

            elif self.arguments.args.dbaas_commands == 'delete':
                try:
                    dbaas_class_object.delete_dbaas_by_name()
                except KeyboardInterrupt:
                    Py_version_manager.py_print(" ")
        

        elif(self.arguments.args.action is not None):
            DBaas_operations=DBaasAction(alias=self.arguments.args.alias, inputs=self.arguments.inputs)     
            if(DBaas_operations.possible):
                operation = DBaas_operations.caller(
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