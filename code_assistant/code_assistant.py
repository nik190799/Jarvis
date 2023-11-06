import os
import json
import time
import subprocess
import openai

class CodeAssistant:
    def __init__(self):
        # Initialization code here

        self.code_map = {}
        self.task_list = []
        self.current_feature_index = -1
        
        self.project_location = "location-for-deploying-application"
        self.current_directory = "jarvis-project-file-location"
        self.project_builder_json_path = 'ModelDatasets/flutterProjects.json'
        self.incremental_build_json_path_1 = '/incrementalCodePrompts.json'
        self.incremental_build_json_path_2 = '/ModelDatasets/incrementalCodePrompts2.json'
        self.product_manager_json_path = '/ModelDatasets/featureFinder.json'
        
        YOUR_OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        openai.api_key = YOUR_OPENAI_API_KEY


    def load_messages(self, json_id):
        # Load messages from a file based on the given json_id

        if json_id == 0:
            path = self.project_builder_json_path
        elif json_id == 1:
            path = self.incremental_build_json_path_1
        elif json_id == 2:
            path = self.incremental_build_json_path_2
        else:
            path = self.product_manager_json_path

        if os.path.exists(path):
            with open(path, 'r') as f:
                messages = json.load(f)
            return messages
        else:
            return []

    def save_messages(self, json_id, messages):
        # Save messages to a file based on the given json_id
        
        if json_id == 0:
            path = self.project_builder_json_path
        elif json_id == 1:
            path = self.incremental_build_json_path_1
        elif json_id == 2:
            path = self.incremental_build_json_path_2
        else:
            return

        with open(path, 'w') as f:
            json.dump(messages, f)
    

    def write_code_files(self, code_map):
        # Write code to files in a project directory
        
        for filename in code_map.keys():
            try:
                dart_path = os.path.join(self.project_location, "lib", filename)
                with open(dart_path, "w") as dart_file:
                    dart_file.write(code_map[filename])
            except KeyError as ke:
                print(f"KeyError: {ke} occurred while writing {filename}")
            except OSError as oe:
                print(f"OSError: {oe} occurred while writing {filename}")

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

        return result

    def get_response(self, json_id, user_input):
        # Get a response from the OpenAI API and manage messages
        
        messages = self.load_messages(json_id)
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
        self.save_messages(json_id, messages)
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
        self.write_code_files(code_map_1)
        print("    Application updated...")
        self.current_feature_index += 1
        self.run_flutter_app()


    def task_distribution(self):
        # Distribute tasks and perform incremental development for each task
        
        index = 0
        while index < len(self.task_list):
            task = self.task_list[index]
            print("Feature: " + task)
            self.incremental_development(task)
            index += 1
        print("----------------------------------------Updates Finished--------------------------------------------")
        obj.generate_tasks()

    def generate_project_template(self):
        # Generate the project template
        
        user_input = input("Application Template: ")
        self.code_map = self.get_response(0, user_input)
        self.write_code_files(self.code_map)

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
            os.chdir(self.project_location)
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

            if completed_process.returncode != 0:
                print("Flutter app build failed. Error messages:")
                print(completed_process.stderr)
                self.raise_bug("Resolve this bug: " + str(completed_process.stderr))
            else:
                print("Flutter app built successfully")
        except Exception as e:
            print("An error occurred:")
            print(e)
            self.run_flutter_clean_and_pub_get()
            self.run_flutter_app()


    def run_flutter_clean_and_pub_get(self):
        # Run 'flutter clean' and 'flutter pub get' commands
        
        try:
            subprocess.run(['C:\\src\\flutter\\bin\\flutter.bat', 'clean'], check=True)
            subprocess.run(['C:\\src\\flutter\\bin\\flutter.bat', 'pub', 'get'], check=True)
            print("Flutter clean and pub get commands executed successfully")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing a Flutter command: {e}")
        except FileNotFoundError:
            print("Flutter executable not found. Please check the path.")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")

    def raise_bug(self, error_message):
        # Raise a bug
        
        print("Raising a bug")
        self.task_list.insert(self.current_feature_index, error_message)
        return

if __name__ == "__main__":
    obj = CodeAssistant()
    obj.generate_project_template()
    obj.generate_tasks()
