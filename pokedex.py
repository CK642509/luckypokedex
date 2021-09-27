import tkinter as tk
import tkinter.messagebox
from PIL import Image, ImageTk
from functools import partial

# make sure the input is correct
def check(index):
    # check if it is an integer
    try:
        index = int(index)
        
    except(TypeError, ValueError):
        tk.messagebox.showerror(title="Error", message="Invalid input!")
        return False

    # check if the range is correct
    if index <= 0 or index > 493:
        tk.messagebox.showerror(title="Error", message="Invalid input!")
        return False
    else:
        return True

# open or create a file to get shiny list
def open_list():
    try:
        with open('shiny_list.txt', 'r') as file:
            shiny_list = file.read()
            shiny_list = shiny_list.split() # change string to list
            shiny_list = list(map(int, shiny_list)) # change it to int
            return shiny_list

    except FileNotFoundError:
        with open('shiny_list.txt', 'a') as file:
            shiny_list = "" 
            file.write(shiny_list) # write nothing
            return shiny_list
        
# make it shine
def shiny(index):
    r = (index-1) // 15
    c = (index-1) % 15
    buttons[r][c].configure(bg="#766fe2")

# click the pokemon button
def click(i,j):
    index = 15*i+j+1
    buttons[i][j].configure(bg="#766fe2")
    add_list.append(index)
    print(add_list)


def add():
    #global add_index
    pokemon_index = var_index.get()

    # make sure the input is an integer
    is_int = check(pokemon_index)

    if is_int == True:
        pokemon_index = int(pokemon_index)
        add_list.append(pokemon_index)   # add it to the add list
        shiny(pokemon_index)
        
    print(add_list)

def save():
    with open('shiny_list.txt', 'a') as file:
        global add_list
        save_list = list(map(str, add_list))   # change int to string
        save_list = " ".join(save_list)
        file.write(" " + save_list)   # write it into text file
        tk.messagebox.showinfo(title='Success', message='Successfully saved!')
        add_list = []   # reset add list


######################################################################

### build a window
root = tk.Tk()
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame_main = tk.Frame(root, bg="gray")
frame_main.grid(sticky='news')

# create an entry
var_index = tk.StringVar()
entry_index = tk.Entry(frame_main, textvariable=var_index, font=('Arial', 12), width=10)
entry_index.grid(row=0, column=0, pady=(5, 0))


# create an Add button
ab = tk.Button(frame_main, text="Add", font=('Arial', 12), width=10, height=1, command=add)
ab.grid(row=0, column=1, pady=(5, 0))

# create a Save button
sb = tk.Button(frame_main, text="Save", font=('Arial', 12), width=10, height=1, command=save)
sb.grid(row=0, column=2, pady=(5, 0))





# Create a frame for the canvas with non-zero row&column weights
frame_canvas = tk.Frame(frame_main)
frame_canvas.grid(row=2, column=0, columnspan=3, pady=(5, 0), sticky='nw')
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
# Set grid_propagate to False to allow 5-by-5 buttons resizing later
frame_canvas.grid_propagate(False)

# Add a canvas in that frame
canvas = tk.Canvas(frame_canvas, bg="yellow")
canvas.grid(row=0, column=0, sticky="news")

# Link a scrollbar to the canvas
vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)

# Create a frame to contain the buttons
frame_buttons = tk.Frame(canvas, bg="blue")
canvas.create_window((0, 0), window=frame_buttons, anchor='nw')


### set up the parameters ###
add_list = []

# make a list
pokemon = []
for i in range(1, 10):
    img_name = "image/00" + str(i) + "_00.png"
    pokemon.append(img_name)

for i in range(10, 100):
    img_name = "image/0" + str(i) + "_00.png"
    pokemon.append(img_name)
for i in range(100, 1000):
    img_name = "image/" + str(i) + "_00.png"
    pokemon.append(img_name)
    
# make a blank list
test = [None]*493

# Add buttons to the frame
rows = 33
columns = 15
buttons = [[tk.Button() for j in range(columns)] for i in range(rows)]
for i in range(0, rows):
    for j in range(0, columns):
        index = i*15+j
        try:
            test[index] = Image.open(pokemon[index]) # open the image
            test[index] = test[index].resize((64,64),Image.ANTIALIAS) # resize
            test[index] = ImageTk.PhotoImage(test[index]) # open the image
            buttons[i][j] = tk.Button(frame_buttons, image=test[index],bg="#d8cff9", command=partial(click, i,j))
            # if we use command=click(i,j), this method will invoke immediately
        except(FileNotFoundError):
            buttons[i][j] = tk.Button(frame_buttons,bg="#d8cff9")
            
        buttons[i][j].grid(row=i, column=j, sticky='news')


# Update buttons frames idle tasks to let tkinter calculate buttons sizes
frame_buttons.update_idletasks()

# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
first15columns_width = sum([buttons[0][j].winfo_width() for j in range(0, 15)])
first10rows_height = sum([buttons[i][0].winfo_height() for i in range(0, 10)])
frame_canvas.config(width=first15columns_width + vsb.winfo_width(),
                    height=first10rows_height)

# Set the canvas scrolling region
canvas.config(scrollregion=canvas.bbox("all"))

### load data and make it shine
# get the list
shiny_list = open_list()

# make it shine
for x in shiny_list:
    shiny(x)

# Launch the GUI
root.mainloop()
