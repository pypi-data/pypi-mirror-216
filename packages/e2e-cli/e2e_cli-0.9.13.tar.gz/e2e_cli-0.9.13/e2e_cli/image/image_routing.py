import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.image.image_crud.image import ImageCrud
from e2e_cli.image.image_listing.image_list import ImageListing

class ImageRouting:
    def __init__(self, arguments):
        self.arguments = arguments
        

    def route(self, Parsing_Errors):
        if (self.arguments.args.image_commands is None):
            if(Parsing_Errors):
                Py_version_manager.py_print("Parsing Errors :")
                Py_version_manager.py_print(*Parsing_Errors, sep="\n")
                Py_version_manager.py_print("")
            subprocess.call(['e2e_cli', 'image', '-h'])


        elif(self.arguments.args.image_commands is not None):
            image_operations = ImageCrud(alias=self.arguments.args.alias, inputs=self.arguments.inputs)
            if(image_operations.possible):
                operation = image_operations.caller(
                    self.arguments.args.image_commands)
                if operation:
                    try:
                        operation()
                    except KeyboardInterrupt:
                        Py_version_manager.py_print(" ")
        
                        
        # elif self.arguments.args.list_by == 'image_type':
        #     image_operations=ImageListing(alias=self.arguments.args.alias)     
        #     if(image_operations.possible):
        #                 try: 
        #                    image_operations.all()
        #                 except KeyboardInterrupt:
        #                     Py_version_manager.py_print(" ")

        else:
            Py_version_manager.py_print("command not found")
            if(Parsing_Errors):
                Py_version_manager.py_print("Parsing Errors :")
                Py_version_manager.py_print(*Parsing_Errors, sep="\n")