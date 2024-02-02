import os
import json
from colorama import Fore, Style

class FileStorage:
    """
    FileStorage is responsible for handling the storage, retrieval, and management of files.
    It allows for operations such as reading, writing, listing, and deleting files, and maintains
    a manifest file to keep track of metadata associated with these files.
    
    Methods:
        __init__: Initializes the FileStorage, loads the manifest file into memory.
            Input: None
            Output: An instance of FileStorage.

        get_file_path(file_name, extension='yml'): Returns the full path of a file given its name and extension.
            Input:
                file_name (str): The name of the file.
                extension (str): The file extension (default is 'yml').
            Output:
                str: The full path to the file.

        get_file_content(file_name): Reads and returns the content of a file.
            Input:
                file_name (str): The name of the file to read.
            Output:
                str or None: The content of the file or None if the file does not exist.

        list_files(): Lists all files in the storage directory, excluding their extensions.
            Input: None
            Output:
                list[str]: A list of file names.

        store_file(file_name, file_description, file_content): Stores a file, writes its content, and updates the manifest with its metadata.
            Input:
                file_name (str): The name of the file.
                file_description (str): A description of the file.
                file_content (str): The content of the file.
            Output:
                bool: True if the file was successfully stored, False otherwise.

        delete_file(file_name): Deletes a file and removes its entry from the manifest.
            Input:
                file_name (str): The name of the file to delete.
            Output:
                bool: True if the file was successfully deleted, False otherwise.

        update_file(old_file, new_file): Updates (replaces) an existing file with a new file (To be implemented).
            Input:
                old_file (str): The name of the existing file.
                new_file (str): The name of the new file to replace the old file.
            Output:
                bool: True if the file was successfully updated, False otherwise. (To be implemented)
    
    Attributes:
        storage_dir (str): The directory where files are stored.
        MANIFEST_FILE (str): The name of the manifest file that stores metadata about the files.
        manifest (dict): A dictionary holding the loaded content of the manifest file.
    """

    MANIFEST_FILE = '.manifest.json'

    def __init__(self,storage_dir):
        self.storage_dir = storage_dir

        if not os.path.exists(self.storage_dir):
            os.mkdir(self.storage_dir)

        # Load the manifest file into memory
        if os.path.exists(self.MANIFEST_FILE):
            with open(self.MANIFEST_FILE, 'r') as file:
                self.manifest = json.load(file)
        else:
            self.manifest = {}

    def get_file_path(self, file_name, extension='yml'):
        return os.path.join(self.storage_dir, f"{file_name}.{extension}")

    def get_file_content(self, file_name):
        file_path = self.get_file_path(file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read()
        else:
            # print(f"{Fore.RED}File {file_name} does not exist.{Style.RESET_ALL}")
            return None

    def list_files(self):
        files = os.listdir(self.storage_dir)
        files_without_extension = [os.path.splitext(file)[0] for file in files]
        return files_without_extension
    
    def store_file(self, file_name, file_description, file_content):
        file_path = self.get_file_path(file_name)
        
        with open(file_path, 'w') as file:
            file.write(file_content)
        # print(f"{Fore.GREEN}Stored file: {file_path}{Style.RESET_ALL}")

        # Update the manifest
        self.manifest[file_name] = {
            'name': file_name,
            'description': file_description,
            'path': file_path
        }
        with open(self.MANIFEST_FILE, 'w') as file:
            json.dump(self.manifest, file)

        return True

    def delete_file(self, file_name):
        file_path = self.get_file_path(file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            # print(f"{Fore.GREEN}Deleted file: {file_path}{Style.RESET_ALL}")
            
            # Update the manifest
            del self.manifest[file_name]
            with open(self.MANIFEST_FILE, 'w') as file:
                json.dump(self.manifest, file)
            
            return True
        else:
            # print(f"{Fore.RED}File not found: {file_path}{Style.RESET_ALL}")
            return False

    # TODO: implement update 
    def update_file(self, old_file, new_file):
        old_file_path = self.get_file_path(old_file)
        if os.path.exists(old_file_path):
            new_file_path = self.get_file_path(new_file)
            # Mocked code to update a file
            # print(f"{Fore.GREEN}Updating file: {old_file_path} with {new_file_path}{Style.RESET_ALL}")
            return True
        else:
            # print(f"{Fore.RED}File not found: {old_file_path}{Style.RESET_ALL}")
            return False