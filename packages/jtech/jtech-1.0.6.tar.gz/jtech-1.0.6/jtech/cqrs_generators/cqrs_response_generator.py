import getpass

import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.utils.generator import Generator


class CqrsResponseGenerator:
    """
        Generate CQRS Response

        :param params: Package name for use in template
        :param project: Project name in lowercase
        :param capitalize: Project name Case Sensitive
        :param folder: Source for save file
        """

    def __init__(self, params, project, capitalize, folder):
        self.params = params
        self.project = project
        self.capitalize = capitalize
        self.folder = folder

    def generate(self):
        target = self.capitalize + "Response.java"
        data = {
            "package": self.params.package,
            "className": self.capitalize,
            "project": self.project,
            "username": getpass.getuser()
        }
        generator = Generator(self.folder, data)
        generator.exec(tpl.CQRS_RESPONSE, src.CQRS_PROTOCOLS, target)
