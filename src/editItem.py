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

#=========================== establish connection to database ======================================================================================================================================================
cluster = MongoClient("mongodb+srv://fireplatypus375:0TgN3YyiObPpHtmQ@fblamain.emmytgc.mongodb.net/")
db = cluster["main"]
loginInfo = db["loginInfo"]
orgInfo = db["orgInfo"]

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

check = 0


#=========================== function to create edit item frame ======================================================================================================================================================
def editItem(root, listbox,):
#=========================== edit organization frame ======================================================================================================================================================
    global check
    print(check)
    if check == 0:
        temp = listbox.selection()
        if len(temp) == 0:
            error("Please select an organization to edit", root)
        elif len(temp) > 1:
            error("You can only select one organization to edit at a time", root)
        else:
            check = 1
            selection = listbox.item(temp, option="values")

            editItemFrame = ctk.CTkFrame(root, width= 500, height= 600, fg_color= color, border_color= "#1e2121", border_width=4)
            editItemFrame.place(relx= 1, rely= 0, anchor= "ne")
            editItemFrame.focus_set()

            def back():
                global check
                editItemFrame.place_forget()
                check = 0

            backButton = ctk.CTkButton(editItemFrame, text="x", font=font(20), command= back, fg_color=color, hover_color=color, width=0, height=0)
            backButton.place(relx=.04, rely=0.02, anchor="nw")
            backButton.bind("<Enter>", on_enter)
            backButton.bind("<Leave>", on_leave)

            labelText = ctk.CTkLabel(editItemFrame, text="Edit Organization", font=font(20))
            labelText.place(relx=0.5, rely=0.05, anchor="center")

            orgNameText = ctk.CTkLabel(editItemFrame, text="Organization Name", font=font(15))
            orgNameText.place(relx=0.12, rely=0.15, anchor="w")

            orgNameEntry = ctk.CTkEntry(editItemFrame, font = font(15), width = 400, height= 40, justify = "center")
            orgNameEntry.place(relx= 0.5, rely= 0.2, anchor= "center")
            orgNameEntry.insert(0, selection[0])
            orgNameEntry.bind('<FocusIn>', lambda x: orgNameEntry.select_range(0, "end"))

            resourcesText = ctk.CTkLabel(editItemFrame, text="Resources", font=font(15))
            resourcesText.place(relx=0.12, rely=0.35, anchor="w")

            resourcesEntry = ctk.CTkEntry(editItemFrame, font = font(15), width = 400, height= 40, justify = "center")
            resourcesEntry.place(relx= 0.5, rely= 0.4, anchor= "center")
            resourcesEntry.insert(0, selection[1])
            resourcesEntry.bind('<FocusIn>', lambda x: resourcesEntry.select_range(0, "end"))

            locationText = ctk.CTkLabel(editItemFrame, text="Location", font=font(15))
            locationText.place(relx=0.12, rely=0.55, anchor="w")

            locationEntry = ctk.CTkEntry(editItemFrame, font = font(15), width = 400, height= 40, justify = "center")
            locationEntry.place(relx= 0.5, rely= 0.6, anchor= "center")
            locationEntry.insert(0, selection[2])
            locationEntry.bind('<FocusIn>', lambda x: locationEntry.select_range(0, "end"))

            contactInfoText = ctk.CTkLabel(editItemFrame, text="Contact info", font=font(15))
            contactInfoText.place(relx=0.12, rely=0.75, anchor="w")

            contactInfoEntry = ctk.CTkEntry(editItemFrame, font = font(15), width = 400, height= 40, justify = "center")
            contactInfoEntry.place(relx= 0.5, rely= 0.8, anchor= "center")
            contactInfoEntry.insert(0, selection[3])
            contactInfoEntry.bind('<FocusIn>', lambda x: contactInfoEntry.select_range(0, "end"))

            def submit():
                global check
                orgs = orgInfo.find()
                if  orgNameEntry.get() == "" or locationEntry.get() == "" or resourcesEntry.get() == "" or contactInfoEntry.get() == "":
                    error("One or more fields are empty, please use N/A in replacement of an empty entry", root)
                else:
                    orgInfo.replace_one({"orgName": selection[0]}, {"orgName": orgNameEntry.get(), "resources": resourcesEntry.get(), "location": locationEntry.get(), "contactInfo": contactInfoEntry.get()})
                    editItemFrame.place_forget()
                    count = 0
                for item in listbox.get_children():
                    listbox.delete(item)
                for item in orgs:
                    listbox.insert(parent='', index='end', text= "", iid= count, values= (item["orgName"], item["location"], item["resources"], item["contactInfo"]) )
                    count+= 1
                check = 0


            submitButton = ctk.CTkButton(editItemFrame, text="Submit", font=font(18), command = submit, fg_color=color, hover_color=color)
            submitButton.place(relx=0.5, rely=0.9, anchor="center")
            submitButton.bind("<Enter>", on_enter)
            submitButton.bind("<Leave>", on_leave)
    else:
        error("please close the existing 'edit organization' page first", root)