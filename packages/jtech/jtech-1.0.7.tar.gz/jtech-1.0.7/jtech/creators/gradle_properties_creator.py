class GradlePropertiesCreator:
    def __init__(self, file_path):
        self.file_path = file_path

    def create_gradle_properties(self):
        content = "APP_VERSION=1.0.0-SNAPSHOT\n"

        with open(self.file_path, "w") as file:
            file.write(content)