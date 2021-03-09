class Win():
    #En konstriuktion som anropas om en spelare vinner.
    def __init__(self, name, size, mines, time):
        self.name = name
        self.size = int(size)
        self.mines = int(float(mines)*100)
        self.time = float(time)

    def __repr__(self):
        #Formaterar strängen.
        return str(f"{self.name:1}") + ", Size:" + str(f"{self.size:2}") + " squares, Mines: "  + str(f"{self.mines:2}") + "%, Time: " + str(f"{self.time:3}" + "s.")
