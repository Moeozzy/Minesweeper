#Här kallar jag på olika moduler men även en python fil vilket inehåller en klass.
from tkinter import *
from tkinter import messagebox
import sys
import os
from operator import attrgetter
from Mine_Class import *
import time
import random

#Detta är fönstret som öppnas vid start av programet, I detta tkinter fönster
#Så kan man starta spelet, se highscore, ta upp instruktionerna och ställa in spelplanen.
#Fönstret består av knappar, två skalor och samt en input för användaren.
def mainmenu(main_screen):
    Button(main_screen, bg = "BLACK", fg = "WHITE", text = "Instructions:", command = lambda: view_instructions()).pack()
    Label(main_screen, bg = "BLACK", fg = "WHITE", text = "Name:").pack()
    nameinput = Entry(main_screen)
    nameinput.pack()
    Label(main_screen, bg = "BLACK", fg = "WHITE", text = "Number of rows:").pack()
    row = Scale(main_screen, bg = "BLACK", fg = "WHITE", from_= 6, to = 32, orient = HORIZONTAL)
    row.pack()
    Label(main_screen, bg = "BLACK", fg = "WHITE", text = "Number of columns:").pack()
    col = Scale(main_screen, bg = "BLACK", fg = "WHITE", from_= 6, to = 32, orient = HORIZONTAL)
    col.pack()
    Label(main_screen, bg = "BLACK", fg = "WHITE", text = " Procentage of Mines:").pack()
    mines = Scale(main_screen, bg = "BLACK", fg = "WHITE", from_= 15, to = 70, orient = HORIZONTAL)
    mines.pack()
    start_button = Button(main_screen, text = "Play", width = 25, fg = "GREEN", bg = "BLACK", command = lambda: Game_screen(row, col, mines, nameinput, main_screen))
    start_button.pack() 
    Button(main_screen, text = "Exit", width = 25, fg = "RED", bg = "BLACK", command = main_screen.destroy).pack() 
    Button(main_screen, text = "Highscores", width = 25, fg = "GOLD", bg = "BLACK", command = lambda: ShowHighscores()).pack()
    main_screen.config(bg = "BLACK")

#Denna funktion körs vid klick av "Instructions". Då öppnas en ny tkinter fönster
#Som användaren kan använda för att läsa om hur man spelar. Vid stänging av fönstret
#Så försvinner den och mainmenu kan användas
def view_instructions():
    instructions = Toplevel()
    instructions.title("Instructions")
    message = Text(instructions)
    message.insert(INSERT, """\t*********** INSTRUCTIONS ***********
\tHow to win:
- By revealing all squares without a mine or...
- "flagging" all squares with mines.
\tLeftclick:
- Opens selected square.
- * = Mine, you revealed a mine thus lost the game.
- 1-8 = Amount of mines that are adjacent to a square.
- Empty = No mines are adjacent to this square. 
  All adjacent squares without mines are automatically revealed.
\tRightclick:
- You can flag squares you suspect are mines.
- You can only win by flagging mines and only mines.
\tChoose dimensions:
- You can select the amount of rows and columns.
  Remember the bigger the board the harder it is.
\tTip:
- Use the numbers to determine where you know a bomb is.
\t*********** GOOD LUCK ***********""")
    message.config(bg = "BLACK", fg = "WHITE")
    message.pack()

#Den här funktionen visar då topplistan vid click av knappen "Highscores".
#Det den gör också är att den läser in topplistan genom en for-lopp
#Detta är för att göra det lättare att ordna samt numrera topplistan.
#Här använder jag mig även av Typerror, vilket är en felhantering om ingen är med i topplistan.
#Då sskriver den bara ut texten "No highscores made yet."
def ShowHighscores():
    Highscore_list = read_file()
    highscore = Toplevel()
    highscore.title("Highscores")
    message = Text(highscore)
    try:
        for i in range (len(Highscore_list)):
            message.insert(INSERT, str(i+1) + ". " + str(Highscore_list[i]) + "\n")
        highscore.config(bg = "BLACK")
        message.config(bg = "BLACK", fg  = "WHITE")
        message.pack()
    except TypeError:
        message.insert(INSERT, "No Highscores made yet.")
        highscore.config(bg = "BLACK")
        message.config(bg = "BLACK", fg  = "WHITE")
        message.pack()

#Den här funktionen används för att sortera listan via tre olika attribut (snabbast tid, störst plan och antalet minor)
#Det attregetter gör är att den frågar om attributen från operatorn och om det är mer än 1 så
#Kommer den att göra det till en tuple.
def sort_list(Highscore_list, attribute):
    for key, reverse in reversed(attribute):
        Highscore_list.sort(key = attrgetter(key), reverse = reverse)
    return Highscore_list

