import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.volumes.volumes_crud.volumes import VolumesCrud
from e2e_cli.volumes.volumes_actions.volumes_action import volumesActions

class volumes_Routing:
    def __init__(self, arguments):
        self.arguments = arguments
        
        
    def route(self,  Parsing_Errors):
        if (self.arguments.args.action is None) and (self.arguments.args.volumes_commands is None):
            if(Parsing_Errors):
                Py_version_manager.py_print("Parsing Errors :")
                Py_version_manager.py_print(*Parsing_Errors, sep="\n")
                Py_version_manager.py_print("")
            subprocess.call(['e2e_cli', 'volumes', '-h'])


        elif (self.arguments.args.volumes_commands is not None) and (self.arguments.args.action is not None):
              Py_version_manager.py_print("Only one action at a time !!")


        elif(self.arguments.args.volumes_commands is not None):
            volumes_operations = VolumesCrud(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if(volumes_operations.possible):
                operation = volumes_operations.caller(
                    self.arguments.args.volumes_commands)
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
        # elif self.arguments.args.action == "attach_volume":
        #     volumes_operations = volumesActions(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
        #     if(volumes_operations.possible):
        #                 try:
        #                     volumes_operations.attach_volume()
        #                 except KeyboardInterrupt:
        #                     Py_version_manager.py_print(" ")

        # elif self.arguments.args.action == "desable_volumes":
        #     volumes_operations = volumesActions(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
        #     if(volumes_operations.possible):
        #                 try:
        #                     volumes_operations.disable_volumes()
        #                 except KeyboardInterrupt:
        #                     Py_version_manager.py_print(" ")
        
        
        else:
            Py_version_manager.py_print("command not found")
            if(Parsing_Errors):
                Py_version_manager.py_print("Parsing Errors :")
                Py_version_manager.py_print(*Parsing_Errors, sep="\n")