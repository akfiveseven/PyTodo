import datetime
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

    def PopTask(self, idx):
        self.tasks.pop(idx)

    def CompleteTask(self, idx):
        self.tasks[idx].is_complete = True

    def ModePrint(self, mode):
        if not self.tasks:
            print(f"{self.name.upper()}")
            print("NO TASKS IN LIST")
            return
        if (mode == "todo"):
            print(f"{self.name.upper()} [todo]")
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
            for i in range(0, len(self.tasks)):
                j = i + 1
                print(f"({j})", end=" ")
                self.tasks[i].Print()


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

    def PopReward(self, idx):
        self.rewards.pop(idx)

    def ClaimReward(self, idx):
        self.rewards[idx].is_claimed = True

    def ModePrint(self, mode):
        if not self.rewards:
            print("REWARDS:")
            print("NO REWARDS")
            return
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
            for i in range(0, len(self.rewards)):
                j = i + 1
                print(f"({j})", end=" ")
                self.rewards[i].Print()


class Interface:
    def __init__(self):
        self.user_prefix = "[user@automaton] $ "
        self.output_prefix = "[output@automaton] "
        self.error_prefix = "[error@automaton] "
        self.tasklist = TaskList("todo")
        self.dailylist = TaskList("daily")
        self.rewardlist = RewardList()
        self.loaded_data = []
        self.command = None
        self.balance = 0
        self.saved_date = None
        self.current_date = datetime.date.today()

    def Add_Task(self, label, bounty):
        self.tasklist.PushTask(label, False, bounty)

    def Remove_Task(self, idx):
        self.tasklist.PopTask(idx)

    def Consume_Task(self, idx):
        if self.tasklist.tasks[idx].is_complete is False:
            bounty = self.tasklist.tasks[idx].bounty
            self.tasklist.CompleteTask(idx)
            self.balance = self.balance + bounty

    def Add_Reward(self, label, price):
        self.rewardlist.PushReward(label, False, price)

    def Remove_Reward(self, idx):
        self.rewardlist.PopReward(idx)

    def Consume_Reward(self, idx):
        reward = self.rewardlist.rewards[idx]
        if reward.is_claimed is False:
            if self.balance >= reward.price:
                self.balance = self.balance - reward.price
                # self.Remove_Reward(idx)
                self.rewardlist.ClaimReward(idx)

    def Save(self, filename):
        tlist = self.tasklist
        daily = self.dailylist
        rewards = self.rewardlist
        bal = self.balance
        d = self.saved_date
        with open(f"{filename}.pk1", "wb") as file:
            pickle.dump(tlist, file)
            pickle.dump(daily, file)
            pickle.dump(rewards, file)
            pickle.dump(bal, file)
            pickle.dump(d, file)

    def Load(self, filename):
        with open(f"{filename}.pk1", "rb") as file:
            tlist = pickle.load(file)
            daily = pickle.load(file)
            rewards = pickle.load(file)
            bal = pickle.load(file)
            d8 = pickle.load(file)

            self.tasklist = tlist
            self.dailylist = daily
            self.rewardlist = rewards
            self.balance = bal
            self.saved_date = d8

    def Start(self):
        if os.path.exists("data.pk1"):
            self.Load("data")
        self.clear()
        print("Automaton v0.1a by Ammar Khan")
        print("Welcome to Autmaton! The only productivity app you will EVER need!")
        while True:
            print(self.saved_date)
            print(f"BALANCE: {self.balance}")
            self.command = input(self.user_prefix)
            self.clear()
            self.Execute(self.command)
            print()

    def Execute(self, cmd):
        args = cmd.split(" ")
        if args[0] == "quit" or args[0] == "exit":
            print("[output@automaton] Automaton exited.")
            sys.exit()
        elif args[0] == "save":
            self.Save("data")
        elif args[0] == "load":
            self.Load("data")
        elif args[0] == "list":
            if len(args) == 1:
                self.dailylist.ModePrint("all")
                self.tasklist.ModePrint("all")
                return
            if args[1] == "add":
                if len(args) == 4:
                    self.Add_Task(args[2], int(args[3]))
                else:
                    print("Syntax error: args")
            if args[1] == "remove":
                if len(args) == 3:
                    task_to_remove_idx = int(args[2])-1
                    self.tasklist.PopTask(task_to_remove_idx)
            if args[1] == "consume":
                if len(args) == 3:
                    task_to_consume_idx = int(args[2])-1
                    self.Consume_Task(task_to_consume_idx)
            self.tasklist.ModePrint("all")
        elif args[0] == "rewards":
            if len(args) == 1:
                self.rewardlist.ModePrint("all")
                return
            if args[1] == "add":
                if len(args) == 4:
                    self.Add_Reward(args[2], int(args[3]))
                else:
                    print("Syntax error: args")
            if args[1] == "remove":
                if len(args) == 3:
                    reward_to_remove_idx = int(args[2])-1
                    self.rewardlist.PopReward(reward_to_remove_idx)
            if args[1] == "consume":
                if len(args) == 3:
                    reward_to_consume_idx = int(args[2])-1
                    self.Consume_Reward(reward_to_consume_idx)
            self.rewardlist.ModePrint("all")
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

    # prog.Load("data")

    # prog.dailylist.PushTask("Healthy Breakfast", False, 20)
    # prog.dailylist.PushTask("Write down todo tasks", False, 20)
    # prog.dailylist.PushTask("Exercise ~20-60 min", False, 20)
    # prog.dailylist.PushTask("Wash face/shower, brush teeth", False, 20)
    # prog.dailylist.PushTask("Complete todo tasks", False, 50)
    # prog.dailylist.PushTask("Duolingo ~20-30 min", False, 20)
    # prog.dailylist.PushTask("Coding Daily: projects, leetcode, codecademy", False, 20)
    # prog.dailylist.PushTask("Read ~30-60 min", False, 20)
    # prog.dailylist.PushTask("Lift", False, 20)

    # prog.Save("data")
    prog.Start()




# ===============================================



main()
