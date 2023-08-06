import os
import getpass

from jtech.template_processor.template_processor import TemplateProcessor


class CleanRepositoryDefaultGenerator:
    """
    Class for Create Default Repository Java Class

    :param package: Java package for change in template.
    :param project_name: Project name for use in lowercase.
    :param cap_name: Project name for use in uppercase.
    :param project_dir: Source for create java file.

    Generate a Generic interface for use.
    """

    def __init__(self, package, project_name, cap_name, project_dir):
        self.package_name = package
        self.project_name = project_name
        self.cap_name = cap_name
        self.project_dir = project_dir

    def generate(self):
        """Generate repository interface {{Project}}Repository.java extended to MongoRepository"""
        target_filename = self.cap_name + "Repository.java"
        processor = TemplateProcessor("../resources/tpl/clean_repository_default.tpl",
                                      os.path.join(self.project_dir, "adapters/output"
                                                                     "/repositories"))
        data = {
            "package": self.package_name,
            "className": self.cap_name,
            "project": self.project_name,
            "username": getpass.getuser()
        }
        processor.process_template(data, target_filename)
