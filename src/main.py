#import all required dependencies
import tkinter as tk
import customtkinter as ctk
from pymongo import MongoClient
import pyglet

#set up connections with the database
cluster = MongoClient("mongodb+srv://fireplatypus375:0TgN3YyiObPpHtmQ@fblamain.emmytgc.mongodb.net/")
db = cluster["FBLAMain"]
loginInfo = db["login_info"]

#import custom font
pyglet.font.add_file('assets/Quicksand-Bold.ttf')

#creates main home gui
root= ctk.CTk()
root.geometry("1000x500+100+100")


loginLabel = ctk.CTkLabel(root, text="login", font=("Quicksand",50))
loginLabel.place(relx=0.5, rely=0.2, anchor="center")

def done():
    loginInfo.insert_one()
randomButton = ctk.Ctkbutton(root, text="click me", command= done, )
randomButton.place(relx= 0.5, rely= 0.4)


#keeps application running 
if __name__ == "__main__":
    root.mainloop()



