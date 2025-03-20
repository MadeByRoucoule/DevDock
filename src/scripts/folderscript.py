import os

class FolderScript:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def get_files(self):
        return os.listdir(self.folder_path)
    
    def get_folders(self):
        return [f for f in os.listdir(self.folder_path) if os.path.isdir(os.path.join(self.folder_path, f))]
    
    def create_folder(self, folder_name):
        folder_path = os.path.join(self.folder_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path
    
    def delete_folder(self, folder_name):
        folder_path = os.path.join(self.folder_path, folder_name)
        os.removedirs(folder_path)
        return folder_path
    
    def create_file(self, file_name, content=""):
        file_path = os.path.join(self.folder_path, file_name)
        with open(file_path, "w") as f:
            f.write(content)
        return file_path
    
    def delete_file(self, file_name):
        file_path = os.path.join(self.folder_path, file_name)
        os.remove(file_path)
        return file_path

    def rename_folder(self, old_name, new_name):
        old_path = os.path.join(self.folder_path, old_name)
        new_path = os.path.join(self.folder_path, new_name)
        os.rename(old_path, new_path)
        return new_path

    def rename_file(self, old_name, new_name):
        old_path = os.path.join(self.folder_path, old_name)
        new_path = os.path.join(self.folder_path, new_name)
        os.rename(old_path, new_path)
        return new_path
