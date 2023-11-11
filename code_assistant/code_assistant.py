from directories import Directories
from file_operations import Operation
from flutter_operations import Flutter
from openai_operations import OpenAI

class CodeAssistant:
    def __init__(self):
        self.code_map = {}
        self.task_list = []
        self.current_feature_index = -1
        self.application_template = ""
        self.errorOccured = False

    def get_code_string(self, code_map, assistant_mid_response):
        result = ""
        for filename in assistant_mid_response:
            try:
                result = result + filename + '***' + code_map[filename] + '***'
            except KeyError as ke:
                print(f"<Error: KeyError: {ke} occurred while processing {filename}>")
                print("<Request: Wrong format code from API. Start the project again!>")
                Operation.clear_project_folder()
                OpenAI.get_response(0, self.application_template)
        return result

    def map_main_code_map(self, code_map_1):
        for key in code_map_1.keys():
            self.code_map[key] = code_map_1[key]

    def incremental_development(self, user_input):
        modified_input = "request: " + user_input + f" filenames: {list(self.code_map.keys())}"
        assistant_mid_response = OpenAI.get_response(2, modified_input).split('***')
        final_input = "request: " + user_input + " codeString: " + self.get_code_string(self.code_map, assistant_mid_response)
        code_map_1 = OpenAI.get_response(1, final_input)
        self.map_main_code_map(code_map_1)
        Operation.write_code_files(code_map_1)
        self.current_feature_index += 1
        Flutter.run_flutter_app()


    def task_distribution(self):
        index = 0
        while(index < len(self.task_list) and not self.errorOccured):
            task = self.task_list[index].split('.')[0]
            print("<Feature: " + task + ">")
            self.incremental_development(task)
            index += 1
        print("<Update: Updates Finished, Generating new tasks!>")
        obj.generate_tasks()

    def generate_project_template(self):
        Operation.clear_project_folder()
        self.application_template = input("<Input: Application Template: ")
        self.code_map = OpenAI.get_response(0, self.application_template)
        Operation.write_code_files(self.code_map)

    def generate_tasks(self):
        entire_code = self.get_entire_code_as_string()
        self.task_list = OpenAI.get_response(3, entire_code).split('***')
        self.task_distribution()

    def get_entire_code_as_string(self):
        return '***'.join([f"{key}***{value}" for key, value in self.code_map.items()])

    def raise_bug(self, error_message):
        print("<Update: Raising Bug!!!>")
        self.task_list.insert(self.current_feature_index, error_message)
        return
    
if __name__ == "__main__":
    obj = CodeAssistant()
    obj.generate_project_template()
    obj.generate_tasks()
