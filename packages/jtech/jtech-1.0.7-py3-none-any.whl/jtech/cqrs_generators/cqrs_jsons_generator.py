import getpass
import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl

from jtech.utils.generator import Generator


class CqrsJsonsGenerator:
    """
    Class for Create Jsons Java Class

    :param params: Java package for change in template.
    :param folder: Source for create java file.
    """

    def __init__(self, params, folder):
        self.params = params
        self.folder = folder

    def generate(self):
        """Generate a Java Class with name: Jsons.java"""
        target_filename = "Jsons.java"
        data = {
            "package": self.params.package,
            "username": getpass.getuser()
        }
        generator = Generator(self.folder, data)
        generator.exec(tpl.CQRS_JSONS, src.CQRS_UTILS, target_filename)
