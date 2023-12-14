from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox,filedialog
import pymysql
import pandas


def exit_page():
    result=messagebox.askyesno('Confirm','Do you want to Exit')
    if result:
        root.destroy()
    else:
        pass
def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=studenttable.get_children()
    newlist=[]
    for index in indexing:
        content=studenttable.item(index)
        datalist=content['values']
        newlist.append(datalist)

    table=pandas.DataFrame(newlist,columns=['Id','Name','Mobile','Email','Address','Gender','DOB','Added Date','Added Time'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved successfully')

def Top_level(title,button_text,command):

    global identry,nameentry,mobileentry,emailentry,addressentry,genderentry,dobentry,screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)
    idlabel = Label(screen, text='ID', font=('arial', 15, 'bold'))
    idlabel.grid(row=0, column=0, padx=20, pady=10)
    identry = Entry(screen, font=('arial', 15), width=20)
    identry.grid(row=0, column=1, padx=20, pady=10)

    namelabel = Label(screen, text='Name', font=('arial', 15, 'bold'))
    namelabel.grid(row=1, column=0, padx=20, pady=10)
    nameentry = Entry(screen, font=('arial', 15), width=20)
    nameentry.grid(row=1, column=1, padx=20, pady=10)

    mobilelabel = Label(screen, text='Mobile No', font=('arial', 15, 'bold'))
    mobilelabel.grid(row=2, column=0, padx=20, pady=10)
    mobileentry = Entry(screen, font=('arial', 15), width=20)
    mobileentry.grid(row=2, column=1, padx=20, pady=10)

    emaillabel = Label(screen, text='Email', font=('arial', 15, 'bold'))
    emaillabel.grid(row=3, column=0, padx=20, pady=10)
    emailentry = Entry(screen, font=('arial', 15), width=20)
    emailentry.grid(row=3, column=1, padx=20, pady=10)

    addresslabel = Label(screen, text='Address', font=('arial', 15, 'bold'))
    addresslabel.grid(row=4, column=0, padx=20, pady=10)
    addressentry = Entry(screen, font=('arial', 15), width=20)
    addressentry.grid(row=4, column=1, padx=20, pady=10)

    genderlabel = Label(screen, text='Gender', font=('arial', 15, 'bold'))
    genderlabel.grid(row=5, column=0, padx=20, pady=10)
    genderentry = Entry(screen, font=('arial', 15), width=20)
    genderentry.grid(row=5, column=1, padx=20, pady=10)

    doblabel = Label(screen, text='D.O.B.', font=('arial', 15, 'bold'))
    doblabel.grid(row=6, column=0, padx=20, pady=10)
    dobentry = Entry(screen, font=('arial', 15), width=20)
    dobentry.grid(row=6, column=1, padx=20, pady=10)

    studentbutton = ttk.Button(screen, text=button_text , width=10, command=command)
    studentbutton.grid(row=7, columnspan=2, pady=15)

    if title=='Update Student':
        indexing = studenttable.focus()
        print(indexing)
        content = studenttable.item(indexing)
        listdata = content['values']
        print(listdata)
        identry.insert(0, listdata[0])
        nameentry.insert(0, listdata[1])
        mobileentry.insert(0, listdata[2])
        emailentry.insert(0, listdata[3])
        addressentry.insert(0, listdata[4])
        genderentry.insert(0, listdata[5])
        dobentry.insert(0, listdata[6])

def update_data():
    global date, currenttime
    query='update students set name=%s,mobile=%s,email=%s,address=%s,gender=%s,dob=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query,(nameentry.get(),mobileentry.get(),emailentry.get(),addressentry.get(),genderentry.get(),dobentry.get(),date,currenttime,identry.get()))
    con.commit()
    messagebox.showinfo('Success', f'ID {identry.get()} is modified successfully',parent=screen)
    screen.destroy()
    showstudent()





def showstudent():
    query='select * from students'
    mycursor.execute(query)
    fetchdata = mycursor.fetchall()
    studenttable.delete(*studenttable.get_children())

    for data in fetchdata:
        studenttable.insert('', END, values=data)


def deletestudent():
    indexing=studenttable.focus()
    print(indexing)
    content=studenttable.item(indexing)
    content_id=content['values'][0]
    query='delete from students where id=%s'
    mycursor.execute(query, content_id)
    con.commit()
    messagebox.showinfo('Deleted',f'ID {content_id} is deleted successfully')
    query='select * from students'
    mycursor.execute(query)
    fetchdata = mycursor.fetchall()
    studenttable.delete(*studenttable.get_children())

    for data in fetchdata:
        studenttable.insert('', END, values=data)


def search_data():

    query = 'select * from students where id=%s or name=%s or email=%s or mobile=%s or address=%s or gender=%s or dob=%s'

    mycursor.execute(query,(identry.get(),nameentry.get(),emailentry.get(),mobileentry.get(),addressentry.get(),genderentry.get(),dobentry.get()))
    fetchdata = mycursor.fetchall()
    studenttable.delete(*studenttable.get_children())

    for data in fetchdata:
        studenttable.insert('', END, values=data)




def add_data():
    if identry.get()=='' or nameentry.get()=='' or mobileentry.get()=='' or emailentry.get()=='' or addressentry.get()=='' or genderentry.get()=='' or dobentry.get()=='' :
        messagebox.showerror('Error','All Fields are required',parent=screen)

    else:

        try:
            check_query = 'select * from students where Id=%s'
            mycursor.execute(check_query, (identry.get(),))
            existing_data = mycursor.fetchone()

            if existing_data:
                messagebox.showerror('Error', 'ID Already Exists. Please choose a unique ID.', parent=screen)
            else:
                query='insert into students value(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                mycursor.execute(query,(identry.get(),nameentry.get(),mobileentry.get(),emailentry.get(),addressentry.get(),
                                    genderentry.get(),dobentry.get(),date,currenttime))

                con.commit()
                result=messagebox.askyesno('Confirmation','Data added Successfully, Do you want clear the form?',parent=screen)
                if result:
                    identry.delete(0,END)
                    nameentry.delete(0, END)
                    mobileentry.delete(0, END)
                    emailentry.delete(0, END)
                    addressentry.delete(0, END)
                    genderentry.delete(0, END)
                    dobentry.delete(0, END)
                else:
                    pass
        except :
            messagebox.showerror('Error','ID Cannot be Duplicate',parent=screen)
            return



        query='select * from students'
        mycursor.execute(query)
        fetchdata=mycursor.fetchall()
        studenttable.delete(*studenttable.get_children() )

        for i in fetchdata:

            studenttable.insert('',END,values=i)

