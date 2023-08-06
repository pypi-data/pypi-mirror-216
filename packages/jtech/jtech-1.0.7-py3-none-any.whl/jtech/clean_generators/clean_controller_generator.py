import os
import getpass

from jtech.template_processor.template_processor import TemplateProcessor


class CleanControllerGenerator:
    """
    Class for Create Controller Java Class

    :param package: Java package for change in template.
    :param project_name: Project name for use in lowercase.
    :param capitalize: Project name for use in uppercase.
    :param project_dir: Source for create java file.
    """

    def __init__(self, package, project_name, capitalize, project_dir):
        self.package_name = package
        self.project_name = project_name
        self.capitalize = capitalize
        self.project_dir = project_dir

    def generate(self):
        """Generate class Create{{Project}}Controller.java"""
        target_filename = "Create" + self.capitalize + "Controller.java"
        processor = TemplateProcessor("../resources/tpl/clean_controller.tpl", os.path.join(self.project_dir,
                                                                           'adapters/input/controllers'))
        data = {
            "package": self.package_name,
            "className": self.capitalize,
            "project": self.project_name,
            "username": getpass.getuser()
        }
        processor.process_template(data, target_filename)
