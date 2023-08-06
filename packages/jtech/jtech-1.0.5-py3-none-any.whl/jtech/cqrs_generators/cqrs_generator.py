from jtech.cqrs_generators.cars_controller_template import CqrsControllerGenerator
from jtech.cqrs_generators.cqrs_aggregator_template import CqrsAggregatorGenerator


class CqrsGenerator:
    def __init__(self, project, package, capitalize, path, jpa=False, mongo=False):
        self.project = project
        self.package = package
        self.capitalize = capitalize
        self.path = path
        self.jpa = jpa
        self.mongo = mongo

    def gen_aggregate(self):
        aggregate = CqrsAggregatorGenerator(package=self.package, project_name=self.project, cap_name=self.capitalize,
                                            project_dir=self.path)
        aggregate.generate()

    def gen_controllers(self):
        controllers = CqrsControllerGenerator(package=self.package, project_name=self.project, cap_name=self.capitalize,
                                              project_dir=self.path)
        controllers.generate()

    def all(self):
        self.gen_aggregate()
        self.gen_controllers()
