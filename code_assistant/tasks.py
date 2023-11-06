class TaskManager:
    def __init__(self):
        # Task management code here

        self.task_list = []
        self.current_feature_index = 0
        self.code_map = {}

    def generate_tasks(self):
        # Generate tasks based on the entire code
        
        entire_code = self.get_entire_code_as_string()
        self.task_list = self.get_response(3, entire_code).split('***')
        self.task_distribution()

    def get_entire_code_as_string(self):
        return '***'.join([f"{key}***{value}" for key, value in self.code_map.items()])


if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.generate_tasks()
