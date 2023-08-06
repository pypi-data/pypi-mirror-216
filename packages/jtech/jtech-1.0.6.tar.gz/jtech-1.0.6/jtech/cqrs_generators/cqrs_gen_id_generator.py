import getpass
import os
import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl

from jtech.utils.generator import Generator


class CqrsGenIdGenerator:
    """
    Class for Create GenId Java Class

    :param params: Java package for change in template.
    :param folder: Source for create java file.
    """

    def __init__(self, params, folder):
        self.params = params
        self.folder = folder

    def generate(self):
        """Generate a Java Class with name: GenId.java"""
        target_filename = "GenId.java"
        data = {
            "package": self.params.package,
            "username": getpass.getuser()
        }
        generator = Generator(self.folder, data)
        generator.exec(tpl.CQRS_GEN_ID, src.CQRS_UTILS, target_filename)
