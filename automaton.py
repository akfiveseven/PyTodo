import os
import sys
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

    def ModePrint(self, mode):
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

    def ModePrint(self, mode):
        if not self.rewards:
            print("REWARDS:")
            print("NO TASKS IN LIST")
        if (mode == "available"):
            print("REWARDS [PURCHASABLE]")
            for i in self.rewards:
                if (i.is_claimed is False):
                    i.Print()
        if (mode == "purchased"):
            print("REWARDS [PURCHASED]")
            for i in self.rewards:
                if (i.is_claimed is True):
                    i.Print()
        if (mode == "all"):
            print("REWARDS [ALL]")
            for i in self.rewards:
                i.Print()


class Interface:
    def __init__(self):
        self.prefix = "[user@automaton] $ "
        self.task_lists = []
        self.rewards = RewardList()
        self.loaded_data = []
        self.command = None
        self.balance = 0

    def Create_Task_List(self, name):
        self.task_lists.append(TaskList(name))

    def Get_Task_List_Index(self, list_name):
        if self.task_lists:
            for i in range(0, len(self.task_lists)):
                if self.task_lists[i].name == list_name:
                    return i
                else:
                    print(f"[output@automaton] $ Task list {list_name} not found.")
                    return -1

    def Add_Task(self, label, complete, bounty, list_name):
        list_index = self.Get_Task_List_Index(list_name)

        if list_index != -1:
            self.task_lists[list_index].PushTask(label, complete, bounty)

    def Remove_Task(self, target_list_name, task_pos):
        list_index = self.Get_Task_List_Index(target_list_name)

        if list_index != -1:
            self.task_lists[list_index].tasks.pop(task_pos)

    def Consume_Task(self, list_name, pos):
        list_idx = self.Get_Task_List_Index(list_name)
        if list_idx != -1:
            bounty = self.task_lists[list_idx].tasks[pos].bounty
            self.Remove_Task(list_name, pos)
            self.balance = self.balance + bounty

    def Add_Reward(self, label, price):
        self.rewards.PushReward(label, False, price)

    def Remove_Reward(self, pos):
        self.rewards.rewards.pop(pos)

    def Consume_Reward(self, pos):
        reward = self.rewards.rewards[pos]
        if self.balance >= reward.price:
            self.balance = self.balance - reward.price
            self.Remove_Reward(pos)

    def Save(self, filename):
        tlist = self.task_lists
        rewards = self.rewards
        bal = self.balance
        with open(f"{filename}.pk1", "wb") as file:
            pickle.dump(tlist, file)
            pickle.dump(rewards, file)
            pickle.dump(bal, file)

    def Load(self, filename):
        with open(f"{filename}.pk1", "rb") as file:
            tlist = pickle.load(file)
            rewards = pickle.load(file)
            bal = pickle.load(file)

            self.task_lists = tlist
            self.rewards = rewards
            self.balance = bal

    def Start(self):
        if os.path.exists("data.pk1"):
            self.Load("data")
        self.clear()
        print("Automaton v0.1a by Ammar Khan")
        print("Welcome to Autmaton! The only productivity app you will EVER need!")
        while True:
            print(f"BALANCE: {self.balance}")
            self.command = input(self.prefix)
            self.clear()
            self.Execute(self.command)
            print()

    def Execute(self, cmd):
        args = cmd.split(" ")
        if args[0] == "quit" or args[0] == "exit":
            print("[output@automaton] Automaton exited.")
            sys.exit()
        elif args[0] == "create":
            if args[1] == "list":
                if args[2]:
                    self.Create_Task_List(args[2])
            elif args[1] == "task":
                if args[2] and args[3] and args[4]:
                    self.Add_Task(args[2], False, int(args[3]), args[4])
            elif args[1] == "reward":
                if args[2] and args[3]:
                    self.Add_Reward(args[2], args[3])
        elif args[0] == "rewards":
            self.rewards.ModePrint("all")
        elif args[0] == "list":
            list_idx = self.Get_Task_List_Index(args[1])
            self.task_lists[list_idx].ModePrint("all")
        elif args[0] == "consume":
            if args[1] == "task":
                self.Consume_Task(args[3], int(args[2]))
            elif args[1] == "reward":
                self.Consume_Reward(int(args[2]))
        elif args[0] == "remove":
            if args[1] == "task":
                self.Remove_Task(args[3], int(args[2]))
            elif args[1] == "reward":
                self.Remove_Reward(int(args[2]))
        elif args[0] == "save":
            self.Save("data")
        elif args[0] == "load":
            self.Load("data")

        else:
            print(f"[output@automaton] Error: Unknown command: {cmd}")

    def clear(self):
        platform_name = platform.system()
        if platform_name == "Windows":
            os.system('cls')
        elif platform_name in ["Linux", "Darwin"]:
            os.system('clear')
        else:
            print("\n[output@automaton] Error: Unknown operating system")


# ===============================================


def main():
    prog = Interface()

    prog.Start()

# ===============================================


main()
