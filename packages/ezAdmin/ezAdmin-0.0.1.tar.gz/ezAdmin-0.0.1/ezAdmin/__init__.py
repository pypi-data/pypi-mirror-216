import pyuac
from tkinter import messagebox

class Admin():
    def __init__(self):
        self.self = self
    class Catch():
        def __init__(self):
            self.self = self
        def ShowAdminCatch(self, msg, title, type):
            if type == 'ERROR':
                messagebox.showerror(title=title, message=msg)
            elif type == 'WARN':
                messagebox.showwarning(title=title,message=msg)
            elif type == 'INFO':
                messagebox.showinfo(title=title,message=msg)
            elif type not in ['ERROR','WARN','INFO']:
                raise ValueError(f'Invalid option type {type}')

a = Admin()
show = a.Catch()
show.ShowAdminCatch('hi', 'hi', type='ERROR')
