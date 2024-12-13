import argparse
import os


#default name for the todo file 
DEFAULT_TODO_FILE = "TODO.txt"


#class for a todo item
class TodoItem:
    def __init__(self, task_id, topic, description, status):
        self.task_id = task_id
        self.topic = topic
        self.description = description
        self.status = status

    def change_status(self, new_status):
        valid_statuses = ["incomplete", "in progress", "complete"]
        if new_status not in valid_statuses:
            print(f"Error: Invalid status '{new_status}'. Valid statuses are {', '.join(valid_statuses)}.")
        else:
            self.status = new_status
            print(f"Status of task ID {self.task_id} changed to '{new_status}'.")

    def update_task(self, new_topic, new_description):
        self.topic = new_topic
        self.description = new_description
        print(f"Task ID {self.task_id} updated: Topic: '{new_topic}', Description: '{new_description}'.")


#class for a collection of to do items aka todo list
class TodoList:
    def __init__(self, filename=DEFAULT_TODO_FILE):
        # Check if the filename is None or empty and default to TODO.txt if so
        if not filename:
            filename = DEFAULT_TODO_FILE
        self.filename = filename
        self.todos = self.load_todos()

    def load_todos(self):
        todos = []
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                for line in file.readlines()[2:]:  
                    parts = line.strip().split(" | ")
                    if len(parts) == 3:
                        task_id, topic_and_description, status = parts
                        topic, description = topic_and_description.split(" - ", 1)
                        todos.append(TodoItem(int(task_id), topic, description, status))
        else:
            print(f"The file '{self.filename}' doesn't exist. Starting with an empty TODO list.")
        return todos

    def save_todos(self):
        with open(self.filename, "w") as file:
            # Write the header and separator
            file.write(f"{'ID':<5} | {'Topic & Description':<40} | {'Status':<12}\n")
            file.write("-" * 60 + "\n")
            for task in self.todos:
                topic_and_description = f"{task.topic} - {task.description}"
                file.write(f"{task.task_id:<5} | {topic_and_description:<40} | {task.status:<12}\n")
        print(f"TODO list saved to '{self.filename}'.")

    def add_task(self, topic, description, status):
        # Method to add a new task to the TODO list

        new_id = max([task.task_id for task in self.todos], default=0) + 1
        new_task = TodoItem(new_id, topic, description, status)
        self.todos.append(new_task)
        self.save_todos()
        print(f"Task added: ID {new_task.task_id}, Topic: '{topic}', Status: '{status}'.")
    # Method to list all tasks in the TODO list
    def list_tasks(self):
        if self.todos:
            print("Your current TODO list:")
            print(f"{'ID':<5} {'Topic & Description':<40} {'Status':<12}")
            print("-" * 60)
            for task in self.todos:
                topic_and_description = f"{task.topic} - {task.description}"
                print(f"{task.task_id:<5} {topic_and_description:<40} {task.status:<12}")
        else:
            print("Your TODO list is empty.")

    def find_task_by_id(self, task_id):
        for task in self.todos:
            if task.task_id == task_id:
                return task
        return None

    def update_task(self, task_id, new_topic, new_description):
        task = self.find_task_by_id(task_id)
        if task:
            task.update_task(new_topic, new_description)
            self.save_todos()
        else:
            print(f"Error: Task with ID {task_id} not found.")

    def change_task_status(self, task_id, new_status):
        task = self.find_task_by_id(task_id)
        if task:
            task.change_status(new_status)
            self.save_todos()
        else:
            print(f"Error: Task with ID {task_id} not found.")

def handle_commands(args):
    # Use the list_name argument if provided, or default to the file name
    list_name = getattr(args, 'list_name', DEFAULT_TODO_FILE)
    if list_name == "":
        list_name = DEFAULT_TODO_FILE  # if list is empty, use the default file

    
    todo_list = TodoList(list_name)

    #handle commands user input
    if args.command == "add":
        todo_list.add_task(args.topic, args.description, args.status)
    elif args.command == "list":
        todo_list.list_tasks()
    elif args.command == "change_status":
        todo_list.change_task_status(args.task_id, args.status)
    elif args.command == "update":
        todo_list.update_task(args.task_id, args.new_topic, args.new_description)
    else:
        print("Error: Unknown command. Use 'add', 'list', 'change_status', or 'update'.")

def file_parser():
    parser = argparse.ArgumentParser(description="Manage your TODO list.")
    subparsers = parser.add_subparsers(dest="command")

    # lists the task parser
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("--list-name", type=str, help="Name of the TODO list file")


    # to add task parsers
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("topic", type=str, help="The topic of the task")
    add_parser.add_argument("description", type=str, help="The task description")
    add_parser.add_argument("status", type=str, choices=["incomplete", "in progress", "complete"], help="The status of the task")
    add_parser.add_argument("--list-name", type=str, help="Name of the TODO list file")

    # to change status paser
    status_parser = subparsers.add_parser("change_status", help="Change the status of a task")
    status_parser.add_argument("task_id", type=int, help="The ID of the task to update")
    status_parser.add_argument("status", type=str, choices=["incomplete", "in progress", "complete"], help="The new status for the task")
    status_parser.add_argument("--list-name", type=str, help="Name of the TODO list file")

    # to update task parser
    update_parser = subparsers.add_parser("update", help="Update a task's details")
    update_parser.add_argument("task_id", type=int, help="The ID of the task to update")
    update_parser.add_argument("new_topic", type=str, help="The new topic for the task")
    update_parser.add_argument("new_description", type=str, help="The new description for the task")
    update_parser.add_argument("--list-name", type=str, help="Name of the TODO list file")

    return parser 




def main():
    parser = file_parser()
    args = parser.parse_args()

    if not args.command:
        print("Error: No command provided. Use 'add', 'list', 'change_status', or 'update'.")
    else:
        handle_commands(args)
#runs the program
if __name__ == "__main__":
    main()
