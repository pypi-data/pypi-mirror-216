from jtech.cqrs_generators.cqrs_api_error_generator import CqrsApiErrorGenerator
from jtech.cqrs_generators.cqrs_api_sub_error_generator import CqrsApiSubErrorGenerator
from jtech.cqrs_generators.cqrs_api_validation_error_generator import CqrsApiValidationErrorGenerator
from jtech.cqrs_generators.cqrs_command_generator import CqrsCommandGenerator
from jtech.cqrs_generators.cqrs_controller_generator import CqrsControllerGenerator
from jtech.cqrs_generators.cqrs_aggregator_generator import CqrsAggregatorGenerator
from jtech.cqrs_generators.cqrs_entity_generator import CqrsEntityGenerator
from jtech.cqrs_generators.cqrs_find_by_id_query_generator import CqrsFindByIdQueryGenerator
from jtech.cqrs_generators.cqrs_gen_id_generator import CqrsGenIdGenerator
from jtech.cqrs_generators.cqrs_global_handler_generator import CqrsGlobalExceptionHandlerGenerator
from jtech.cqrs_generators.cqrs_http_utils_generator import CqrsHttpUtilsGenerator
from jtech.cqrs_generators.cqrs_jsons_generator import CqrsJsonsGenerator
from jtech.cqrs_generators.cqrs_kafka_generator import CqrsKafkaGenerator
from jtech.cqrs_generators.cqrs_openapi_generator import CqrsOpenApiGenerator
from jtech.cqrs_generators.cqrs_redis_generator import CqrsRedisGenerator
from jtech.cqrs_generators.cqrs_repository_default_generator import CqrsRepositoryDefaultGenerator
from jtech.cqrs_generators.cqrs_repository_jpa_generator import CqrsRepositoryJpaGenerator
from jtech.cqrs_generators.cqrs_repository_mongo_generator import CqrsRepositoryMongoGenerator
from jtech.cqrs_generators.cqrs_request_generator import CqrsRequestGenerator
from jtech.cqrs_generators.cqrs_response_generator import CqrsResponseGenerator
from jtech.cqrs_generators.cqrs_service_generator import CqrsServicesGenerator


class CqrsArchitectureGenerator:
    """
    Class for generate All CQRS Samples
    :param project:
    """

    def __init__(self, project, capitalize, path, param):
        self.project = project
        self.capitalize = capitalize
        self.path = path
        self.param = param

    def gen_aggregate(self):
        aggregate = CqrsAggregatorGenerator(self.param.package, self.project, self.capitalize, self.path)
        aggregate.generate()

    def gen_controllers(self):
        controllers = CqrsControllerGenerator(self.param.package, self.project, self.capitalize, self.path)
        controllers.generate()

    def gen_exceptions(self):
        api_error = CqrsApiErrorGenerator(self.param, self.project, self.capitalize, self.path)
        error_sub = CqrsApiSubErrorGenerator(self.param, self.project, self.capitalize, self.path)
        error_validation = CqrsApiValidationErrorGenerator(self.param, self.project, self.capitalize, self.path)
        error_handler = CqrsGlobalExceptionHandlerGenerator(self.param, self.project, self.capitalize, self.path)
        api_error.generate()
        error_handler.generate()
        error_sub.generate()
        error_validation.generate()

    def gen_kafka_configuration(self):
        kafka = CqrsKafkaGenerator(self.param, self.project, self.capitalize, self.path)
        kafka.generate()

    def gen_redis_configuration(self):
        redis = CqrsRedisGenerator(self.param, self.project, self.capitalize, self.path)
        redis.generate()

    def gen_create_command(self):
        command = CqrsCommandGenerator(self.param, self.project, self.capitalize, self.path)
        command.generate()

    def gen_entity(self):
        entity = CqrsEntityGenerator(self.param, self.project, self.capitalize, self.path)
        entity.generate()

    def gen_find_by_id_query(self):
        query = CqrsFindByIdQueryGenerator(self.param, self.project, self.capitalize, self.path)
        query.generate()

    def gen_genid(self):
        genid = CqrsGenIdGenerator(self.param, self.path)
        genid.generate()

    def gen_httputils(self):
        httputils = CqrsHttpUtilsGenerator(self.param, self.project, self.capitalize, self.path)
        httputils.generate()

    def gen_jsons(self):
        jsons = CqrsJsonsGenerator(self.param, self.path)
        jsons.generate()

    def gen_openapi(self):
        openapi = CqrsOpenApiGenerator(self.param, self.project, self.capitalize, self.path)
        openapi.generate()

    def gen_repository(self):
        if self.param.jpa:
            repository = CqrsRepositoryJpaGenerator(self.param, self.project, self.capitalize, self.path)
        elif self.param.mongo:
            repository = CqrsRepositoryMongoGenerator(self.param, self.project, self.capitalize, self.path)
        else:
            repository = CqrsRepositoryDefaultGenerator(self.param, self.project, self.capitalize, self.path)

        repository.generate()

    def gen_request(self):
        request = CqrsRequestGenerator(self.param, self.project, self.capitalize, self.path)
        request.generate()

    def gen_response(self):
        response = CqrsResponseGenerator(self.param, self.project, self.capitalize, self.path)
        response.generate()

    def gen_services(self):
        services = CqrsServicesGenerator(self.param, self.project, self.capitalize, self.path)
        services.generate()

    def all(self):
        self.gen_aggregate()
        self.gen_controllers()
        self.gen_response()
        self.gen_services()
        self.gen_request()
        self.gen_openapi()
        self.gen_entity()
        self.gen_jsons()
        self.gen_genid()
        self.gen_create_command()
        self.gen_exceptions()
        self.gen_find_by_id_query()
        self.gen_httputils()
        self.gen_repository()

        if self.param.kafka:
            self.gen_kafka_configuration()

        if self.param.redis:
            self.gen_redis_configuration()
