from tkinter import *
from sqlite3 import *
from tkinter import Toplevel, Frame, Label, Listbox, ttk


class FoodStorageApp:
    def __init__(self, window):
#----------------------------------
# TKINTER GUI
#----------------------------------
        self.window = window 
        self.window.title('FOOD STORAGE APP')
        self.window.geometry('900x900')
        self.window['bg'] = 'darkred'

        self.create_widgets()
        self.connection() 

    def create_widgets(self):
        self.window.option_add('*Frame.Background', 'darkred') #although the window is red, it is not visible because the Frames are gray by default. We change the color of them as well
        self.window.option_add('*Font', 'Arial 14 bold')
        self.window.option_add('*Entry.Justify', 'center')
        self.window.option_add('*Label.Background', 'darkred')
        self.window.option_add('*Label.Foreground', 'white')
        self.window.option_add('*Button.Background', 'darkred')
        self.window.option_add('*Button.Foreground', 'white')
        

#----------------------------------
# FRAMES FOR GRID POSITIONING
#----------------------------------

        Frame1 = Frame(self.window)
        Frame1.grid(row=0, column=0, sticky='nsew', pady=(100, 0))

        Frame2 = Frame(self.window)
        Frame2.grid(row=0, column=1, sticky='nsew', pady=(100, 0))

        Frame3 = Frame(self.window)
        Frame3.grid(row=1, column=0, sticky='nsew')

        Frame4 = Frame(self.window)
        Frame4.grid(row=1, column=1, sticky='nsew')

        Frame5_message = Frame(self.window)
        Frame5_message.grid(row=2, columnspan=2, pady=(0, 100))

        self.create_labels(Frame1)
        self.create_entries(Frame2)
        self.create_buttons(Frame3, Frame4)
        self.Lmessage = Label(Frame5_message, text='', font='Arial 12 bold')
        self.Lmessage.pack()

# Making grids responsive
#WITH WEIGHT 1 THE WIDGETS WILL SPREAD ACCORDINGLY, IN CASE OF 0 WILL NOT.

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)

#----------------------------------
# TEXT LABELS 
#----------------------------------
    def create_labels(self, frame):
        Label(frame, text='NAME').pack(pady=10)
        Label(frame, text='CATEGORY').pack(pady=10)
        Label(frame, text='QUANTITY').pack(pady=10)
        Label(frame, text='LOCATION').pack(pady=10)
#----------------------------------
# ENTRY FIELDS
#----------------------------------
    def create_entries(self, frame):
        self.Ename = Entry(frame)
        self.Ename.pack(pady=10)

        self.Ecategory = Entry(frame)
        self.Ecategory.pack(pady=10)

        self.Equantity = Entry(frame)
        self.Equantity.pack(pady=10)

        self.Elocation = Entry(frame)
        self.Elocation.pack(pady=10)

#----------------------------------
# BUTTONS
#----------------------------------
    def create_buttons(self, frame3, frame4):
        Button(frame3, text='Put the item inside', command=self.enter_into).pack(pady=10)
        Button(frame3, text='Remove quantity', command=self.remove_quantity).pack(pady=10)
        Button(frame4, text='Add quantity', command=self.add_to).pack(pady=10)
        Button(frame4, text='Delete the item', command=self.remove_from).pack(pady=10)
        Button(frame3, text='Show data', command = self.create_show_window).pack(pady=10)

    def create_show_window(self):
        
        def show_all():
            show_all_window=Toplevel()
            show_all_window.geometry('400x300')
            tree = ttk.Treeview(show_all_window, columns=('Name', 'Category', 'Quantity', 'Location'), show='headings')
            tree.heading('Name', text='NAME', anchor='w')
            tree.heading('Category', text='CATEGORY', anchor='w') #anchor(west) aligns the text to the left
            tree.heading('Quantity', text='QUANTITY', anchor='w')
            tree.heading('Location', text='LOCATION', anchor='w')

            tree.pack(fill='both', expand=True)
            # Adjusting the column widths
            tree.column('Name', width=100)
            tree.column('Category', width=100)
            tree.column('Quantity', width=100)
            tree.column('Location', width=100)
          

            q = '''
            SELECT * FROM Foodstufs
            '''
#LISTBOX DOESN'T SUPPORT COMPLICATED FORMMATING: THUS WE USE Treview
            lines = self.c.execute(q)
            for line in lines:
                tree.insert('', 'end', values=(line))
            show_all_window.mainloop()

        def create_show_widgets():
            Frame1_inshow = Frame(self.show_window)
            Frame1_inshow.grid(row=0, columnspan=2, sticky='nsew', pady=10)
            Ltitle = Label(Frame1_inshow, text='SHOW DATA FROM DATABASE').pack(pady=10)

            Frame2_inshow = Frame(self.show_window)
            Frame2_inshow.grid(row=1, column=0, sticky='nsew', pady=10)
            Bshow_all = Button(Frame2_inshow, text='SHOW ALL DATA', command=show_all).pack(pady=10)

            self.show_window.grid_rowconfigure(0, weight=1)
            self.show_window.grid_columnconfigure(0, weight=1)
            self.show_window.grid_rowconfigure(1, weight=1)
            self.show_window.grid_columnconfigure(1, weight=1)

        self.show_window = Toplevel(self.window)
        self.show_window.geometry('333x300')
        self.show_window['bg'] = 'white'
        self.show_window.option_add('*Label.Foreground', 'black')  # Changed to black for visibility
        self.show_window.option_add('*Label.Font', 'Arial 12 bold')
        self.show_window.option_add('*Frame.Background', 'white')

        create_show_widgets()

        self.show_window.mainloop()


        

            

