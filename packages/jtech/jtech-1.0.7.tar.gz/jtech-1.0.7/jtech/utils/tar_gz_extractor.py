import tarfile
import os


class TarGzExtractor:
    """
    Class for extract and delete zip file.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def extract(self):
        """
        Extract downloaded file from Spring Starter.
        """
        target = os.getcwd()
        with tarfile.open(self.file_path, "r:gz") as tar:
            tar.extractall(target)

    def delete(self):
        """
        Delete tar.gz file extracted.
        """
        os.remove(self.file_path)
