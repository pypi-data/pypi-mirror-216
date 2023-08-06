import getpass
import os

from jtech.template_processor.template_processor import TemplateProcessor


class CleanOpenApiGenerator:
    """
    Class for Create OpenAPI30Configuration Configuration Java Class

    :param package: Java package for change in template.
    :param project_dir: Source for create java file.
    """
    def __init__(self, package, project_dir):
        self.package_name = package
        self.project_dir = project_dir

    def generate(self):
        """Generate a Java Class with name: OpenAPI30Configuration.java"""
        target_filename = "OpenAPI30Configuration.java"
        processor = TemplateProcessor("../resources/tpl/clean_openapi.tpl", os.path.join(self.project_dir, "config/infra/swagger"))
        data = {
            "package": self.package_name,
            "username": getpass.getuser()
        }
        processor.process_template(data, target_filename)
