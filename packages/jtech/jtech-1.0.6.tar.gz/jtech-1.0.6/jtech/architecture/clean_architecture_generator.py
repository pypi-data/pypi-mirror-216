import os
import yaml
from jtech.clean_generators.clean_generator import CleanArchitectureGenerator
from jtech.docker_compose.generate_docker_compose import GenerateDockerCompose
from jtech.manipulate.application_yml_manipulator import ApplicationYmlManipulator
from jtech.manipulate.java_class_manipulator import JavaFileManipulator
from jtech.mockserver.mockserver import GenerateMockServer
from jtech.utils.file_remove import RemoveFile

import jtech.utils.dir_constants as const


class CleanArchitectureStructureCreator:
    """
    Generate clean architecture structure and sample files.

    :param param: DTO with all parameters.
    """

    def __init__(self, param):
        self.param = param

    def create_structure(self):
        """Create folder structure."""
        composer_dir, mockserver_dir, project_dir, resources_dir = self.generate_base_folder()
        self.generate_subfolders(project_dir)
        self.generate_docker_and_mockserver(composer_dir, mockserver_dir)
        project = self.generate_sample_files(project_dir)
        self.remove_application_properties(resources_dir)
        self.create_yaml(resources_dir, project, self.param.package)
        self.generate_docker_compose(composer_dir)
        self.generate_mockserver(mockserver_dir)

    def generate_mockserver(self, mockserver_dir):
        """Generate mockserver folder and add mockeserver"""
        mockserver = GenerateMockServer(path=mockserver_dir, param=self.param)
        mockserver.generate()

    def generate_docker_compose(self, composer_dir):
        docker_compose = GenerateDockerCompose(path=os.path.join(composer_dir, 'docker-compose.yml'), param=self.param)
        docker_compose.generate()

    def remove_application_properties(self, resources_dir):
        application_properties = RemoveFile(os.path.join(resources_dir, "application.properties"))
        application_properties.remove()

    def generate_sample_files(self, project_dir):
        names = self.param.project.split("-")
        real_name = names[-1]
        cap_name = real_name[0].upper() + real_name[1:]
        if self.param.samples:
            self.generate_samples(project_name=real_name, cap_name=cap_name, project_dir=project_dir)
        return real_name

    def generate_docker_and_mockserver(self, composer_dir, mockserver_dir):
        os.makedirs(composer_dir, exist_ok=True)
        os.makedirs(mockserver_dir, exist_ok=True)

    def generate_subfolders(self, project_dir):
        """Create subfolders for project"""
        os.makedirs(project_dir, exist_ok=True)
        subfolders = [
            const.CLEAN_DOMAINS,
            const.CLEAN_USECASE,
            const.CLEAN_PORT_INPUT,
            const.CLEAN_PORT_OUTPUT,
            const.CLEAN_ADAPTERS_INPUT_CONTROLLERS,
            const.CLEAN_ADAPTERS_INPUT_HANDLERS,
            const.CLEAN_ADAPTERS_INPUT_PROTOCOLS,
            const.CLEAN_ADAPTERS_OUTPUT_ENTITIES,
            const.CLEAN_CONFIG_INFRA_SWAGGER,
            const.CLEAN_CONFIG_INFRA_UTILS,
            const.CLEAN_CONFIG_INFRA_EXCEPTIONS,
            const.CLEAN_CONFIG_INFRA_HANDLERS,
            const.CLEAN_CONFIG_INFRA_LISTENERS,
            const.CLEAN_CONFIG_USECASES,
        ]

        for subfolder in subfolders:
            os.makedirs(os.path.join(project_dir), subfolder)

        if self.param.kafka:
            os.makedirs(os.path.join(project_dir, const.CLEAN_CONFIG_INFRA_KAFKA), exist_ok=True)
        if self.param.redis:
            os.makedirs(os.path.join(project_dir, const.CLEAN_CONFIG_INFRA_REDIS), exist_ok=True)

    def generate_base_folder(self):
        main_dir = os.path.join(self.param.base_dir, "src/main/java")
        resources_dir = os.path.join(self.param.base_dir, "src/main/resources")
        package_dir = self.param.package.replace(".", "/")
        project_dir = os.path.join(main_dir, package_dir)
        composer_dir = os.path.join(self.param.base_dir, "composer")
        mockserver_dir = os.path.join(self.param.base_dir, "mockserver")
        return composer_dir, mockserver_dir, project_dir, resources_dir

    def create_yaml(self, resources_dir, project, package):
        file = os.path.join(resources_dir, "application.yml")
        application = ApplicationYmlManipulator(file)
        application.generate_header(project, package)

        if self.param.kafka:
            application.generate_kafka_configuration()

        if self.param.redis:
            application.generate_redis_configuration()

        if self.param.is_jpa:
            application.generate_jpa_configuration()

        if self.param.mongo:
            application.generate_mongodb_configuration(project)

        if self.param.zipkin:
            application.generate_zipkin_configuration()

        if self.param.config_server:
            application.generate_config_server_configuration()

        if self.param.eureka_client:
            application.generate_eureka_client_configuration()

    def generate_samples(self, project_name, cap_name, project_dir):
        """Generate Clean Architecture sample files."""
        generator = CleanArchitectureGenerator(project_name, cap_name, project_dir, self.param)
        generator.all()

        manipulator = JavaFileManipulator(os.path.join(project_dir, "Start" + cap_name + ".java"))

        if self.param.redis & self.param.kafka:
            imports = [
                self.param.package + ".config.infra.kafka.KafkaConfiguration",
                self.param.package + ".config.infra.redis.RedisConfiguration",
                "org.springframework.context.annotation.Import"
            ]
            manipulator.add_import_to_class(["RedisConfiguration.class", "KafkaConfiguration.class"])
            manipulator.add_imports(imports)
        elif self.param.redis:
            imports = [
                self.param.package + ".config.infra.redis.RedisConfiguration",
                "org.springframework.context.annotation.Import"
            ]
            manipulator.add_import_to_class("RedisConfiguration.class")
            manipulator.add_imports(imports)
        elif self.param.kafka:
            imports = [
                self.param.package + ".config.infra.kafka.KafkaConfiguration",
                "org.springframework.context.annotation.Import"
            ]
            manipulator.add_import_to_class("KafkaConfiguration.class")
            manipulator.add_imports(imports)