def connect_database():
    def connect():
        global mycursor,con
        try:
            con=pymysql.connect(host='localhost',user='root',password='1234')
            mycursor=con.cursor()

        except:
            messagebox.showerror('Error','Invalid Details',parent=connectwindow)
            return

        try:
            query='create database sdbms'
            mycursor.execute(query)
            query='use sdbms'
            mycursor.execute(query)
            query = ('create table students(Id int not null primary key, name varchar(50), mobile varchar(15), email varchar(50), '
                'address varchar(100), gender varchar(10), dob varchar(10), date varchar(10), time varchar(10))')

            mycursor.execute(query)

        except:
            query = 'use sdbms'
            mycursor.execute(query)
            messagebox.showinfo('Success','Database Connection is Successful',parent=connectwindow)
            connectwindow.destroy()

        addbutton.config(state=NORMAL)
        searchbutton.config(state=NORMAL)
        deletebutton.config(state=NORMAL)
        searchbutton.config(state=NORMAL)
        updatebutton.config(state=NORMAL)
        showbutton.config(state=NORMAL)
        exportbutton.config(state=NORMAL)



    connectwindow=Toplevel()
    connectwindow.grab_set()
    connectwindow.geometry('400x220+500+200')
    connectwindow.title('Database Connection')
    connectwindow.resizable(0,0)

    hostnamelabel=Label(connectwindow,text='HOST NAME:',font=('arial', 15, 'bold'))
    hostnamelabel.grid(row=0,column=0,padx=20)
    hostnameentry = Entry(connectwindow, font=('roman', 10),width=30)
    hostnameentry.grid(row=0, column=1, pady=20,padx=10)

    usernamelabel = Label(connectwindow, text='USER NAME:', font=('arial', 15, 'bold'))
    usernamelabel.grid(row=1, column=0, padx=20)
    usernameentry = Entry(connectwindow, font=('roman', 10), width=30)
    usernameentry.grid(row=1, column=1 ,pady=20,padx=10)

    passwordlabel = Label(connectwindow, text='PASSWORD:', font=('arial', 15, 'bold'))
    passwordlabel.grid(row=2, column=0, padx=20)
    passwordentry = Entry(connectwindow, font=('roman', 10), width=30)
    passwordentry.grid(row=2, column=1, pady=20, padx=10)


    connectbutton=ttk.Button(connectwindow, text='    Connect',width=15, command=connect)
    connectbutton.place(x=165,y=175)




