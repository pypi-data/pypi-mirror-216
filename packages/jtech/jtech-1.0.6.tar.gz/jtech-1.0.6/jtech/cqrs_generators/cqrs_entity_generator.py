import os
import getpass

import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as source
from jtech.utils.generator import Generator


class CqrsEntityGenerator:
    """
    Class for create Entity Java Class

    :param project: Project name for use in lowercase
    :param capitalize: Project name for use in uppercase like name class
    :param folder: Source create java file
    :param param: Configurations params

    """

    def __init__(self, param, project, capitalize, folder):
        self.project = project
        self.capitalize = capitalize
        self.folder = folder
        self.param = param

    def generate(self):
        """Generate entity class {{Project}}Entity.java"""
        target_filename = self.capitalize + "Entity.java"
        if self.param.spring_version.startswith("3") & self.param.jpa:
            template = tpl.CQRS_ENTITY_JPA_3
        elif self.param.spring_version.startswith("2") & self.param.jpa:
            template = tpl.CQRS_ENTITY_JPA_2
        elif self.param.mongo:
            template = tpl.CQRS_ENTITY_MONGO
        else:
            template = tpl.CQRS_DEFAULT_ENTITY

        data = {
            "package": self.param.package,
            "className": self.capitalize,
            "project": self.project,
            "username": getpass.getuser()
        }
        generator = Generator(self.folder, data)
        generator.exec(template, source.CQRS_ENTITIES, target_filename)
