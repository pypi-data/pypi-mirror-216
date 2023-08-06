import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.auto_scaling.auto_scaling import AutoscalingCrud

class autoscaling_Routing:
    def __init__(self, arguments):
        self.arguments = arguments
        
        
    def route(self, Parsing_Errors):
        if (self.arguments.args.autoscaling_commands is None):
            if(Parsing_Errors):
                Py_version_manager.py_print("Parsing Errors :")
                Py_version_manager.py_print(*Parsing_Errors, sep="\n")
                Py_version_manager.py_print("")
            subprocess.call(['e2e_cli', 'autoscaling', '-h'])

        # elif (self.arguments.args.autoscaling_commands is not None) and (self.arguments.args.action is not None):
        #       Py_version_manager.py_print("Only one action at a time !!")

        elif(self.arguments.args.autoscaling_commands is not None):
            auto_scaling_operations = AutoscalingCrud(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if(auto_scaling_operations.possible):
                operation = auto_scaling_operations.caller(
                    self.arguments.args.autoscaling_commands)
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