import getpass
import os

from jtech.template_processor.template_processor import TemplateProcessor


class CleanRedisGenerator:
    """
    Class for Create RedisConfiguration Java Class

    :param package: Java package for change in template.
    :param project_dir: Source for create java file.
    """
    def __init__(self, package, project_dir):
        self.package_name = package
        self.project_dir = project_dir

    def generate(self):
        """Generate a Java Class with name: RedisConfiguration.java"""
        target_filename = "RedisConfiguration.java"
        processor = TemplateProcessor("../resources/tpl/clean_redis.tpl", os.path.join(self.project_dir, "config/infra/redis"))
        data = {
            "package": self.package_name,
            "username": getpass.getuser()
        }
        processor.process_template(data, target_filename)
