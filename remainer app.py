import sqlite3 as sq
import tkinter as tk
from tkinter import ttk
from win10toast import ToastNotifier
import multiprocessing
import tkcalendar as tc
import time
import re
import datetime


db = sq.connect("event remainder.db")
cursor = db.cursor()
cmd1 = ('''CREATE TABLE IF NOT EXISTS EVENTS
(EVENT NAME,DATE,TIME)
''')

cursor.execute(cmd1)
e_date = ""
def first(s):

    root = tk.Tk() # Defining the main app
    root.title("Event Remainder App")
    root.geometry("800x400+50+50")

    def events(self):
        event_name = EventEntry.get()
        event_date = DateEntry.get()
        event_date = e_date
        event_time = EventTimeEntry.get()

        a,b = 'Enter your event name...',len(event_name)
        c,d = 'Enter date : dd/mm/yyyy',len(event_date)
        e,f = 'time:hh:mm,ex:16:30 as 4:30PM',len(event_time)

        
        if (event_name == a or b == 0) and (event_date == c or d == 0) and (event_time == e or f == 0) :
            Output.config(text = "Please fill in the event name, event date as dd/mm/yyyy and event time as hh:mm,ex:16:30 as 4:30PM")
        elif (event_name == a or len(event_name) == 0) and (event_date != c or d != 0) and (event_time == e or f == 0) :
            Output.config(text = "Please Enter  event name and event time as hh:mm,ex:16:30 as 4:30PM")
        elif (event_name == a or len(event_name) == 0) and (event_date == c or d == 0) and (event_time != e or f != 0) :
            Output.config(text = "Please Enter  event name and event date as dd/mm/yyyy") 
        elif (event_name == a or len(event_name) == 0) and (event_date == c or d == 0) and (event_time != e or f != 0) :
            Output.config(text = "Please Enter event name and event date as dd/mm/yyyy")
        elif (event_name != a or len(event_name) != 0) and (event_date == c or d == 0) and (event_time == e or f == 0) :
            Output.config(text = "Please Enter event date as dd/mm/yyyy and event time as hh:mm,ex:16:30 as 4:30PM")
        elif (event_name != a or len(event_name) != 0) and (event_date == c or d == 0) and (event_time == e or f == 0) :
            Output.config(text = "Please Enter  event date as dd/mm/yyyy and event time as hh:mm,ex:16:30 as 4:30PM")
        elif (event_name == a or len(event_name) == 0) and (event_date != c or d != 0) and (event_time == e or f == 0) :
            Output.config(text = "Please Enter  event name and event time as hh:mm,ex:16:30 as 4:30PM")
        elif (event_name != a or len(event_name) != 0) and (event_date != c or d != 0) and (event_time == e or f == 0) :
            Output.config(text = "Please Enter  event time as hh:mm,ex:16:30 as 4:30PM")
        elif (event_name != a or len(event_name) != 0) and (event_date == c or d == 0) and (event_time != e or f != 0) :
            Output.config(text = "Please Enter  event date as dd/mm/yyyy")
        elif (event_name == a or len(event_name) == 0) and (event_date != c or d != 0) and (event_time != e or f != 0) :
            Output.config(text = "Please Enter  event name")
        else:
            regex = "^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$"
            p = re.compile(regex)
            m = re.search(p, event_time)
            if (event_time == "") :
                Output.config(text = "Please Enter event time as hh:mm")
            if m is None :
                Output.config(text = "Please Enter valid event time as hh:mm")
            else:
                try:
                    datetime.datetime.strptime(event_date, '%d/%m/%Y')
                except ValueError:
                    Output.config(text = "Please Enter valid event date as dd/mm/yyyy")
                else:
                    now = datetime.datetime.now()
                    ut1,ut2 = event_time.split(":")
                    ut = ut1 + ut2
                    st = now.strftime("%H:%M")
                    st1,st2 = st.split(":")
                    st = st1+st2
                    d1 = event_date
                    d2 = now.strftime("%d/%m/%Y")
                    if d1<d2:
                        Output.config(text = "Please Enter date of today or greater")
                    elif ut <= st :
                        Output.config(text = "Please Enter time greater than current time")
                    else:
                        sql_data = cursor.execute('''SELECT EVENT FROM EVENTS WHERE EVENT = (?)''', (event_name,))
                        sql_data = cursor.fetchall()
                        if len(sql_data) == 0 or sql_data is None:
                            cursor.execute(f'''INSERT INTO EVENTS (EVENT,DATE,TIME) VALUES("{event_name}","{event_date}","{event_time}")''')
                            db.commit()
                            Output.config(text = "event remainder succcess")
                        else:
                            i = (event_date,event_time)
                            db.row_factory = lambda event_name, row: row[0]
                            j = cursor.execute('SELECT DATE,TIME FROM EVENTS').fetchall()
                            if i in j:
                                Output.config(text = "event already exists")
                            else:
                                cursor.execute(f'''INSERT INTO EVENTS (EVENT,DATE,TIME) VALUES("{event_name}","{event_date}","{event_time}")''')
                                db.commit()
                                Output.config(text = "event remainder succcess")


    def delete_event(self):
        selected_item = tree.selection() 
        for selected_item in tree.selection():
            db.execute("DELETE FROM EVENTS WHERE EVENT=?", (tree.set(selected_item, '#1'),))
            db.commit()
            tree.delete(selected_item)

    def viewevents(self):   # view and take command to delete
        frame1.place_forget()
        frame2.place(x=0,y=0,height=800,width=1000)
        #print("all events")
        db = sq.connect("event remainder.db")

        cursor = db.cursor()

        cursor.execute("SELECT * FROM EVENTS")

        rows = cursor.fetchall()    

        for row in rows:

            #print(row) 

            tree.insert("", tk.END, values=row)        

        db.close()

    def backtoapp(self):
        while True:
            for i in tree.get_children():
                tree.delete(i)
            break
        frame2.place_forget()
        frame1.place(x=0,y=0,height=800,width=1000)


    def event_focus_in(_):
        EventEntry.delete(0, tk.END)
        EventEntry.config(fg='black')
    def date_focus_in(_):
        DateEntry.delete(0, tk.END)
        DateEntry.config(fg='black')
    def time_focus_in(_):
        EventTimeEntry.delete(0, tk.END)
        EventTimeEntry.config(fg='black')

    def get_date(self):
        root = tk.Tk()
        root.title("Date Picker")
        root.geometry("350x350+50+50")
        today = datetime.date.today()
        cal = tc.Calendar(root, selectmode='day',cursor="hand1",date_pattern="dd/mm/yyyy", year=today.year, month=today.month, day=today.day)
        cal.place(x=50,y=0,height=250,width=250)
        def grad_date():
            global e_date
            e_date = cal.get_date()
            DateEntry.delete(0, tk.END)
            DateEntry.insert(0,e_date)
            DateEntry.config(font=("arial",10,"bold"),fg='black')
            root.destroy()
            return e_date
        tk.Button(root,text ="Pick Date",command = grad_date).place(x=100,y=250,height=25,width=100)

        #root.mainloop()


    frame1 = tk.Frame(root) #Creating a Frame for root app
    global DateEntry
    EventEntry=tk.Label(text="Enter Event Name:",font=("arial",15,"bold")).place(x=30,y=40,height=20,width=200)
    EventEntry=tk.Entry(root) #Taking Event Name
    EventEntry.insert(0,"Enter your event name...")
    EventEntry.bind("<FocusIn>", event_focus_in)
    EventEntry.config(font=("arial",10,"bold"),fg='grey')
    EventEntry.place(x=40,y=60,height=25,width=320)

    DateEntry=tk.Label(text="Event Date:",font=("arial",15,"bold")).place(x=30,y=90,height=20,width=130)  #eventname label creation
    DateEntry=tk.Entry(root) # taking Date
    DateEntry.insert(0,"Enter date : dd/mm/yyyy")
    DateEntry.bind("<FocusIn>", date_focus_in)
    DateEntry.config(font=("arial",10,"bold"),fg='grey')
    DateEntry.place(x=160,y=90,height=25,width=200)

    EventTimeEntry=tk.Label(text="EventTime:",font=("arial",15,"bold")).place(x=30,y=120,height=20,width=130) #EventTime label creation
    EventTimeEntry=tk.Entry(root) #taking EventTime
    EventTimeEntry.insert(0,"time:hh:mm,ex:16:30 as 4:30PM")
    EventTimeEntry.bind("<FocusIn>", time_focus_in)
    EventTimeEntry.config(font=("arial",10,"bold"),fg='grey')
    EventTimeEntry.place(x=160,y=120,height=25,width=200)


    b1 = tk.Button(text ="Submit") #Creating login button
    b1.config(bg="yellow", fg="blue",font=("arial",15,"bold"))
    b1.bind("<Button-1>",events)
    b1.place(x=200,y=150,height=30,width=75)


    b2 = tk.Button(text ="View All Events")
    b2.config(bg="yellow", fg="blue",font=("arial",15,"bold"))
    b2.bind("<Button-1>",viewevents)
    b2.place(x=550,y=100,height=25,width=200)

    b5 = tk.Button(text ="select Date")
    b5.config(bg="grey", fg="black",font=("arial",10,"bold"))
    b5.bind("<Button-1>",get_date)
    b5.place(x=360,y=90,height=25,width=100)


    Output=tk.Label(text="Output:",font=("arial",15,"bold")).place(x=0,y=220,height=20,width=200) #Creating output label
    Output = tk.Label(text = "     ") #displaying the output
    Output.config(bg="white",fg="black",font=("arial",10,"bold"))
    Output.place(x=50,y=250,height=50,width=700)


    frame2 = tk.Frame(root) #Creating a Frame for root app


    b3 = tk.Button(frame2,text ="delete") #Creating login button
    b3.config(bg="yellow", fg="blue",font=("arial",15,"bold"))
    b3.bind("<Button-1>", delete_event)
    b3.place(x=300,y=350,height=30,width=75)

    b4 = tk.Button(frame2,text ="back") #Creating login button
    b4.config(bg="yellow", fg="blue",font=("arial",15,"bold"))
    b4.bind("<Button-1>", backtoapp)
    b4.place(x=680,y=350,height=30,width=75)



    tree = ttk.Treeview(frame2, column=("c1", "c2", "c3"), show='headings')

    tree.column("#1", anchor=tk.CENTER)

    tree.heading("#1", text="EVENT NAME")

    tree.column("#2", anchor=tk.CENTER)

    tree.heading("#2", text="DATE")

    tree.column("#3", anchor=tk.CENTER)

    tree.heading("#3", text="TIME")

    tree.place(x=0,y=0,height=350,width=800)

    style = ttk.Style(root)
    # set ttk theme to "clam" which support the fieldbackground option
    style.theme_use("clam")
    style.configure("Treeview", font =("arial",15,"bold") )

    frame1.place(x=0,y=0,height=800,width=1000)

    root.mainloop()
    time.sleep(s)

def toasts(s):
    while True:
        now = datetime.datetime.now()
        d2 = now.strftime("%d/%m/%Y")
        st = now.strftime("%H:%M")
        tup = (d2,st)
        k = cursor.execute('SELECT DATE,TIME FROM EVENTS').fetchall()
        if tup in k:
            q = cursor.execute("SELECT EVENT FROM EVENTS WHERE DATE = ? AND TIME = ? ", (d2,st))
            q = q.fetchone()
            q = q[0]        
            notifier = ToastNotifier()
            notifier.show_toast(title="event remainder", msg=f"{q}",duration=15)
            cursor.execute("DELETE FROM EVENTS WHERE DATE = (?) AND TIME = (?) ", (d2,st))
            db.commit()
        time.sleep(s)

p1 = multiprocessing.Process(target=first,args=[1])
p2 = multiprocessing.Process(target=toasts,args=[1])

if __name__ == '__main__':
    p1.start()
    p2.start()
    p1.join()
    p2.join()