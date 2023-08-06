import os
import getpass

from jtech.template_processor.template_processor import TemplateProcessor


class CqrsControllerGenerator:
    def __init__(self, package, project_name, cap_name, project_dir):
        self.package_name = package
        self.project_name = project_name
        self.cap_name = cap_name
        self.project_dir = project_dir

    def generate(self):
        target_filename_create = "Create" + self.cap_name + "Controller.java"
        target_filename_find = "Find" + self.cap_name + "ByIdController.java"
        cmd_controller = TemplateProcessor("./tpl/cqrs_cmd_controller.tpl",
                                           os.path.join(self.project_dir, "controllers/commands"))
        qry_controller = TemplateProcessor("./tpl/cqrs_qry_controller.tpl",
                                           os.path.join(self.project_dir, "controllers/queries"))
        data = {
            "package": self.package_name,
            "className": self.cap_name,
            "project": self.project_name,
            "username": getpass.getuser()
        }
        cmd_controller.process_template(data, target_filename_create)
        qry_controller.process_template(data, target_filename_find)
