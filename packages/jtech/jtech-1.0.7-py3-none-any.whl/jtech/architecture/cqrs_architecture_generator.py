import os

from jtech.cqrs_generators.cqrs_generator import CqrsArchitectureGenerator
from jtech.docker_compose.generate_docker_compose import GenerateDockerCompose
from jtech.manipulate.application_yml_manipulator import ApplicationYmlManipulator
from jtech.manipulate.java_class_manipulator import JavaFileManipulator
from jtech.mockserver.mockserver import GenerateMockServer
from jtech.utils.file_remove import RemoveFile
import jtech.utils.dir_constants as const


class CqrsArchitectureStructureCreator:
    """
    Generate cqrs architecture structure and sample files.

    :param param: DTO with all parameters.
    """

    def __init__(self, param):
        self.param = param

    def create_structure(self):
        """Create folder structure."""
        composer_dir, mockserver_dir, project_dir, resources_dir = self.generate_base_folder()
        self.create_subfolders(project_dir)
        self.generate_docker_mockserver(composer_dir, mockserver_dir)
        real_name = self.create_samples(project_dir)
        self.remove_application_properties(resources_dir)
        self.create_yaml(os.path.join(resources_dir, "application.yml"), real_name, self.param.package)
        self.create_docker_compose(composer_dir)
        self.create_mockserver(mockserver_dir)

    def generate_docker_mockserver(self, composer_dir, mockserver_dir):
        os.makedirs(composer_dir, exist_ok=True)
        os.makedirs(mockserver_dir, exist_ok=True)

    def generate_base_folder(self):
        main_dir = os.path.join(self.param.base_dir, "src/main/java")
        resources_dir = os.path.join(self.param.base_dir, "src/main/resources")
        package_dir = self.param.package.replace(".", "/")
        project_dir = os.path.join(main_dir, package_dir)
        composer_dir = os.path.join(self.param.base_dir, "composer")
        mockserver_dir = os.path.join(self.param.base_dir, "mockserver")
        return composer_dir, mockserver_dir, project_dir, resources_dir

    def create_samples(self, folder):
        names = self.param.project.split("-")
        project = names[-1]
        capitalize = project[0].upper() + project[1:]
        if self.param.samples:
            self.generate_samples(project, capitalize, folder)
        return project

    def remove_application_properties(self, resources_dir):
        application_properties = RemoveFile(os.path.join(resources_dir, "application.properties"))
        application_properties.remove()

    def create_docker_compose(self, composer_dir):
        docker_compose = GenerateDockerCompose(path=os.path.join(composer_dir, 'docker-compose.yml'), param=self.param)
        docker_compose.generate()

    def create_mockserver(self, mockserver_dir):
        mockserver = GenerateMockServer(path=mockserver_dir, param=self.param)
        mockserver.generate()

    def create_subfolders(self, project_dir):
        """Create subfolders in the project directory."""
        subfolders = [
            const.CQRS_AGGREGATE_IMPL,
            const.CQRS_CONTROLLERS_COMMANDS,
            const.CQRS_CONTROLLERS_QUERIES,
            const.CQRS_ENTITIES,
            const.CQRS_INFRA,
            const.CQRS_INFRA_EXCEPTIONS,
            const.CQRS_PROTOCOLS,
            const.CQRS_REPOSITORIES,
            const.CQRS_COMMAND,
            const.CQRS_SERVICES_COMMANDS_IMPL,
            const.CQRS_QUERY,
            const.CQRS_SERVICES_QUERIES_IMPL,
            const.CQRS_UTILS,
            const.CQRS_VALIDATOR
        ]

        for subfolder in subfolders:
            os.makedirs(os.path.join(project_dir, subfolder), exist_ok=True)

    def create_yaml(self, file, project, package):
        application = ApplicationYmlManipulator(file)
        application.generate_header(project, package)

        if self.param.kafka:
            application.generate_kafka_configuration()

        if self.param.redis:
            application.generate_redis_configuration()

        if self.param.jpa:
            application.generate_jpa_configuration()

        if self.param.mongo:
            application.generate_mongodb_configuration(project)

        if self.param.zipkin:
            application.generate_zipkin_configuration()

        if self.param.config_server:
            application.generate_config_server_configuration()

        if self.param.eureka_client:
            application.generate_eureka_client_configuration()

    def generate_samples(self, project, capitalize, folder):
        generator = CqrsArchitectureGenerator(project, capitalize, folder, self.param)
        generator.all()

        file = os.path.join(folder, "Start" + capitalize + ".java")
        manipulator = JavaFileManipulator(file)

        if self.param.redis & self.param.kafka:
            imports = [
                self.param.package + ".infra.KafkaConfiguration",
                self.param.package + ".infra.RedisConfiguration",
                "org.springframework.context.annotation.Import"
            ]
            manipulator.add_import_to_class(["RedisConfiguration.class", "KafkaConfiguration.class"])
            manipulator.add_imports(imports)
        elif self.param.redis:
            imports = [
                self.param.package + ".infra.RedisConfiguration",
                "org.springframework.context.annotation.Import"
            ]
            manipulator.add_import_to_class("RedisConfiguration.class")
            manipulator.add_imports(imports)
        elif self.param.kafka:
            imports = [
                self.param.package + ".infra.KafkaConfiguration",
                "org.springframework.context.annotation.Import"
            ]
            manipulator.add_import_to_class("KafkaConfiguration.class")
            manipulator.add_imports(imports)
