class Task:
    def __init__(self, title,):
        self.title = title
        self.completed = False
    def complete(self):
        self.completed = True
    def rename(self, new_title):
        new_title = new_title.strip()

        if new_title == "":
            raise ValueError("Title cannot be empty")

        self.title = new_title.strip()

first_task = Task("Learn classes")

print("Before:", first_task.title)

try:
    first_task.rename("   ")
except ValueError as error:
    print("Error:", error)

print("After:", first_task.title)
