from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
from tkinter import ttk
import pymysql

def login():
    if userentry.get()=='' or passentry.get()=='':
        messagebox.showerror('Error','Field cannot be empty')
    elif userentry.get()=='Ramya' and passentry.get()=='1234':
        messagebox.showinfo('success','Welcome')
        window.destroy()
        import sms

    else:
        messagebox.showerror('Error','Please enter correct credentials')




# creating object for Tk class
window=Tk()

#geometry method from class Tk, used to modify size of the screen
window.geometry('1200x700+0+0')
window.title('Login System of Students Management System')

#resizable method from Tk class, disabling maximize symbol
window.resizable(False,False)

#importing image in code by using imageTk class, bgimage=obj, photoimage class
bgimage=ImageTk.PhotoImage(file='bgimg.jpg')
bglabel=Label(window,image=bgimage)
bglabel.place(x=0,y=0)

#creating frame class, it keeps labels buttons inside it, passing (window) , and loginFrame=obj
loginframe=Frame(window,bg='black')
loginframe.place(x=450,y=225)

logoimage=PhotoImage(file='logo.png',)
logolabel=Label(loginframe,image=logoimage)
logolabel.grid(row=0,column=0,columnspan=2,pady=10)

username=PhotoImage(file='user.png')
userlabel=Label(loginframe,image=username,text='username',compound=LEFT,font=('Times new roman',10),fg='white',bg='black')
userlabel.grid(row=1,column=0,padx=20)

userentry=Entry(loginframe,font=('Times new roman',10),bd=5,fg='medium blue')
userentry.grid(row=1,column=1,pady=10,padx=10)

password=PhotoImage(file='lock.png')
passlabel=Label(loginframe,image=password,text='password',compound=LEFT,font=('Times new roman',10),fg='white',bg='black')
passlabel.grid(row=2,column=0,padx=20)

passentry=Entry(loginframe,font=('Times new roman',10),bd=5,fg='medium blue')
passentry.grid(row=2,column=1,pady=10,padx=10)

button=Button(loginframe,text='Login',font=('Times new roman',10),bg='cornflowerblue',
              activebackground='cornflowerblue',cursor='hand2',command=login) #login func called here
button.grid(row=3,column=1,pady=10)

#mainloop another method of class Tk, will show the screen continously
window.mainloop()