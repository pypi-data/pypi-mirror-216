import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.node.node_crud.node import NodeCrud
from e2e_cli.node.node_actions.node_action import NodeActions


class NodeRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self, Parsing_Errors):
        if (self.arguments.args.node_commands is None) and (self.arguments.args.action is None):
            if (Parsing_Errors):
                Py_version_manager.py_print("Parsing Errors :")
                Py_version_manager.py_print(*Parsing_Errors, sep="\n")
                Py_version_manager.py_print("")
            subprocess.call(['e2e_cli', 'node', '-h'])


        elif (self.arguments.args.node_commands is not None) and (self.arguments.args.action is not None):
            Py_version_manager.py_print("Only one action at a time !!")


        elif (self.arguments.args.node_commands is not None):
            Node_operations = NodeCrud(
                alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if (Node_operations.possible):
                operation = Node_operations.caller(
                    self.arguments.args.node_commands)
                if (operation):
                    operation()


        elif (self.arguments.args.action is not None):
            Node_operations = NodeActions(
                alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if (Node_operations.possible):
                operation = Node_operations.caller(
                    self.arguments.args.action)
                if (operation):
                    operation()

                else:
                    Py_version_manager.py_print("command not found")
                    if (Parsing_Errors):
                        Py_version_manager.py_print("Parsing Errors :")
                        Py_version_manager.py_print(*Parsing_Errors, sep="\n")


        else:
            Py_version_manager.py_print("command not found")
            if (Parsing_Errors):
                Py_version_manager.py_print("Parsing Errors :")
                Py_version_manager.py_print(*Parsing_Errors, sep="\n")