#----------------------------------
# FUNCTION TO OPEN AND ACCESS THE DATABASE IMMEDIATELY
#----------------------------------
    def connection(self): #with this function we make the connection every time when starting the program. Thus reducing the code in every function for button. This method is called inside of def __init__
        self.conn = connect('Food_storage.db')
        self.c = self.conn.cursor()

#----------------------------------
# FUNCTIONS FOR BUTTONS
#----------------------------------
#----------------------------------
# FUNCTIONS FOR ENTERING AN ITEM
#----------------------------------
    def enter_into(self): 
        name = self.Ename.get()
        category = self.Ecategory.get()
        quantity = self.Equantity.get()
        location = self.Elocation.get()

        data = (name, category, quantity, location)

        q = '''
            INSERT INTO Foodstufs (Name, Category, Quantity, Location)
            VALUES(?,?,?,?)
        '''

        check_for_existence = '''
                SELECT Name FROM Foodstufs
                WHERE Name = ?
            '''
        is_there = self.c.execute(check_for_existence, (name,)).fetchone() 
        if is_there:
            is_there = is_there[0]
        if name != '' and category != '' and quantity != '' and location != '':
            self.c.execute(q, data)
            self.conn.commit()
            self.clear_entries()
            self.Lmessage.config(text='You entered new item to the warehouse:\n {0} units of the {1}/s ({2}). Location: {3}'.format(quantity, name, category, location))
        elif name != '' and name == is_there:
            self.Lmessage.config(text='{0} is already in the database. \n You can add or remove some quantity.'.format(name))
        else:
            self.Lmessage.config(text='Please, fill in all the fields.')

#----------------------------------
# FUNCTIONS FOR DELETING AN ITEM FROM DATABASE
#----------------------------------

    def remove_from(self): 
        name = self.Ename.get()
        category = self.Ecategory.get()
        data = (name, category)

        after_check = self.c.fetchone()

        q = '''
            DELETE FROM Foodstufs 
            WHERE Name = ? AND Category = ?
        '''

        if name != '' and category != '':
            check_for_existence = '''
                SELECT Name FROM Foodstufs
                WHERE Name = ? AND Category = ?
            '''
            self.c.execute(check_for_existence, data)
            if after_check:
                self.c.execute(q, data)
                self.conn.commit() 
                #here would usually come the closing of the database. We avoid that, because we opened it once in main method. It will not reopen until next time we open the program. 
            
                self.clear_entries()
                self.Lmessage.config(text='You deleted {0}/s from the database.'.format(name))

            else:
                self.Lmessage.config(text='There is no such item in the database.')

            
        else:
            self.Lmessage.config(text='Fill the name and category fields.')


        

        
#----------------------------------
# FUNCTIONS FOR REMOVING THE QUANTITY FROM EXISTING ITEM
#----------------------------------

    def remove_quantity(self):
        name = self.Ename.get()
        quantity = self.Equantity.get()

        data = (quantity, name)

        q = '''
            UPDATE Foodstufs 
            SET Quantity = Quantity - ?
            WHERE Name = ? 
        '''

        check_for_existence = '''
                SELECT Name FROM Foodstufs
                WHERE Name = ?
            '''
        is_there = self.c.execute(check_for_existence, (name,)).fetchone() 
        if is_there:
            is_there = is_there[0]

        if name == '' or quantity == '':
            self.Lmessage.config(text='Please, fill in the name and quantity fields.')
        elif name != '' and quantity != '' and name != is_there:
            self.Lmessage.config(text='That item is not in the database.')
        else:
            self.c.execute(q, data)
            self.conn.commit()
            self.clear_entries()

#----------------------------------
# FUNCTIONS FOR ADDING THE QUANTITY TO AN EXISTING ITEM
#----------------------------------
    def add_to(self): 
        name = self.Ename.get()
        quantity = self.Equantity.get()
        if quantity == '':  #making sure the absence of quantity entry will be 0
            quantity = 0

        data = (quantity, name)

        q = '''
            UPDATE Foodstufs 
            SET Quantity = Quantity + ?
            WHERE Name = ? 
        '''       


        check_for_existence = '''
                SELECT Name FROM Foodstufs
                WHERE Name = ?
            '''
        is_there = self.c.execute(check_for_existence, (name,)).fetchone() 
        if is_there:
            is_there = is_there[0]

        if name !='' and quantity != '' and name == is_there:  
            self.c.execute(q, data)
            new_number = '''
            SELECT Quantity FROM Foodstufs
            WHERE Name = ? 
            '''
            self.c.execute(new_number, (name,))
            new_sum = self.c.fetchone()
            turn_to_int = int(new_sum[0]) #you can use str() method as well. It is important to put the index because fetchone() returns a tuple

            self.Lmessage.config(text='You added {0} units to the {1}/s. Now it counts {2}'.format(quantity, name, turn_to_int))
            self.conn.commit()
            self.clear_entries()
        elif name != '' and quantity != '' and name != is_there:
            self.Lmessage.config(text='That item is not in the database.')
        else:
            self.Lmessage.config(text='Please, fill in all the fields.')


#----------------------------------
# FUNCTION FOR DELETING ENTRY FILEDS
#----------------------------------
    def clear_entries(self): 
        self.Ename.delete(0, END)
        self.Ecategory.delete(0, END)
        self.Equantity.delete(0, END)
        self.Elocation.delete(0, END)




#----------------------------------
# starting THE GUI with mainloop()
#----------------------------------
root = Tk()
app = FoodStorageApp(root)
root.mainloop()