#Den här funktionen läser av filen för topplistan
#Det den använder är av en try och except för felhantering.
#Funktionen börjar med att först kolla om fillen ligger i samma sökväg som programmet om inte så
#Kommer except köras och då skapas en ny fil. Om filen finns så läses den genom en for lopp.
#Samt så definereas "Keys" till sort_list
def read_file():
    Highscore_list = []
    try:
        with open(os.path.join(sys.path[0], "Mine score.txt"), "r") as file:
            text = file.readlines()
            for row in text:
                name, size, mines, time = row.split(" ")
                Highscore_list.append(Win(name, size, mines, time))
            sort_list(Highscore_list, (("size", True), ("mines", True), ("time", False)))
            return Highscore_list
    except IOError:
        file = open(os.path.join(sys.path[0], "Mine score.txt"), "w")

#Här sparas filen och så öppnas den även genom os modulen. Så sparas även filen med attributen namn, storlek och tid.
#Här används även tidsfunktionen för att spara tiden.
def save_file(name, time_stop, time_start, row, col, mines):
    with open(os.path.join(sys.path[0], "Mine score.txt"), "a") as file:
        file.write(str(name) + " " + str(row*col) + " " + str(mines) + " " + str(round(time_stop-time_start, 2)) + "\n")
        file.close()

#Här är felhanteringen för användarens input. Du får alltså bara använda dig av bokstäver (isalpha) 
#Samt så får du bara ha ett namn med max 15 bokstäver och minst 1.
#Vid fel inmatning så körs en messagebox och då tas tillbacks till mainmenu.
def check_name(name, main_screen):
    if len(name) >= 15:
        messagebox.showerror("Error:", "Your name cant exceed 15 characters, try again.")
        main_screen.destroy()
        main()
    if not name.isalpha():
        messagebox.showerror("Error:", "Your name can only contain letters and atleast one, try again.")
        main_screen.destroy()
        main()

#Det här är funktionen för spel fönstret och är det tkinter fönstret som öppnas vid click av "Play"
#Den tar emot infromation såsom antal rader, kol och namn som användaren har uppgett.
#Lambda används för att köra en funktion i en annan funktion och commando är det som händer vid klick av knappen
#Jag gör spelplanen till en lista som sedan fylls med knappar via en for-loop
#Kallar även på funktionen "Squares" som är algorithemn för hur spelpölanen röjs.
#Buttons är de rutor man trycker på som sedan även kör vänster och högerclick.
#Field är en lista för vart innehållet av knapparna befinner sig. Fylls på med nya listor motsvarande antalet rader
#Den stänger även huvudmenyn fönstret innan den öppnar sig själv.
#Denna funktion inehåller även en timer som används för att sortera topplistan.     
def Game_screen(row, col, mines, nameinput, main_screen):
    row = row.get()
    col = col.get()
    name = nameinput.get()
    mines = (mines.get()/100)
    check_name(name, main_screen)
    main_screen.destroy()
    Game_screen = Tk()
    Game_screen.title("Mine")
    Game_screen.config(bg="BLACK")
    Button(Game_screen, fg = "WHITE", bg = "BLACK", text="Mainmenu", width = 25, command=lambda:[Game_screen.destroy(),main()]).grid(row=row-1, column=col+1)
    field = []
    for x in range(row):
        field.append([])
        for y in range(col):
            field[x].append(0)
    Squares(x, y, row, col, mines, field)
    buttons = []
    for x in range(row):
        buttons.append([])
        for y in range(col):
            button = Button(Game_screen, width = 2, height = 1, bg = "saddlebrown", disabledforeground = "BLACK")
            button.grid(row=x, column=y, sticky=N+W+S+E)
            button.bind("<Button-1>", lambda i, x=x, y=y: left_click(x, y, col, row, mines, buttons, field, mines_flagged, flagged_squares, Game_screen, name, minutes, seconds, time_start))
            button.bind("<Button-3>", lambda j, x=x, y=y: right_click(x, y, col, row, mines, buttons, field, Game_screen, mines_flagged, flagged_squares, name, minutes, seconds, time_start))
            buttons[x].append(button)
    minutes = 0
    seconds = 0
    mines_flagged = []
    flagged_squares = []
    time_start = time.time()
    check_win(Game_screen, row, col, mines, x, y, field, buttons, mines_flagged, flagged_squares, name, minutes, seconds, time_start)
    #Verktyg för att se vart minorna befinner sig.
    print(field)

