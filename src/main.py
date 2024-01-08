#=========================== import all required packages ======================================================================================================================================================
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from pymongo import MongoClient
import ctypes
import sys
from pathlib import Path


#=========================== import all required functions ======================================================================================================================================================

from errorPage import error
from signUp import signUp
from pickingOrganization import pickingOrg

#=========================== establish connection to database ======================================================================================================================================================
cluster = MongoClient("mongodb+srv://fireplatypus375:0TgN3YyiObPpHtmQ@fblamain.emmytgc.mongodb.net/")
db = cluster["main"]
loginInfo = db["loginInfo"]

#=========================== import custom font ======================================================================================================================================================
def fetch_resource(rsrc_path):
    """Loads resources from the temp dir used by pyinstaller executables"""
    try:
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        return rsrc_path  # not running as exe, just return the unaltered path
    else:
        return base_path.joinpath(rsrc_path)


def load_font(font_path, private=True, enumerable=False):
    """Add the font at 'font_path' as a Windows font resource"""
    FR_PRIVATE = 0x10
    FR_NOT_ENUM = 0x20
    flags = (FR_PRIVATE * int(private)) | (FR_NOT_ENUM * int(1 - enumerable))
    font_fetch = str(fetch_resource(font_path))
    path_buf = ctypes.create_unicode_buffer(font_fetch)
    add_font = ctypes.windll.gdi32.AddFontResource.ExW
    font_added = add_font(ctypes.byref(path_buf), flags, 0)
    return bool(font_added)  # True if the font was added successfully

font = "Quicksand"

#=========================== fucntion to simplify font size ======================================================================================================================================================
def font(size):
    return ("Quicksand",size)

#=========================== set default colors ======================================================================================================================================================
color = "#121414"
accent = "#3cb371"

#=========================== cunction for button highliting ======================================================================================================================================================
def on_enter(e):
    e.widget['foreground'] = accent

def on_leave(e):
    e.widget['foreground'] = 'white'


#=========================== creates main frame ======================================================================================================================================================
mainFrame = ctk.CTk(fg_color = color) 
mainFrame.geometry("1200x600+180+120")


#========================================================================================================================================================================================================================================================================
#========================================================================================================================================================================================================================================================================
#=========================== ALL OF THE LOGIN PAGE STUFF ======================================================================================================================================================
#========================================================================================================================================================================================================================================================================
#========================================================================================================================================================================================================================================================================
#========================================================================================================================================================================================================================================================================


#=========================== Creating a blank page or "frame" on top of the main one to work on for the login page ======================================================================================================================================================

loginFrame = ctk.CTkFrame(mainFrame, width = 1200, height = 600, fg_color = color)
loginFrame.place(relx = 0, rely = 0)

#=========================== Creating title text that says "Login to CTE PartnerPro" ======================================================================================================================================================

loginLabel = ctk.CTkLabel(loginFrame, text="Log in to CTE PartnerPro", font=font(50))
loginLabel.place(relx=0.5, rely=0.2, anchor="center")

#=========================== Creating a email entry box and the text above it ======================================================================================================================================================

#Text box
emailEntry = ctk.CTkEntry(loginFrame, font= font(15), placeholder_text= "Name@domain.com", width= 400, height= 40, justify= "center")
emailEntry.place(relx= 0.5, rely= 0.45, anchor= "center")

#Text above text box
emailLabel = ctk.CTkLabel(loginFrame, text="Email", font=font(15))
emailLabel.place(relx=0.335, rely=0.36, anchor="nw")

#=========================== Creating a password entry box and the text above it ======================================================================================================================================================

#Text box
passwordEntry = ctk.CTkEntry(loginFrame, font= font(15), placeholder_text= "Password", width= 400, height= 40, justify= "center", show= "*")
passwordEntry.place(relx= 0.5, rely= 0.6, anchor= "center")

#Text above text box
passwordLabel = ctk.CTkLabel(loginFrame, text="Password", font=font(15))
passwordLabel.place(relx=0.335, rely=0.51, anchor="nw")

#============ Making sure that the email and the password is valid in our database =============================================================================================================================

def login():
    count = 0
    temp = loginInfo.find()
    for item in temp:
        if str(item['email']) == str(emailEntry.get()) and str(item['password']) == str(passwordEntry.get()):
            count +=1  
            
    if count == 1:
        pickingOrg(loginFrame, emailEntry.get())
        emailEntry.delete(0,"end")
        passwordEntry.delete(0,"end")
        
    else:
        error("Wrong email or password!", loginFrame)
        emailEntry.delete(0,"end")
        passwordEntry.delete(0,"end")




    

#=========================== Login Button ======================================================================================================================================================
        

loginButton = ctk.CTkButton(loginFrame, text="Log in to PartnerPro", font=font(25), command= lambda:(login()), fg_color=accent, hover_color="#63C28D", text_color= color)
loginButton.place(relx=0.5, rely=0.825, anchor="center")



''' - WORK IN PROGRESS
#=========================== Light and Dark Mode Button ======================================================================================================================================================
switch_var = ctk.StringVar(value="on")
def backgroundColor(root):

    if switch_var.get() == "on": #root.cget('fg_color') == "#121414":
        color = "white"     
        print(1)   
    elif switch_var.get() == "off":  #root.cget('fg_color') == "white":
        color = "#121414"
        print(0)
    
    root.configure(fg_color = color)     
        

lightAndDarkSwitch = ctk.CTkSwitch(loginFrame, command = lambda:(backgroundColor(loginFrame)), onvalue= "on", offvalue= "off", variable= switch_var, text = "hola")
lightAndDarkSwitch.place(relx = 0.5, rely = 0.5)
'''
#=========================== Sign up Button ======================================================================================================================================================

signupButton = ctk.CTkButton(loginFrame, text="Sign up for PartnerPro", font=font(18), command = lambda:(signUp(loginFrame)), fg_color=color, hover_color=color)
signupButton.place(relx=0.5, rely=0.92, anchor="center")
signupButton.bind("<Enter>", on_enter)
signupButton.bind("<Leave>", on_leave)


#=========================== Password Checkbox ======================================================================================================================================================
    
def showPasswordCommand():
    if passwordEntry.cget('show') == '':
        passwordEntry.configure(show='*')
    else:
        passwordEntry.configure(show='')

showPasswordCheckbox = ctk.CTkCheckBox(loginFrame, text="Show Password", command = showPasswordCommand, hover_color=accent, checkmark_color=accent, font= font(12))
showPasswordCheckbox.place(relx = 0.335, rely = 0.65)

#=========================== Keeps GUI Running ======================================================================================================================================================
if __name__ == "__main__":
    mainFrame.mainloop()