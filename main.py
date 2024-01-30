import json
import os
from datetime import datetime, timedelta

class ToDoList:
    def __init__(self):
        self.tasks = []

    def display_tasks(self):
        print("\n===== TO-DO LIST =====")
        if not self.tasks:
            print("No tasks found. Start by adding some tasks!")
        else:
            for idx, task in enumerate(self.tasks, start=1):
                print(f"{idx}. {task['title']} - {task['description']} - Due: {task['due_date']} - Status: {'Completed' if task['completed'] else 'Pending'}")

    def add_task(self, title, description, due_date=None):
        new_task = {
            "title": title,
            "description": description,
            "due_date": due_date,
            "completed": False
        }
        self.tasks.append(new_task)
        print("Task added successfully!")

    def mark_completed(self, task_index):
        if 1 <= task_index <= len(self.tasks):
            self.tasks[task_index - 1]["completed"] = True
            print("Task marked as completed!")
        else:
            print("Invalid task index.")

    def remove_task(self, task_index):
        if 1 <= task_index <= len(self.tasks):
            removed_task = self.tasks.pop(task_index - 1)
            print(f"Task '{removed_task['title']}' removed successfully!")
        else:
            print("Invalid task index.")

    def save_to_file(self):
        with open("todo_list.json", "w") as file:
            json.dump(self.tasks, file, default=self.datetime_serializer)

    def load_from_file(self):
        if os.path.exists("todo_list.json"):
            with open("todo_list.json", "r") as file:
                self.tasks = json.load(file, object_hook=self.datetime_deserializer)

    def datetime_serializer(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError("Type not serializable")

    def datetime_deserializer(self, d):
        if 'type' in d and d['type'] == 'datetime':
            return datetime.fromisoformat(d['value'])
        return d
    
    def edit_task(self, task_index):
        if 1 <= task_index <= len(self.tasks):
            task_to_edit = self.tasks[task_index - 1]
            print(f"Editing Task: {task_to_edit['title']}")
            
            new_title = input("Enter new task title (press Enter to keep the same): ")
            task_to_edit['title'] = new_title if new_title else task_to_edit['title']

            new_description = input("Enter new task description (press Enter to keep the same): ")
            task_to_edit['description'] = new_description if new_description else task_to_edit['description']

            new_due_date_str = input("Enter new due date (YYYY-MM-DD) [press Enter to keep the same]: ")
            if new_due_date_str:
                task_to_edit['due_date'] = datetime.strptime(new_due_date_str, "%Y-%m-%d")
            
            print("Task edited successfully!")
        else:
            print("Invalid task index.")

def main():
    todo_list = ToDoList()
    todo_list.load_from_file()

    while True:
        print("\n===== TO-DO LIST APPLICATION =====")
        print("1. View To-Do List")
        print("2. Add Task")
        print("3. Edit Task")
        print("4. Mark Task as Completed")
        print("5. Remove Task")
        print("6. Save and Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            todo_list.display_tasks()
        elif choice == "2":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            due_date_str = input("Enter due date (YYYY-MM-DD) [Press Enter if not applicable]: ")
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d") if due_date_str else None
            todo_list.add_task(title, description, due_date)
        elif choice == "3":
            todo_list.display_tasks()
            task_index = int(input("Enter the index of the task to edit: "))
            todo_list.edit_task(task_index)
        elif choice == "4":
            todo_list.display_tasks()
            task_index = int(input("Enter the index of the task to mark as completed: "))
            todo_list.mark_completed(task_index)
        elif choice == "5":
            todo_list.display_tasks()
            task_index = int(input("Enter the index of the task to remove: "))
            todo_list.remove_task(task_index)
        elif choice == "6":
            todo_list.save_to_file()
            print("Changes saved. Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()