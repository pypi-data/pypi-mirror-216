from jtech.clean_generators.clean_adapter_generator import CleanAdapterGenerator
from jtech.clean_generators.clean_api_error_generator import CleanApiErrorGenerator
from jtech.clean_generators.clean_api_sub_error_generator import CleanApiSubErrorGenerator
from jtech.clean_generators.clean_api_validation_error_generator import CleanApiValidationErrorGenerator
from jtech.clean_generators.clean_config_generator import CleanConfigGenerator
from jtech.clean_generators.clean_controller_generator import CleanControllerGenerator
from jtech.clean_generators.clean_domain_generator import CleanDomainGenerator
from jtech.clean_generators.clean_entity_generator import CleanEntityGenerator
from jtech.clean_generators.clean_gen_id_generator import CleanGenIdGenerator
from jtech.clean_generators.clean_global_handler_generator import CleanGlobalExceptionHandlerGenerator
from jtech.clean_generators.clean_input_gateway_generator import CleanInputGatewayGenerator
from jtech.clean_generators.clean_jsons_generator import CleanJsonsGenerator
from jtech.clean_generators.clean_kafka_generator import CleanKafkaGenerator
from jtech.clean_generators.clean_openapi_generator import CleanOpenApiGenerator
from jtech.clean_generators.clean_output_gateway_generator import CleanOutputGatewayGenerator
from jtech.clean_generators.clean_ready_event_listener_generator import CleanReadyEventListenerGenerator
from jtech.clean_generators.clean_redis_generator import CleanRedisGenerator
from jtech.clean_generators.clean_repository_default_generator import CleanRepositoryDefaultGenerator
from jtech.clean_generators.clean_repository_jpa_generator import CleanRepositoryJpaGenerator
from jtech.clean_generators.clean_repository_mongo_generator import CleanRepositoryMongoGenerator
from jtech.clean_generators.clean_request_generator import CleanRequestGenerator
from jtech.clean_generators.clean_response_generator import CleanResponseGenerator
from jtech.clean_generators.clean_usecase_generator import CleanUseCaseGenerator


class CleanArchitectureGenerator:
    """
    Class for Generate all Java Classes

    :param project: Project name for use in lowercase.
    :param capitalize: Project name for use in uppercase.
    :param path: Source for create java file.
    :param param: DTO with all parameters to generate.
    """

    def __init__(self, project, capitalize, path, param):
        self.project = project
        self.capitalize = capitalize
        self.path = path
        self.param = param

    def gen_adapter(self):
        """Generate Adapter"""
        adapter = CleanAdapterGenerator(self.param.package, self.project, self.capitalize, self.path)
        adapter.generate()

    def gen_config(self):
        """Generate UseCase Configuration"""
        config = CleanConfigGenerator(self.param.package, self.project, self.capitalize, self.path)
        config.generate()

    def gen_controller(self):
        """Generate Create Controller"""
        controller = CleanControllerGenerator(self.param.package, self.project, self.capitalize, self.path)
        controller.generate()

    def gen_domain(self):
        """Generate Domain"""
        domain = CleanDomainGenerator(self.param.package, self.project, self.capitalize, self.path)
        domain.generate()

    def gen_entity(self):
        """Generate JPA or MongoDB Entity"""
        entity = CleanEntityGenerator(self.param.package, self.project, self.capitalize, self.path,
                                      self.param.spring_version, self.param.jpa, self.param.mongo)
        entity.generate()

    def gen_input_gateway(self):
        """Generate Create Input Gateway Interface"""
        gateway = CleanInputGatewayGenerator(self.param.package, self.project, self.capitalize, self.path)
        gateway.generate()

    def gen_output_gateway(self):
        """Generate Create Output Gateway Interface"""
        gateway = CleanOutputGatewayGenerator(self.param.package, self.project, self.capitalize, self.path)
        gateway.generate()

    def gen_repository(self):
        """Generate JPA or MongoDB repository"""
        if self.param.jpa:
            repository = CleanRepositoryJpaGenerator(self.param.package, self.project, self.capitalize, self.path)
            repository.generate()
        elif self.param.mongo:
            repository = CleanRepositoryMongoGenerator(self.param.package, self.project, self.capitalize,
                                                       self.path)
            repository.generate()
        else:
            repository = CleanRepositoryDefaultGenerator(self.param.package, self.project, self.capitalize,
                                                         self.path)
            repository.generate()

    def gen_request(self):
        """Generate Request Protocol"""
        request = CleanRequestGenerator(self.param.package, self.project, self.capitalize, self.path)
        request.generate()

    def gen_response(self):
        """Generate Response Protocol"""
        response = CleanResponseGenerator(self.param.package, self.project, self.capitalize, self.path)
        response.generate()

    def gen_usecase(self):
        """Generate UseCase"""
        usecase = CleanUseCaseGenerator(self.param.package, self.project, self.capitalize, self.path)
        usecase.generate()

    def gen_kafka_configuration(self):
        """Generate kafka Configuration if necessary"""
        kafka = CleanKafkaGenerator(self.param.package, self.path)
        kafka.generate()

    def gen_genid(self):
        """Generate GenId Utility class"""
        genid = CleanGenIdGenerator(self.param.package, self.path)
        genid.generate()

    def gen_api_error(self):
        """Generate API Error"""
        api_error = CleanApiErrorGenerator(self.param.package, self.path)
        api_error.generate()

    def gen_api_sub_error(self):
        """Generate API Sub Error Interface"""
        api_error = CleanApiSubErrorGenerator(self.param.package, self.path)
        api_error.generate()

    def gen_api_validation_error(self):
        """Generate API Validation Error"""
        api_error = CleanApiValidationErrorGenerator(self.param.package, self.path)
        api_error.generate()

    def gen_global_exception_handler(self):
        """Generate Global Exception Error Handler"""
        command = CleanGlobalExceptionHandlerGenerator(self.param.package, self.path)
        command.generate()

    def gen_jsons(self):
        """Generate JSON Parser utility"""
        command = CleanJsonsGenerator(self.param.package, self.path)
        command.generate()

    def gen_openapi(self):
        """Generate configuration OpenAPI"""
        command = CleanOpenApiGenerator(self.param.package, self.path)
        command.generate()

    def gen_redis_configuration(self):
        """Generate Redis Configuration if necessary"""
        command = CleanRedisGenerator(self.param.package, self.path)
        command.generate()

    def gen_ready_event_listener(self):
        """Generate Ready Event Listener for Spring Boot"""
        command = CleanReadyEventListenerGenerator(self.param.package, self.path)
        command.generate()

    def all(self):
        """Generate All methods above"""
        self.gen_adapter()
        self.gen_config()
        self.gen_controller()
        self.gen_domain()
        self.gen_entity()
        self.gen_input_gateway()
        self.gen_output_gateway()
        self.gen_repository()
        self.gen_request()
        self.gen_response()
        self.gen_usecase()
        self.gen_genid()
        self.gen_api_error()
        self.gen_api_sub_error()
        self.gen_api_validation_error()
        self.gen_global_exception_handler()
        self.gen_jsons()
        self.gen_openapi()
        self.gen_ready_event_listener()

        if self.param.kafka:
            self.gen_kafka_configuration()

        if self.param.redis:
            self.gen_redis_configuration()
