from abc import ABC, abstractmethod
from opstimus.utils.file_storage import FileStorage

class BaseConfigManager(ABC):
    
    def __init__(self, file_storage: FileStorage):
        self.file_storage = file_storage

    @abstractmethod
    def create_config(self, fuzzy_query):
        pass

    # @abstractmethod
    # def get_config(self, query):
    #     pass

    @abstractmethod
    def get_config(self, config_name):
        pass

    @abstractmethod
    def save_config(self, config_name, config_description, config_data):
        pass

    @abstractmethod
    def validate_config(self, config_data):
        pass

    def list_configs(self):
        return self.file_storage.list_files()