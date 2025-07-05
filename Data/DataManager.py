import json
import logging

class DataManager:
    def __init__(self, file_path:str = './Data/data.json'):
        self.logger = logging.getLogger('DataManager')
        self.logger.addHandler(logging.FileHandler('./Log/DataManager.log'))
        self.logger.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger.level = logging.INFO
        self.logger.info("DataManager: logger initialized")

        self.file_path = file_path
        self.data = {}
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.output_file = open(self.file_path, 'w', encoding='utf-8')
        # with open(self.file_path, 'r', encoding='utf-8') as f:
        #     self.data = json.load(f)
        self.logger.info("DataManager loaded")

    def __del__(self):
        self.write_data()
        #self.input_file.close()
        self.output_file.close()
        self.logger.info("DataManager deleted\n")

    def save_data(self, name:str, data):
        self.data[name] = data
        self.logger.info(f"Data '{name}' saved")

    def load_data(self, name:str):
        if name not in self.data:
            self.logger.error(f"Data '{name}' not found, fail to load")
            raise Exception(f"Data '{name}' not found")
        return self.data[name]

    def delete_data(self, name:str):
        if name not in self.data:
            self.logger.warning(f"Data '{name}' not found, fail to delete")
            return
        self.data.pop(name)
        self.logger.info(f"Data '{name}' deleted")

    def write_data(self):
        json.dump(self.data, self.output_file, ensure_ascii=False, indent=4)
        # with open(self.file_path, 'w', encoding='utf-8') as f:
        #     json.dump(self.data, f, ensure_ascii=False, indent=4)
        self.logger.info(f"Data written to file {self.file_path}")


