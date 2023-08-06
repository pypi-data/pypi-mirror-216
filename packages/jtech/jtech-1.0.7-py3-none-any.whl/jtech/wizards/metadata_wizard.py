import questionary
import getpass


class ProjectMetadataWizard:
    """
    Metadata for create project.
    """

    def __init__(self, project_name):
        self.project_name = project_name
        self.project_user = getpass.getuser()
        self.project_group = None
        self.project_artifact = None
        self.project_description = None
        self.project_package = None
        self.project_java = None
        self.project_spring = None

    def prompt_project_details(self):
        """
        Prompt to create Spring Boot project.
        """
        if self.project_name:
            self.project_name = questionary.text("Project name: ", default=self.project_name).ask()
        else:
            self.project_name = questionary.text("Project name: ").ask()

        self.project_group = questionary.text("Project Group:", default="br.com.sansys.services").ask()
        self.project_artifact = self.project_name
        self.project_description = questionary.text("Project Description:", default="Jtech Microservices v1.0").ask()
        package_default = self.project_group.replace("-", ".") + "." + self.project_artifact.replace("-", ".")
        self.project_package = questionary.text("Project package:", default=package_default).ask()
        self.project_java = questionary.select(
            "Select Java Version:",
            choices=["1.8", "11", "17", "19", "20"],
            default="17"
        ).ask()
        self.project_spring = questionary.select(
            "Select Spring Boot Version:",
            choices=["2.7.12", "3.0.7", "3.1.0"],
            default="3.0.7"
        ).ask()
        if not self.project_package:
            self.project_package = package_default

    def run(self):
        """
        Run prompt above.
        """
        self.prompt_project_details()
