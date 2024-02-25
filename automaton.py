import os
import platform
import pickle


class Task:
    def __init__(self, label, is_complete, bounty):
        self.label = label
        self.is_complete = is_complete
        self.bounty = bounty
        self.type = "task"

    def Print(self):
        if (self.is_complete):
            print("[X]", end=" ")
        else:
            print("[ ]", end=" ")
        print(f"{self.label}: {self.bounty}")


class TaskList():
    def __init__(self, name):
        self.name = name
        self.tasks = []
        self.type = "tasklist"

    def PushTask(self, label, is_complete, bounty):
        self.tasks.append(Task(label, is_complete, bounty))

    def PrintMode(self, mode):
        if not self.tasks:
            print(f"{self.name.upper()}")
            print("NO TASKS IN LIST")
            return
        if (mode == "todo"):
            print(f"{self.name.upper()} [TODO]")
            for i in self.tasks:
                if (i.is_complete is False):
                    i.Print()
        if (mode == "complete"):
            print(f"{self.name.upper()} [COMPLETE]")
            for i in self.tasks:
                if (i.is_complete is True):
                    i.Print()
        if (mode == "all"):
            print(f"{self.name.upper()} [ALL]")
            for i in self.tasks:
                i.Print()


class Reward:
    def __init__(self, label, is_claimed, price):
        self.label = label 
        self.is_claimed = is_claimed
        self.price = price
        self.type = "reward"

    def Print(self):
        if (self.is_claimed):
            print("[X]", end=" ")
        else:
            print("[ ]", end=" ")
        print(f"{self.label}: {self.price}")


class RewardList():
    def __init__(self):
        self.rewards = []
        self.type = "rewardlist"

    def PushReward(self, label, is_claimed, price):
        self.rewards.append(Reward(label, is_claimed, price))

    def Print(self, mode):
        if not self.rewards:
            print("REWARDS:")
            print("NO TASKS IN LIST")
        if (mode == 0):
            print("REWARDS [PURCHASABLE]")
            for i in self.rewards:
                if (i.is_claimed is False):
                    i.Print()
        if (mode == 1):
            print("REWARDS [PURCHASED]")
            for i in self.rewards:
                if (i.is_claimed is True):
                    i.Print()
        if (mode == 2):
            print("REWARDS [ALL]")
            for i in self.rewards:
                i.Print()


class Interface:
    def __init__(self):
        self.prefix = "[user@automaton] $ "
        self.task_lists = []
        self.reward_lists = []
        self.loaded_data = []
        self.command = None

    def Create_Task_List(self, name):
        self.task_lists.append(TaskList(name))

    def Add_Task(self, label, complete, bounty, list_name):
        if self.task_lists:
            for i in range(0, len(self.task_lists)):
                if self.task_lists[i].name == list_name:
                    self.task_lists[i].PushTask(label, complete, bounty)
                    return
            print(f"[output@automaton] $ Task list {list_name} not found.")

    def Save(self, filename):
        with open(f"{filename}.pk1", "wb") as file:
            pickle.dump(self.task_lists, file)
            pickle.dump(self.reward_lists, file)

    def Load(self, filename):
        with open(f"{filename}.pk1", "rb") as file:
            self.loaded_data = pickle.load(file)

    def Start(self):
        self.clear()
        print("Automaton v0.1a by Ammar Khan")
        print("Welcome to Autmaton! The only productivity app you will EVER need!")
        while True:
            print()
            self.command = input(self.prefix)
            if (self.command == "quit"):
                break
            self.clear()
            print(self.command)

        print("\n[output@automaton] Automaton exited.")

    def clear(self):
        platform_name = platform.system() 
        if platform_name == "Windows":
            os.system('cls')
        elif platform_name in ["Linux", "Darwin"]:
            os.system('clear')
        else:
            print("\n[output@automaton] Error: Unknown operating system")
    # def execute(self, command):
        # cmd = command.split(' ')
# ===============================================


def main():

    prog = Interface()

    prog.Create_Task_List("list1")
    prog.Add_Task("hi", False, 50, "list1")

    prog.task_lists[0].PrintMode("all")

    # prog.Start()




# ===============================================


main()
