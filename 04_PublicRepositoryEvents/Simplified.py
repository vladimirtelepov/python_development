import tkinter as tk
import re


def add_member(parent, name):
    def upgrade_widget(children, geometry, **kwargs):
        search_re = r"(?P<row>\d+)(?:(\.(?P<row_weight>\d+))?)(?:(\+(?P<height>\d+))?)" \
                    r":(?P<column>\d+)(?:(\.(?P<column_weight>\d+))?)(?:(\+(?P<width>\d+))?)(?:(\/(?P<gravity>\w+))?)"
        params = re.search(search_re, geometry).groupdict()
        assert params is not None, "wrong widget geometry syntax"
        params = {k: int(v) if k != "gravity" else v for k, v in params.items() if v is not None}
        default_params = {"row": 0, "column": 0, "row_weight": 1, "column_weight": 1,
                          "height": 0, "width": 0, "gravity": "NEWS"}
        default_params.update(params)
        params = default_params
        children = type(children.__name__ + "_upgraded", tuple([children]), {"__getattr__": add_member})
        setattr(parent, name, children(parent, **kwargs))
        getattr(parent, name).master.rowconfigure(params["row"], weight=params["row_weight"])
        getattr(parent, name).master.columnconfigure(params["column"], weight=params["column_weight"])
        getattr(parent, name).grid(row=params["row"], column=params["column"],
                                   rowspan=params["height"] + 1, columnspan=params["width"] + 1,
                                   sticky=params["gravity"])
    return upgrade_widget


class Application(tk.Frame):
    def __init__(self, master=None, title=""):
        super().__init__(master)
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        if master is None:
            self.master.title(title)
        Application.__getattr__ = add_member
        self.createWidgets()


class App(Application):
    def createWidgets(self):
        self.message = "Congratulations!\nYou've found a sercet level!"
        self.F1(tk.LabelFrame, "1:0", text="Frame 1")
        self.F1.B1(tk.Button, "0:0/NW", text="1")
        self.F1.B2(tk.Button, "0:1/NE", text="2")
        self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
        self.F2(tk.LabelFrame, "1:1", text="Frame 2")
        self.F2.B1(tk.Button, "0:0/N", text="4")
        self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
        self.F2.B3(tk.Button, "1:0/S", text="6")
        self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
        self.F1.B3.bind("<Any-Key>", lambda event: showinfo(self.message.split()[0], self.message))


def main():
    app = App(title="Sample application")
    app.mainloop()
    

if __name__ == "__main__":
    main()
