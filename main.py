from task_manager import create_task, list_tasks ,complete_task ,delete_task ,get_task

first_task = create_task("Onboarding")
second_task = create_task("Build an API")

found_task = get_task(2)
print("Found task:", found_task)

completed_task = complete_task(2)
print("Completed task:", completed_task)

deleted_task = delete_task(1)
print("Deleted task:", deleted_task)

print("All tasks:", list_tasks())