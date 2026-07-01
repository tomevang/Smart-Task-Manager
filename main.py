from task_manager import TaskManager
from ai_client import get_ai_suggestion


def main():
    tm = TaskManager()
    suggested_tasks = None
    while True:
        command = input("> ").strip()
        # parse and handle the command here
        print(command)
        command = command.split(" ", 1)
        # quit
        if command[0].lower() == "quit" or command[0].lower() == "q":
            break
        # undo
        elif command[0].lower() == "undo":
            success, task_id = tm.undo()
            if success:
                print(f"Task {task_id} successfully restored!")
            else:
                print("Nothing to undo!")
        # process
        elif command[0].lower() == "process":
            status, task_id = tm.process_next()
            if status == "success":
                print(f"Task {task_id} successfully processed!")
            elif status == "busy":
                print(f"Task {task_id} is already in progress. Complete it first with 'complete {task_id}'.")
            elif status == "empty":
                print("Backlog is empty — nothing to process!")
        # show
        elif command[0].lower() == "show":
            tm.show()
        # follow
        elif command[0].lower() == "follow":
            if suggested_tasks is not None:
                print("Reordering the task list according to the AI suggested order.")
                tm.follow(suggested_tasks)
                suggested_tasks = None
            else:
                print('Error: Please run "ai suggest" to create a new task list order before running "follow"')
        # ai suggest
        elif command[0].lower() == "ai" and len(command) > 1 and command[1].lower() == "suggest":
            suggested_tasks = get_ai_suggestion(tm.tasks)
            print(f"AI suggests this order: {suggested_tasks}")
        # add 
        elif command[0].lower() == "add":
            if len(command) < 2 or command[1].strip() == "":
                print(f"Error: Please provide a task description.")
                print(f"  Usage: add TASK_DESCRIPTION")
                print(f"  Example command for add: add create classes for employees and managers")
            else:
                success, task_id = tm.add_task(command[1])
                if success:
                    print(f"Task {task_id} was created successfully.")
                else:
                    print("Error: Task description cannot be empty.")
        # complete
        elif command[0].lower() == "complete":
            if len(command) < 2:
                print("Error: task id must be provided")
                continue
            if not command[1].isdigit():
                print("Error: task id must be a number")
                continue
            task_id = int(command[1])
            status, returned_id = tm.complete_task(task_id)
            if status:
                print(f"Task {returned_id} marked as complete!")
            else:
                print(f"Error: Task {task_id} was not found.")


if __name__ == "__main__":
    main()