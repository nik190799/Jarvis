from file_operations import Operation

class Task:
    def generate_code_map(code_string):
        file_code_map = {}
        parts = code_string.split('***')
        for i in range(0, len(parts), 2):
            try:
                filename = parts[i].strip()
                code = parts[i + 1].strip()
                file_code_map[filename] = code
            except IndexError as ie:
                # getting response again from API
                print("<Error: Wrong format code from API - requesting again!>")
                # Operation.clear_project_folder()
                # OpenAI.get_response(0, application_template)
                print(f"<Error: IndexError: {ie} occurred while processing code string>")
        return file_code_map