def clock():
    global date,currenttime
    date = time.strftime('%d/%m/%Y')  # strftime is function to give format for date and time
    currenttime = time.strftime('%H:%M:%S')
    datetimelabel.config(text=f' Date:{date}\nTime:{currenttime}')
    datetimelabel.after(1000, clock)


count = 0
text = ''
def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderlabel.config(text=text)
    count += 1
    sliderlabel.after(100, slider)


# GUI Part
root = ttkthemes.ThemedTk()

root.get_themes()
root.set_theme('aquativo')

root.geometry('1400x700+0+0')
root.resizable(0,0)
root.title('Student Management System')

datetimelabel = Label(root, font=('date stamp', 10))
datetimelabel.place(x=5, y=5)
clock()

s = 'Students Management System'
sliderlabel = Label(root, font=('arial', 20, 'bold'), width=30)
sliderlabel.place(x=450, y=0)
slider()

connectbutton = ttk.Button(root, text='Connect to Database',command=connect_database)
connectbutton.place(x=1200, y=0)

leftframe = Frame(root)
leftframe.place(x=70, y=50, width=200, height=600)

logosymbol = PhotoImage(file='logo_1.png')
logolabel = Label(leftframe, image=logosymbol)
logolabel.grid(row=0, column=0)

addbutton = ttk.Button(leftframe, text='           Add Student', width=25,state=DISABLED, command=lambda :Top_level('Add Student','  Add',add_data))
addbutton.grid(row=1, column=0, pady=20)

searchbutton = ttk.Button(leftframe, text='          Search Student', width=25,state=DISABLED,command=lambda :Top_level('Search Student','  Search',search_data))
searchbutton.grid(row=2, column=0, pady=20)

deletebutton = ttk.Button(leftframe, text='          Delete Student', width=25,state=DISABLED,command=deletestudent)
deletebutton.grid(row=3, column=0, pady=20)

updatebutton = ttk.Button(leftframe, text='          Update Student', width=25,state=DISABLED,command=lambda :Top_level('Update Student','  Update',update_data))
updatebutton.grid(row=4, column=0, pady=20)

showbutton = ttk.Button(leftframe, text='          Show Student', width=25,state=DISABLED,command=showstudent)
showbutton.grid(row=5, column=0, pady=20)

exportbutton = ttk.Button(leftframe, text='          Export Data', width=25,state=DISABLED,command=export_data)
exportbutton.grid(row=6, column=0, pady=20)

exitbutton = ttk.Button(leftframe, text='                Exit', width=25,command=exit_page)
exitbutton.grid(row=7, column=0, pady=20)

rightframe = Frame(root)
rightframe.place(x=350, y=80, width=1000, height=600)

scrollbarX = Scrollbar(rightframe, orient=HORIZONTAL)
scrollbarX.pack(side=BOTTOM, fill=X)

scrollbarY = Scrollbar(rightframe, orient=VERTICAL)
scrollbarY.pack(side=RIGHT, fill=Y)

studenttable = ttk.Treeview(rightframe,column=('Id', 'Name', 'Mobile No', 'Email', 'Address', 'Gender', 'D.O.B.', 'Added Date', 'Added Time'),
                            xscrollcommand=scrollbarX.set,yscrollcommand=scrollbarY.set)
studenttable.pack(fill=BOTH, expand=1)


scrollbarX.config(command=studenttable.xview)
scrollbarY.config(command=studenttable.yview)


studenttable.heading('Id',text='Id')
studenttable.heading('Name',text='Name')
studenttable.heading('Mobile No',text='Mobile No')
studenttable.heading('Email',text='Email')
studenttable.heading('Address',text='Address')
studenttable.heading('Gender',text='Gender')
studenttable.heading('D.O.B.',text='D.O.B.')
studenttable.heading('Added Date',text='Added Date')
studenttable.heading('Added Time',text='Added Time')

studenttable.column('Id',width=50,anchor=CENTER)
studenttable.column('Name',width=200,anchor=CENTER )
studenttable.column('Mobile No',width=200,anchor=CENTER )
studenttable.column('Email',width=200,anchor=CENTER )
studenttable.column('Address',width=200,anchor=CENTER )
studenttable.column('Gender',width=200,anchor=CENTER )
studenttable.column('D.O.B.',width=200,anchor=CENTER )
studenttable.column('Added Date',width=200,anchor=CENTER )
studenttable.column('Added Time',width=200,anchor=CENTER )

style=ttk.Style()

style.configure('Treeview',rowheight=30,font=('arial',10), foreground='red4', background='peach puff',fieldbackground='bisque')
style.configure('Treeview.heading',rowheight=30,font=('arial',20,'bold'))

studenttable.config(show='headings')

root.mainloop()
