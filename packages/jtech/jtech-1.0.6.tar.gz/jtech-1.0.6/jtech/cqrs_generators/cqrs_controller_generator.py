import getpass

from jtech.utils.generator import Generator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as source


class CqrsControllerGenerator:
    def __init__(self, package, project_name, cap_name, project_dir):
        self.package_name = package
        self.project_name = project_name
        self.cap_name = cap_name
        self.project_dir = project_dir

    def generate(self):
        target_filename_create = "Create" + self.cap_name + "Controller.java"
        target_filename_find = "Find" + self.cap_name + "ByIdController.java"
        data = {
            "package": self.package_name,
            "className": self.cap_name,
            "project": self.project_name,
            "username": getpass.getuser()
        }
        generator = Generator(self.project_dir, data)
        generator.exec(tpl.CQRS_CONTROLLER_COMMAND, source.CQRS_CONTROLLERS_COMMANDS, target_filename_create)
        generator.exec(tpl.CQRS_CONTROLLER_QUERY, source.CQRS_CONTROLLERS_QUERIES, target_filename_find)
