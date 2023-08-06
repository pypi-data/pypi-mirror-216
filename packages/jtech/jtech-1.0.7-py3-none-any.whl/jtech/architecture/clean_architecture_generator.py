import os
import yaml
from jtech.clean_generators.clean_generator import CleanArchitectureGenerator
from jtech.docker_compose.generate_docker_compose import GenerateDockerCompose
from jtech.manipulate.application_yml_manipulator import ApplicationYmlManipulator
from jtech.manipulate.java_class_manipulator import JavaFileManipulator
from jtech.mockserver.mockserver import GenerateMockServer
from jtech.utils.file_remove import RemoveFile


class CleanArchitectureStructureCreator:
    """
    Generate clean architecture structure and sample files.

    :param param: DTO with all parameters.
    """

    def __init__(self, param):
        self.param = param

    def create_structure(self):
        """Create folder structure."""
        main_dir = os.path.join(self.param.base_dir, "src/main/java")
        resources_dir = os.path.join(self.param.base_dir, "src/main/resources")
        package_dir = self.param.package.replace(".", "/")
        project_dir = os.path.join(main_dir, package_dir)
        composer_dir = os.path.join(self.param.base_dir, "composer")
        mockserver_dir = os.path.join(self.param.base_dir, "mockserver")

        # Create folders
        os.makedirs(project_dir, exist_ok=True)
        os.makedirs(os.path.join(project_dir, "application/core/domains"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "application/core/usecases"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "application/ports/input"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "application/ports/output"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "adapters/input/controllers"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "adapters/input/handlers"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "adapters/input/protocols"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "adapters/output/repositories/entities"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "config/infra/swagger"), exist_ok=True)

        if self.param.kafka:
            os.makedirs(os.path.join(project_dir, "config/infra/kafka"), exist_ok=True)
        if self.param.redis:
            os.makedirs(os.path.join(project_dir, "config/infra/redis"), exist_ok=True)

        os.makedirs(os.path.join(project_dir, "config/infra/utils"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "config/infra/exceptions"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "config/infra/handlers"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "config/infra/listeners"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "config/usecases"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "config/infra"), exist_ok=True)

        os.makedirs(composer_dir, exist_ok=True)
        os.makedirs(mockserver_dir, exist_ok=True)

        names = self.param.project.split("-")
        real_name = names[-1]
        cap_name = real_name[0].upper() + real_name[1:]
        if self.param.samples:
            self.generate_samples(project_name=real_name, cap_name=cap_name, project_dir=project_dir)

        application_properties = RemoveFile(os.path.join(resources_dir, "application.properties"))
        application_properties.remove()

        self.create_yaml(os.path.join(resources_dir, "application.yml"), real_name, self.param.package)

        docker_compose = GenerateDockerCompose(path=os.path.join(composer_dir, 'docker-compose.yml'), param=self.param)
        docker_compose.generate()

        mockserver = GenerateMockServer(path=mockserver_dir, param=self.param)
        mockserver.generate()

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
