from directories import Directories
import json
import os

class Operation:

    def clear_project_folder():
        print("Deleting all files in project...")
        try:
            for filename in os.listdir(os.path.join(Directories.PROJECT_LOCATION, "lib")):
                file_path = os.path.join(Directories.PROJECT_LOCATION, "lib", filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print("All files in the folder have been deleted.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def write_code_files(code_map):
        # Write code to files in a project directory
        
        for filename in code_map.keys():
            try:
                dart_path = os.path.join(Directories.PROJECT_LOCATION, "lib", filename)
                with open(dart_path, "w") as dart_file:
                    dart_file.write(code_map[filename])
            except KeyError as ke:
                print(f"KeyError: {ke} occurred while writing {filename}")
            except OSError as oe:
                print(f"OSError: {oe} occurred while writing {filename}")

    def save_messages(json_id, messages):
        # Save messages to a file based on the given json_id
        
        print("---No saving currently---")
        # if json_id == 0:
        #     path = Directories.PROJECT_BUILDER_JSON_PATH
        # elif json_id == 1:
        #     path = Directories.INCREMENTAL_BUILD_JSON_PATH_1
        # elif json_id == 2:
        #     path = Directories.INCREMENTAL_BUILD_JSON_PATH_2
        # else:
        #     return

        # with open(path, 'w') as f:
        #     json.dump(messages, f)

    def load_messages(json_id):
    # Load messages from a file based on the given json_id

        if json_id == 0:
            path = Directories.PROJECT_BUILDER_JSON_PATH
        elif json_id == 1:
            path = Directories.INCREMENTAL_BUILD_JSON_PATH_1
        elif json_id == 2:
            path = Directories.INCREMENTAL_BUILD_JSON_PATH_2
        else:
            path = Directories.PROJECT_MANAGER_JSON_PATH

        if os.path.exists(path):
            with open(path, 'r') as f:
                messages = json.load(f)
            return messages
        else:
            return []