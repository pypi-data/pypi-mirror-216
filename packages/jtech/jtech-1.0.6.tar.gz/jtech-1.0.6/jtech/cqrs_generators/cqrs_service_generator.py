import getpass

import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.utils.generator import Generator


class CqrsServicesGenerator:
    """
        Generate CQRS Services

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
        target_interface = "Create" + self.capitalize + "Service.java"
        target_impl = "Create" + self.capitalize + "ServiceImpl.java"
        target_query_interface = "Find" + self.capitalize + "ByIdService.java"
        target_query_impl = "Find" + self.capitalize + "ByIdServiceImpl.java"
        data = {
            "package": self.params.package,
            "className": self.capitalize,
            "project": self.project,
            "username": getpass.getuser()
        }
        generator = Generator(self.folder, data)
        generator.exec(tpl.CQRS_SERVICE_COMMAND, src.CQRS_SERVICES_COMMANDS, target_interface)
        generator.exec(tpl.CQRS_SERVICE_COMMAND_IMPL, src.CQRS_SERVICES_COMMANDS_IMPL, target_impl)
        generator.exec(tpl.CQRS_SERVICE_QUERY, src.CQRS_SERVICES_QUERIES, target_query_interface)
        generator.exec(tpl.CQRS_SERVICE_QUERY_IMPL, src.CQRS_SERVICES_QUERIES_IMPL, target_query_impl)
