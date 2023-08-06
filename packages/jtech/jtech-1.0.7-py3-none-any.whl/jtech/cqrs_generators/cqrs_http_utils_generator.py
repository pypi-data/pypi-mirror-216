import getpass

from jtech.utils.generator import Generator
import jtech.utils.dir_constants as source
import jtech.utils.tpl_constants as tpl


class CqrsHttpUtilsGenerator:
    """
    Generate CQRS HttpUtils

    :param project: Project name in lowercase
    :param capitalize: Project name Case Sensitive
    :param folder: Source for save file
    :param params: Metadata Params
    """

    def __init__(self, params, project, capitalize, folder):
        self.params = params
        self.project = project
        self.capitalize = capitalize
        self.folder = folder

    def generate(self):
        target = "HttpUtils.java"
        data = {
            "package": self.params.package,
            "className": self.capitalize,
            "project": self.project,
            "username": getpass.getuser()
        }
        generator = Generator(self.folder, data)
        generator.exec(tpl.CQRS_HTTP_UTILS, source.CQRS_UTILS, target)
