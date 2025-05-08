from tkinter import *
from sqlite3 import *
from tkinter import Frame, Label


#----------------------------------
# FUNCTIONS FOR BUTTONS
#----------------------------------

def enter_into():
    name = Ename.get()
    category = Ecategory.get()
    quantity = Equantity.get()
    location = Elocation.get()

    data = (name, category, quantity, location)

    conn = connect('Food_storage.db')
    c = conn.cursor()

    q = '''
        INSERT INTO Foodstufs (Name, Category, Quantity, Location)
        VALUES(?,?,?,?)
        '''

    c.execute(q, data)
    conn.commit()
    conn.close()

    Ename.delete(0, END)
    Ecategory.delete(0, END)
    Equantity.delete(0, END)
    Elocation.delete(0, END)

def remove_from():
    name = Ename.get()
    category = Ecategory.get()
    

    data = (name, category)

    conn = connect('Food_storage.db')
    c = conn.cursor()

    check_for_existence = '''
        SELECT Name FROM Foodstufs
        WHERE Name = ? AND Category = ?
    '''
    c.execute(check_for_existence, data)
    after_check = c.fetchone()

    q = '''
        DELETE FROM Foodstufs 
        WHERE Name = ? AND Category = ?
        '''
    
    if after_check:
        c.execute(q, data) 
    else: 
        print('There is no such item in the Warehouse.')
    
    conn.commit()
    conn.close()

    Ename.delete(0, END)
    Ecategory.delete(0, END)
    Equantity.delete(0, END)
    Elocation.delete(0, END)

def remove_quantity():
    name = Ename.get()
    quantity = Equantity.get()
    

    data = (quantity, name)

    conn = connect('Food_storage.db')
    c = conn.cursor()

    q = '''
        UPDATE Foodstufs 
        SET Quantity = Quantity - ?
        WHERE Name = ? 
        '''

    c.execute(q, data)
    conn.commit()
    conn.close()

    Ename.delete(0, END)
    Ecategory.delete(0, END)
    Equantity.delete(0, END)
    Elocation.delete(0, END)


def add_to():
    name = Ename.get()
    quantity = Equantity.get()
    if quantity == '':
        quantity = 0

    data = (quantity, name)

    conn = connect('Food_storage.db')
    c = conn.cursor()

    q = '''
        UPDATE Foodstufs 
        SET Quantity = Quantity + ?
        WHERE Name = ? 
        '''

    c.execute(q, data)

    new_number= '''
        SELECT Quantity FROM Foodstufs
        '''
    c.execute(new_number)
    new_sum = c.fetchone()
    turn_to_int  = int(new_sum[0]) #you can use str() method as well. It is important to put the index because fetchone() returns a tuple

    conn.commit()
    conn.close()

    Ename.delete(0, END)
    Ecategory.delete(0, END)
    Equantity.delete(0, END)
    Elocation.delete(0, END)

    Lmessage.config(text='You added {0} units to the {1}/s. Now it counts {2}'.format(quantity, name, turn_to_int), background='black')

#----------------------------------
# TKINTER GUI
#----------------------------------

window = Tk()
window.title('FOOD STORAGE APP')
window.geometry('600x600')
window['bg'] = 'darkred'

#although the window is red, it is not visible because the Frames are gray by default. We change the color of them as well
window.option_add('*Frame.Background', 'darkred')
window.option_add('*Font', 'Arial 14 bold')
window.option_add('*Entry.Justify', 'center')
window.option_add('*Label.Background', 'darkred')
window.option_add('*Label.Foreground', 'white')
window.option_add('*Button.Background', 'darkred')
window.option_add('*Button.Foreground', 'white')

#----------------------------------
# FRAMES FOR GRID POSITIONING
#----------------------------------

Frame1 = Frame(window)
Frame1.grid(row = 0, column = 0, sticky = 'nsew', pady=(100, 0)) #'nsew' means, thw widgets inside that frame will spread in all 4 directions.

Frame2 = Frame(window)
Frame2.grid(row = 0, column = 1, sticky = 'nsew', pady=(100, 0)) 

Frame3 = Frame(window)
Frame3.grid(row = 1, column = 0, sticky = 'nsew') 

Frame4 = Frame(window)
Frame4.grid(row = 1, column = 1, sticky = 'nsew') 

Frame5_message = Frame(window)
Frame5_message.grid(row=2, columnspan=2, pady=(0, 100))


# Making grids responsive
#WITH WEIGHT 1 THE WIDGETS WILL SPREAD ACCORDINGLY, IN CASE OF 1 WILL NOT.
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)



#----------------------------------
# TEXT LABELS 
#----------------------------------

Lname = Label(Frame1, text = 'NAME')
Lname.pack(pady= 10)

Lcategory = Label(Frame1, text = 'CATEGORY')
Lcategory.pack(pady= 10)

Lquantity = Label(Frame1, text = 'QUANTITY')
Lquantity.pack(pady= 10)

Lname = Label(Frame1, text = 'LOCATION')
Lname.pack(pady= 10)

Lmessage = Label(Frame5_message, text='', font='Arial 12 bold')
Lmessage.pack()


#----------------------------------
# ENTRY FIELDS
#----------------------------------

Ename = Entry(Frame2)
Ename.pack(pady= 10)

Ecategory = Entry(Frame2)
Ecategory.pack(pady= 10)

Equantity = Entry(Frame2)
Equantity.pack(pady= 10)

Elocation = Entry(Frame2)
Elocation.pack(pady= 10)


#----------------------------------
# BUTTONS
#----------------------------------

Binput = Button(Frame3, text = 'Put the item inside', command = enter_into)
Binput.pack(pady= 10)

Bremovepart = Button(Frame3, text = 'Remove quantity', command = remove_quantity)
Bremovepart.pack(pady= 10)

Bremove = Button(Frame4, text = 'Add quantity', command = add_to)
Bremove.pack(pady= 10)

Bremove = Button(Frame4, text = 'Delete the item', command = remove_from)
Bremove.pack(pady= 10)




# Configure grid to be responsive
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(1, weight=1)

window.mainloop()
