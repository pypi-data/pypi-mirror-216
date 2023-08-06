from jtech.architecture.clean_architecture_generator import CleanArchitectureStructureCreator
from jtech.creators.gradle_properties_creator import GradlePropertiesCreator
from jtech.creators.readme_creator import ReadmeCreator
from jtech.manipulate.build_gradle_manipulator import BuildGradleManipulator
from jtech.utils.file_remove import RemoveFile
from jtech.utils.param_configuration import ParamConfiguration
from jtech.utils.tar_gz_extractor import TarGzExtractor
from jtech.webclient.spring_boot_client import SpringBootWebClient
from jtech.wizards.architecture_choice_wizard import ArchitectureChoiceWizard
from jtech.wizards.checkbox_wizard import CheckboxWizard
from jtech.wizards.metadata_wizard import ProjectMetadataWizard
from jtech.wizards.project import Project
from jtech.wizards.samples_choice_wizard import SampleChoiceWizard
import json
import pkg_resources


class CreateProject:

    def create(self, project_name=None):
        """Template Method for create a Spring Boot Project"""
        # Load options from json
        options = self.load_options()
        # Load Metadata from user
        metadata = ProjectMetadataWizard(project_name)
        metadata.run()
        # Select default dependencies
        choice_dependencies = CheckboxWizard(options)
        selected_dependencies = choice_dependencies.run()
        # Select default architecture
        choice_architecture = ArchitectureChoiceWizard(["Clean", "CQRS", "Default"])
        selected_architecture = choice_architecture.run()
        # Choice generate with samples or not
        choice_with_samples = SampleChoiceWizard(["yes", "no"])
        sample_selected = choice_with_samples.run()
        # Create Project DTO
        project = self.make_project_class(metadata, selected_dependencies)
        # Download default project from Spring Start
        filename = self.download_default_project(project)
        # Extract downloaded project em exclude own zip file
        self.extract_default_project_and_delete_zip(filename)
        # Create folder, files and configurations by architecture
        if selected_architecture == "Clean":
            self.create_clean_architecture(project, sample_selected, selected_dependencies)
        # Add libs, plugins and others
        self.manipulate_build_gradle(project, selected_dependencies)
        # Create gradle.properties file
        self.create_gradle_properties(project)
        # Remove files unnecessary
        self.remove_unnecessary_files(project)

    def create_gradle_properties(self, project):
        """Create Gradle Properties file"""
        generator = GradlePropertiesCreator("./" + project.get_name() + "/gradle.properties")
        generator.create_gradle_properties()

    def remove_unnecessary_files(self, project):
        """Remove unnecessary files"""
        readme = ReadmeCreator("./" + project.get_name() + "/README.md", project.get_name())
        readme.create_readme()
        help_markdown_file = RemoveFile("./" + project.get_name() + "/HELP.md")
        help_markdown_file.remove()

    def manipulate_build_gradle(self, project, selected_dependencies):
        """Manipulate build.gradle"""
        if project.get_spring().startswith("3"):
            spring_doc = "org.springdoc:springdoc-openapi-starter-webmvc-ui:2.0.4"
        else:
            spring_doc = "org.springdoc:springdoc-openapi-ui:1.6.15"
        dependency = [
            spring_doc,
            "org.projectlombok:lombok",
            "org.springframework.boot:spring-boot-starter-web"
        ]
        has_jpa = "data-jpa" in selected_dependencies
        if has_jpa:
            dependency.append('org.hibernate.validator:hibernate-validator:8.0.0.Final')
        manipulator = BuildGradleManipulator('./' + project.get_name() + '/build.gradle')
        manipulator.add_repository("https://nexus.jtech.com.br/repository/maven-public")
        manipulator.update_version("APP_VERSION")
        manipulator.add_publishing()
        manipulator.add_plugin_ids()
        manipulator.add_dependencies(dependency)

    def create_clean_architecture(self, project, sample_selected, selected_dependencies):
        """Create Clean Architecture Structure"""
        param = self.extract_parameters(project, sample_selected, selected_dependencies)
        clean_architecture = CleanArchitectureStructureCreator(param)
        clean_architecture.create_structure()

    def extract_parameters(self, project, sample_selected, selected_dependencies):
        """Create ParamConfiguration DTO"""
        has_jpa = "data-jpa" in selected_dependencies
        has_mongo = "data-mongodb" in selected_dependencies
        has_redis = "data-redis" in selected_dependencies
        has_kafka = "kafka" in selected_dependencies
        has_eureka_client = "cloud-eureka" in selected_dependencies
        has_config_server = "cloud-config-client" in selected_dependencies
        has_zipkin = "zipkin" in selected_dependencies
        generate_sample = "yes" in sample_selected
        has_rabbit = "amqp" in selected_dependencies
        param = ParamConfiguration("./" + project.get_name(), project.get_spring(), project.get_name(),
                                   project.get_package(), has_jpa, has_mongo, generate_sample, has_redis, has_kafka,
                                   has_eureka_client,
                                   has_config_server, has_zipkin, has_rabbit)
        return param

    def extract_default_project_and_delete_zip(self, filename):
        """Extract and delete zipfile"""
        extractor = TarGzExtractor(filename)
        extractor.extract()
        extractor.delete()

    def download_default_project(self, project):
        """Download a save project file from Spring Start"""
        adapter = SpringBootWebClient()
        response = adapter.request(project)
        filename = project.get_name() + ".tar.gz"
        with open(filename, "wb") as file:
            file.write(response)
        return filename

    def make_project_class(self, metadata, selected_dependencies):
        """Create Project DTO"""
        project = Project(metadata.project_name, metadata.project_group, metadata.project_artifact
                          , metadata.project_package, metadata.project_java, metadata.project_spring,
                          selected_dependencies)
        return project

    def load_options(self):
        """Load options from resources dependencies"""
        dependencies_path = pkg_resources.resource_filename('jtech', 'resources/dependencies/dependencies.json')
        with open(dependencies_path, 'r') as file:
            options = json.load(file)
        return options
