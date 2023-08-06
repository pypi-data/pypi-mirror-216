import os
import getpass

from jtech.template_processor.template_processor import TemplateProcessor


class CqrsAggregatorGenerator:
    def __init__(self, package, project_name, cap_name, project_dir):
        self.package_name = package
        self.project_name = project_name
        self.cap_name = cap_name
        self.project_dir = project_dir

    def generate(self):
        target_filename_interface = self.cap_name + "Aggregate.java"
        target_filename_impl = self.cap_name + "AggregateImpl.java"
        processor_interface = TemplateProcessor("./tpl/cqrs_aggregate.tpl", os.path.join(self.project_dir, "aggregate"))
        processor_impl = TemplateProcessor("./tpl/cqrs_aggregate_impl.tpl", os.path.join(self.project_dir, "aggregate/impl"))
        data = {
            "package": self.package_name,
            "className": self.cap_name,
            "project": self.project_name,
            "username": getpass.getuser()
        }
        processor_interface.process_template(data, target_filename_interface)
        processor_impl.process_template(data, target_filename_impl)
