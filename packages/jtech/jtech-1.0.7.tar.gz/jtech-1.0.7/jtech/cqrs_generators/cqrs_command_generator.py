import getpass

from jtech.utils.generator import Generator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as src


class CqrsCommandGenerator:
    """
    Generate CQRS Command

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
        target = "Create" + self.capitalize + "Command.java"
        data = {
            "package": self.params.package,
            "className": self.capitalize,
            "project": self.project,
            "username": getpass.getuser()
        }
        generator = Generator(self.folder, data)
        generator.exec(tpl.CQRS_CREATE_COMMAND, src.CQRS_COMMAND, target)