#Denna funktion används för att nummrerar rutor som angränsar minor.
#Här bestäms även procentandelen minor
#Här finns även algoritmen som numrerar rutorna via antalet angränsande minor
def Squares(x, y, row, col, mines, field):
    for i in range(int(mines*row*col)):
        x = random.randint(0, row-1)
        y = random.randint(0, col-1)
        while field[x][y] == -1:
            x = random.randint(0, row-1)
            y = random.randint(0, col-1)
        field[x][y] = -1
        if x != 0 and y != 0 and field[x-1][y-1] != -1:
            field[x-1][y-1] = int(field[x-1][y-1]) + 1
        if x != 0 and field[x-1][y] != -1:
            field[x-1][y] = int(field[x-1][y]) + 1
        if x != 0 and y != col-1 and field[x-1][y+1] != -1:
            field[x-1][y+1] = int(field[x-1][y+1]) + 1
        if y != 0 and field[x][y-1] != -1:
            field[x][y-1] = int(field[x][y-1]) + 1
        if y != col-1 and field[x][y+1] != -1:
            field[x][y+1] = int(field[x][y+1]) + 1
        if y != 0 and x != row-1 and field[x+1][y-1] != -1:
            field[x+1][y-1] = int(field[x+1][y-1]) + 1        
        if x != row-1 and field[x+1][y] != -1:
            field[x+1][y] = int(field[x+1][y]) + 1
        if x != row-1 and y != col-1 and field[x+1][y+1] != -1:
            field[x+1][y+1] = int(field[x+1][y+1]) + 1  

#left_click används för att köras när användaren vänsterklickar på en ruta.
#Den kollar även om rutan är flaggade, då kan inte användaren väsnterklicka utan att ta bort flaggan.
#Om rutan innehåller en siffra öppnas den och visar siffran.
#Om rutan innehåller en nolla så kommer funktionen autoclick köras för att öppna angränsade rutor fram tills en mina angränsar
#Om rutan innehåller en mina så öppnas alla rutor, visar vart minorna är och en messagebox körs för att säga att spelet är slut
#Samt även visar antalet minor du har flaggat av totala minorna.
#Funktionen ersätter även -1 med * för att indikera en mina.
#Vid förlust så tas användaren tillbaks till mainmenu   
def left_click(x, y, col, row, mines, buttons, field, mines_flagged, flagged_squares, Game_screen, name, minutes, seconds, time_start):
    if buttons[x][y]["text"] != "F":
        if field[x][y] != 0:
            buttons[x][y].config(bg = "#AF6500", text=field[x][y], state=DISABLED, relief=SUNKEN)
        if field[x][y] == 0:
            auto_click(x, y, col , row, mines, buttons, field, mines_flagged, flagged_squares, Game_screen, name, minutes, seconds, time_start)
            buttons[x][y].config(bg = "#AF6500", state=DISABLED, relief=SUNKEN)
        check_win(Game_screen, row, col, mines, x, y, field, buttons, mines_flagged, flagged_squares, name, minutes, seconds, time_start) 
        if field[x][y] == -1:
            for x in range(row):
                for y in range(col ):
                    if field[x][y] != 0:
                        buttons[x][y].config(bg = "#AF6500", relief=SUNKEN, state=DISABLED, text=field[x][y])
                    elif field[x][y] == 0:
                        buttons[x][y].config(bg = "#AF6500", relief=SUNKEN, text=" ")
                    if field[x][y] == -1:
                        buttons[x][y].config(text="*", bg="red", relief=SUNKEN)
            messagebox.showerror("Game over", "You sweept: " + str(len(mines_flagged)) + " bombs, out of " + str(int(mines*row*col)) + " total. Better luck next time.")
            Game_screen.destroy()
            main() 

#Denna funktion används för att flagga rutorna genom användarens högerclick.
#Om rutan inte har en flagga så läggs en flagga till vid högerclick.
#Om rutan har redan en flagga tas den bort vid högerclick.
#Antalet flaggade minor av alla minor sparas även i variabler "mines_flagged" och "flagged_squares" för att jämföra och används som ett verktyg
#Detta görs genom en räknare som tar bort eller lägger till ett index
#Efter varje högerclick så körs även check_win för att kolla om villkoren är uppfyllda.
def right_click(x, y, col, row, mines, buttons, field, Game_screen, mines_flagged, flagged_squares, name, minutes, seconds, time_start):
    if buttons[x][y]["text"] != "F" and buttons[x][y]["state"] != "disabled":
        if field[x][y] == -1:
            mines_flagged.append(1)
        elif field[x][y] != -1:
            flagged_squares.append(1)
        buttons[x][y].config(text = "F", command = lambda x=x, y=y: left_click(x, y, col, row, mines, buttons, field, mines_flagged, flagged_squares, Game_screen, name, minutes, seconds, time_start))  
    elif buttons[x][y]["text"] == "F":
        if field[x][y] == -1:
            mines_flagged.remove(1)
        elif field[x][y] != -1:
            flagged_squares.remove(1)
        buttons[x][y].config(text = " ", command = lambda x=x, y=y: left_click(x, y, col, row, mines, buttons, field, mines_flagged, flagged_squares, Game_screen, name, minutes, seconds, time_start))
    check_win(Game_screen, row, col, mines, x, y, field, buttons, mines_flagged, flagged_squares, name, minutes, seconds, time_start)
    #Verktyg för att visa antalet flaggade minor av alla.
    #print("mines: " + str(len(mines_flagged)) + " None mine: " + str(len(flagged_squares)))

