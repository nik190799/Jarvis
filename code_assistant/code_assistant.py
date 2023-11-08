import os
import json
import time
import subprocess
import openai
from directories import Directories
from file_operations import Operation

class CodeAssistant:
    def __init__(self):
        # Initialization code here

        self.code_map = {}
        self.task_list = []
        self.current_feature_index = -1
        self.application_template = ""
        
        YOUR_OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        openai.api_key = YOUR_OPENAI_API_KEY

    def generate_code_map(self, code_string):
        # Generate a map of filenames and code from a code string
        
        file_code_map = {}
        parts = code_string.split('***')

        for i in range(0, len(parts), 2):
            try:
                filename = parts[i].strip()
                code = parts[i + 1].strip()
                file_code_map[filename] = code
            except IndexError as ie:
                # getting response again from API
                print("Wrong format code from API - requesting again!")
                Operation.clear_project_folder()
                self.get_response(0, self.application_template)
                print(f"IndexError: {ie} occurred while processing code string")

        return file_code_map

    def get_code_string(self, code_map, assistant_mid_response):
        # Combine filenames and code into a single string
        
        result = ""
        for filename in assistant_mid_response:
            try:
                result = result + filename + '***' + code_map[filename] + '***'
            except KeyError as ke:
                print(f"KeyError: {ke} occurred while processing {filename}")
                print("Wrong format code from API - requesting again!")
                Operation.clear_project_folder()
                self.get_response(0, self.application_template)

        return result

    def get_response(self, json_id, user_input):
        # Get a response from the OpenAI API and manage messages
        
        messages = Operation.load_messages(json_id)
        max_attempts = 2
        for attempt in range(max_attempts):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages + [
                        {"role": "user", "content": user_input}
                    ]
                )
                break
            except Exception as e:
                print(f"API error: {str(e)}")
                if attempt < max_attempts - 1:
                    print(f"Retrying... Attempt {attempt + 2}")
                    time.sleep(2)
                else:
                    print("Max attempts reached. Unable to get API response.")
                    return None
        assistant_response = response.choices[0].message.content
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "assistant", "content": assistant_response})
        Operation.save_messages(json_id, messages)
        if json_id == 0 or json_id == 1:
            return self.generate_code_map(assistant_response)
        else:
            return assistant_response
        

    def map_main_code_map(self, code_map_1):
        # Map code from an incremental development step to the main code map
        
        for key in code_map_1.keys():
            self.code_map[key] = code_map_1[key]

    def incremental_development(self, user_input):
        # Perform incremental development using the code assistant
        
        modified_input = "request: " + user_input + f" filenames: {list(self.code_map.keys())}"
        assistant_mid_response = self.get_response(2, modified_input).split('***')
        print("    Midstep completed...")
        final_input = "request: " + user_input + " codeString: " + self.get_code_string(self.code_map, assistant_mid_response)
        code_map_1 = self.get_response(1, final_input)
        self.map_main_code_map(code_map_1)
        print("    Writing the files...")
        Operation.write_code_files(code_map_1)
        print("    Application updated...")
        self.current_feature_index += 1
        self.run_flutter_app()


    def task_distribution(self):
        # Distribute tasks and perform incremental development for each task
        
        index = 0
        while index < len(self.task_list):
            task = self.task_list[index].split('.')[0]
            print("Feature: " + task)
            self.incremental_development(task)
            index += 1
        print("----------------------------------------Updates Finished--------------------------------------------")
        obj.generate_tasks()

    def generate_project_template(self):
        # Generate the project template

        Operation.clear_project_folder()
        self.application_template = input("Application Template: ")
        self.code_map = self.get_response(0, self.application_template)
        Operation.write_code_files(self.code_map)

    def generate_tasks(self):
        # Generate tasks based on the entire code
        
        entire_code = self.get_entire_code_as_string()
        self.task_list = self.get_response(3, entire_code).split('***')
        self.task_distribution()

    def get_entire_code_as_string(self):
        # Get the entire code as a string
        
        return '***'.join([f"{key}***{value}" for key, value in self.code_map.items()])


    def run_flutter_app(self):
        # Run the Flutter app
        
        try:
            os.chdir(Directories.PROJECT_LOCATION)
            flutter_executable = "C:\\src\\flutter\\bin\\flutter.bat"
            cmd = [flutter_executable, "run", "-d", "chrome"]
            print("Application is running...")
            completed_process = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                check=True
            )
            print("Flutter app built successfully")
        except Exception as e:
            print("An error occurred: " + str(e))
            self.run_flutter_clean_and_pub_get(e)


    def run_flutter_clean_and_pub_get(self, error):
        # Run 'flutter clean' and 'flutter pub get' commands
        
        try:
            subprocess.run(['C:\\src\\flutter\\bin\\flutter.bat', 'clean'], check=True)
            subprocess.run(['C:\\src\\flutter\\bin\\flutter.bat', 'pub', 'get'], check=True)
            print("Flutter clean and pub get commands executed successfully")
            self.raise_bug("Resolve this bug: " + str(error))

        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing a Flutter command: {e}")

        except FileNotFoundError:
            print("Flutter executable not found. Please check the path.")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")

    def raise_bug(self, error_message):
        # Raise a bug
        print("----------------------------------------Raising Bug--------------------------------------------")
        self.task_list.insert(self.current_feature_index, error_message)
        return
    

if __name__ == "__main__":
    obj = CodeAssistant()
    obj.generate_project_template()
    obj.generate_tasks()
