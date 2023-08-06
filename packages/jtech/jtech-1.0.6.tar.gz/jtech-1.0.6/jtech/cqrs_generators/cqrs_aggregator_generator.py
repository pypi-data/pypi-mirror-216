import os
import getpass

from jtech.template_processor.template_processor import TemplateProcessor
from jtech.utils.generator import Generator
import jtech.utils.tpl_constants as tpl
import jtech.utils.dir_constants as sources


class CqrsAggregatorGenerator:
    def __init__(self, package, project_name, cap_name, project_dir):
        self.package_name = package
        self.project_name = project_name
        self.cap_name = cap_name
        self.project_dir = project_dir

    def generate(self):
        target_filename_interface = self.cap_name + "Aggregate.java"
        target_filename_impl = self.cap_name + "AggregateImpl.java"
        data = {
            "package": self.package_name,
            "className": self.cap_name,
            "project": self.project_name,
            "username": getpass.getuser()
        }
        generator = Generator(self.project_dir, data)
        generator.exec(tpl.CQRS_AGGREGATE, sources.CQRS_AGGREGATE, target_filename_interface)
        generator.exec(tpl.CQRS_AGGREGATE_IMPL, sources.CQRS_AGGREGATE_IMPL, target_filename_impl)
