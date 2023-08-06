import getpass
import os

from jtech.template_processor.template_processor import TemplateProcessor


class CleanGenIdGenerator:
    """
    Class for Create GenId Java Class

    :param package: Java package for change in template.
    :param project_dir: Source for create java file.
    """
    def __init__(self, package, project_dir):
        self.package_name = package
        self.project_dir = project_dir

    def generate(self):
        """Generate a Java Class with name: GenId.java"""
        target_filename = "GenId.java"
        processor = TemplateProcessor("../resources/tpl/clean_gen_id.tpl", os.path.join(self.project_dir, "config/infra/utils"))
        data = {
            "package": self.package_name,
            "username": getpass.getuser()
        }
        processor.process_template(data, target_filename)