#Denna funktion körs när spelet behöver öppna angränsade minor automatiskt, när t.ex. man öppnar en tom ruta
#Detta görs genom rekursion för att kalla på sig själv tills minor angränsar.
def auto_click(x, y, col, row, mines, buttons, field, mines_flagged, flagged_squares, Game_screen, name, minutes, seconds, time_start):
    if buttons[x][y]["state"] == "disabled":
        return
    else:
        buttons[x][y].config(state=DISABLED, relief=SUNKEN)
    if field[x][y] == 0:
        if x != 0 and y != 0:
            left_click(x-1, y-1, col, row, mines, buttons, field, mines_flagged, flagged_squares, Game_screen, name, minutes, seconds, time_start)  
        if x != 0:
            left_click(x-1, y, col, row, mines, buttons, field, mines_flagged, flagged_squares, Game_screen, name, minutes, seconds, time_start) 
        if x != 0 and y != col-1:
            left_click(x-1, y+1, col, row, mines, buttons, field, mines_flagged, flagged_squares, Game_screen, name, minutes, seconds, time_start)
        if y != 0:
            left_click(x, y-1, col, row, mines, buttons, field, mines_flagged, flagged_squares, Game_screen, name, minutes, seconds, time_start)
        if y != col-1:
            left_click(x, y+1, col, row, mines, buttons, field, mines_flagged, flagged_squares, Game_screen, name, minutes, seconds, time_start)
        if x != row-1 and y != 0:
            left_click(x+1, y-1, col, row, mines, buttons, field, mines_flagged, flagged_squares, Game_screen, name, minutes, seconds, time_start)
        if x != row-1:
            left_click(x+1, y, col, row, mines, buttons, field, mines_flagged, flagged_squares, Game_screen, name, minutes, seconds, time_start) 
        if x != row-1 and y != col-1:
            left_click(x+1, y+1, col, row, mines, buttons, field, mines_flagged, flagged_squares, Game_screen, name, minutes, seconds, time_start)  

#Check_win ansvarar för att kolla im användaren har uppfyllt villkoren för en vinst. Detta körs efter varje knappklickning.
#Börjar med att sätta vinst till sant och kollar om vilkoren är uppfyllda
#Om den inte är uppfylld genom att flagga eller öppna alla rutor utan minor. Så returnerar den false
#Men om det är ippfylld retunerar den true.
#Om true returneras så kommer timern att stoppas och så öppnas alla rutor för att visa vart minorna befinner sig.
#Siffrorna färgas även här-
#save_file körs för att spara vinsten.
#En messsagebox kommer sedan att öppnas för att visa vinsten med info såsom namn, storlek och tid.
#Fönstret stängs och användaren tas till mainmenu       
def check_win(Game_screen, row, col, mines, x, y, field, buttons, mines_flagged, flagged_squares, name, minutes, seconds, time_start):
    win = True
    for x in range(row):
        for y in range(col):
            if field[x][y] != -1 and buttons[x][y]["relief"] != "sunken":
                win = False
    if int(len(mines_flagged)) == int(mines*row*col) and int(len(flagged_squares)) == 0:
        win = True
    if win:
        time_stop = time.time()
        #Verktyg för att se tiden i terminalen.
        #print(time_stop-time_start)
        for x in range(row):
            for y in range(col):
                if field[x][y] == 0:
                    buttons[x][y].config(state=DISABLED, relief=SUNKEN, text=" ")
                elif field[x][y] == -1:
                    buttons[x][y].config(state=DISABLED, relief=SUNKEN, bg="GREEN", text="F")
                else:
                    buttons[x][y].config(state=DISABLED, relief=SUNKEN, text=field[x][y])
        save_file(name, time_stop, time_start, row, col, mines)
        messagebox.showinfo("You Win! ", str(name) + " You sweept all mines in: " + str(round(time_stop-time_start, 2)) + " seconds.")
        Game_screen.destroy()
        main()

#Main funktionen startar mainmenu fönstret.
def main():
    main_screen = Tk()
    main_screen.title("Mine")
    mainmenu(main_screen)
    main_screen.mainloop()

main()
