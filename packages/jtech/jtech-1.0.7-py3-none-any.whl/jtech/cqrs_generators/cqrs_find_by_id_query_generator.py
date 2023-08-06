import getpass

from jtech.utils.generator import Generator
import jtech.utils.dir_constants as source
import jtech.utils.tpl_constants as tpl


class CqrsFindByIdQueryGenerator:
    """
       Generate CQRS FindByIdQuery

       :param params: Params configurations
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
        target = "Find" + self.capitalize + "ByIdQuery.java"
        data = {
            "package": self.params.package,
            "className": self.capitalize,
            "project": self.project,
            "username": getpass.getuser()
        }
        generator = Generator(self.folder, data)
        generator.exec(tpl.CQRS_FIND_BY_ID_QUERY, source.CQRS_QUERY, target)
