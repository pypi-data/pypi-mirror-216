import getpass
import os

from jtech.template_processor.template_processor import TemplateProcessor


class CleanGlobalExceptionHandlerGenerator:
    """
    Class for Create Global Exception Handler Java Class

    :param package: Java package for change in template.
    :param project_dir: Source for create java file.
    """
    def __init__(self, package, project_dir):
        self.package_name = package
        self.project_dir = project_dir

    def generate(self):
        """Generate a Java Class with name: GlobalExceptionHandler.java"""
        target_filename = "GlobalExceptionHandler.java"
        processor = TemplateProcessor("../resources/tpl/clean_global_handler.tpl", os.path.join(self.project_dir, "config/infra/handlers"))
        data = {
            "package": self.package_name,
            "username": getpass.getuser()
        }
        processor.process_template(data, target_filename)
