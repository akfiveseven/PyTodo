class Task:
    def __init__(self, label, is_complete, bounty):
        self.label = label 
        self.is_complete = is_complete
        self.bounty = bounty

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

    def PushTask(self, label, is_complete, bounty):
        self.tasks.append(Task(label, is_complete, bounty))

    def Print(self, mode):
        if (mode == 0):
            print(f"{self.name.upper()} [TODO]")
            for i in self.tasks:
                if (i.is_complete is False):
                    i.Print()
        if (mode == 1):
            print(f"{self.name.upper()} [COMPLETE]")
            for i in self.tasks:
                if (i.is_complete is True):
                    i.Print()
        if (mode == 2):
            print(f"{self.name.upper()} [ALL]")
            for i in self.tasks:
                i.Print()


class Reward:
    def __init__(self, label, is_claimed, price):
        self.label = label 
        self.is_claimed = is_claimed
        self.price = price

    def Print(self):
        if (self.is_claimed):
            print("[X]", end=" ")
        else:
            print("[ ]", end=" ")
        print(f"{self.label}: {self.price}")


class Shop():
    def __init__(self):
        self.rewards = []

    def PushReward(self, label, is_claimed, price):
        self.rewards.append(Reward(label, is_claimed, price))

    def Print(self, mode):
        if (mode == 0):
            print(f"{self.name.upper()} [TODO]")
            for i in self.rewards:
                if (i.is_claimed is False):
                    i.Print()
        if (mode == 1):
            print(f"{self.name.upper()} [COMPLETE]")
            for i in self.rewards:
                if (i.is_claimed is True):
                    i.Print()
        if (mode == 2):
            print(f"{self.name.upper()} [ALL]")
            for i in self.rewards:
                i.Print()


class Interface:
    def __init__(self):
        self.prefix = "[user@automaton] $ "
        self.taskList = None
        self.shop = None

    # def execute(self, command):
        # cmd = command.split(' ')

# ===============================================


def main():
    i = Interface()

    list1 = TaskList("Daily")
    list1.PushTask("t1", False, 10)
    list1.PushTask("t2", True, 20)
    list1.PushTask("t3", False, 30)
    list1.PushTask("t4", True, 40)
    list1.PushTask("t5", True, 50)
    list1.PushTask("t6", True, 60)
    list1.PushTask("t7", False, 70)

    i.taskList = list1
    i.taskList.Print(2)

# ===============================================


main()
