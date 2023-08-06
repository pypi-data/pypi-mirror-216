import os
import getpass

from jtech.template_processor.template_processor import TemplateProcessor


class CleanEntityGenerator:
    """
    Class for Create Entity Java Class

    :param package: Java package for change in template.
    :param project_name: Project name for use in lowercase.
    :param capitalize: Project name for use in uppercase.
    :param project_dir: Source for create java file.
    :param spring_version: Spring version 3.x or 2.7.x
    :param jpa: Is JPA
    :param mongo: Is MongoDB
    """

    def __init__(self, package, project_name, capitalize, project_dir, spring_version, jpa=False, mongo=False):
        self.package_name = package
        self.project_name = project_name
        self.capitalize = capitalize
        self.project_dir = project_dir
        self.spring_version = spring_version
        self.is_jpa = jpa
        self.is_mongodb = mongo

    def generate(self):
        """Generate entity class {{Project}}Entity.java"""
        target_filename = self.capitalize + "Entity.java"
        if self.spring_version.startswith("3") & self.is_jpa:
            template = "../resources/tpl/clean_jpa_entity3.tpl"
        elif self.spring_version.startswith("2") & self.is_jpa:
            template = "../resources/tpl/clean_jpa_entity2.tpl"
        elif self.is_mongodb:
            template = "../resources/tpl/clean_mongo_entity.tpl"
        else:
            template = "../resources/tpl/clean_entity.tpl"

        processor = TemplateProcessor(template, os.path.join(self.project_dir, "adapters/output"
                                                                               "/repositories/entities"))
        data = {
            "package": self.package_name,
            "className": self.capitalize,
            "project": self.project_name,
            "username": getpass.getuser()
        }
        processor.process_template(data, target_filename)
