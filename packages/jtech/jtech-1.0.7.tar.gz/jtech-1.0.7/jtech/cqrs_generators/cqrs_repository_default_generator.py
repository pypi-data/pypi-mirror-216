import getpass

from jtech.utils.generator import Generator
import jtech.utils.dir_constants as source
import jtech.utils.tpl_constants as tpl


class CqrsRepositoryDefaultGenerator:
    """
        Generate CQRS Default Repository

        :param params: Metadata params
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
        target = self.capitalize + "Repository.java"
        data = {
            "package": self.params.package,
            "className": self.capitalize,
            "project": self.project,
            "username": getpass.getuser()
        }
        generator = Generator(self.folder, data)
        generator.exec(tpl.CQRS_REPOSITORY_DEFAULT, source.CQRS_REPOSITORIES, target)
