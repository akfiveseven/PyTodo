import datetime

class Task:
    def __init__(self, name, category, due_date, start_time, end_time, complete_time):
        self.name = name
        self.category = category
        self.due_date = due_date
        self.start_time = start_time
        self.end_time = end_time
        self.complete_time = complete_time
        self.complete_flag = False
        self.tags = []


class User:
    def __init__(self, username):
        self.balance = 0
        self.username = username


class Reward:
    def __init__(self, name, category, cost):
        self.name = name
        self.category = category
        self.cost = cost
        self.consumed_flag = False

class Program:

    def __init__(self):
        self.current_user = None
        self.user_command = ""

    def set_user(self, user):
        self.current_user = user

    def printmenu(self):
        print(f"Welcome to Cognition Pattern, a task/habit/routine scheduler that rewards you for getting stuff done!\n\n1) Log-in\n2) Create user\n\n")

    def command_input(self):
        self.user_command = input("[user@pattern] ~ ")

    def print_command(self):
        print(self.user_command)

prog = Program()
# prog.printmenu()
prog.command_input()
prog.print_command()
