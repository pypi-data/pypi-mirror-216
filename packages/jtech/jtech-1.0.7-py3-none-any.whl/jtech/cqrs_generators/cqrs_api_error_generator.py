import getpass

from jtech.utils.generator import Generator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as source


class CqrsApiErrorGenerator:
    def __init__(self, params, project, capitalize, folder):
        self.params = params
        self.project = project
        self.capitalize = capitalize
        self.folder = folder

    def generate(self):
        target = "ApiError.java"
        data = {
            "package": self.params.package,
            "className": self.capitalize,
            "project": self.folder,
            "username": getpass.getuser()
        }
        generator = Generator(self.folder, data)
        generator.exec(tpl.CQRS_API_ERROR, source.CQRS_INFRA_EXCEPTIONS, target)
