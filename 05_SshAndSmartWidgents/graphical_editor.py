import tkinter as tk
import re
import itertools as it


# language x1 y1 x2 y2 width outline_color fill_color
class Application(tk.Frame):
    def __init__(self, master=None, title="graphical_editor", **kwargs):
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.create_widgets()
        self.figures = dict()
        self.default_options = {"width": "2.0", "outline": "#0000ff", "fill": "#ffff00"}

    def create_widgets(self):
        self.L = tk.Label(self)
        self.L.grid(sticky="NEWS")
        self.L.columnconfigure(0, weight=1)
        self.L.columnconfigure(1, weight=1)
        self.L.rowconfigure(0, weight=1)
        self.T = tk.Text(self.L)
        self.T.grid(row=0, column=0, sticky="NEWS")
        self.C = tk.Canvas(self.L)
        self.C.grid(row=0, column=1, sticky="NEWS")
        self.C.bind("<ButtonPress-1>", self.move_start)
        self.C.bind("<B1-Motion>", self.move_move)
        self.BL = tk.Label(self.L)
        self.BL.grid(row=1, columnspan=2, sticky="E")
        self.Q = tk.Button(self.BL, text="Quit", command=self.master.quit)
        self.Q.grid(row=0, column=2)
        self.UT = tk.Button(self.BL, text="Update Text", command=self.update_text)
        self.UT.grid(row=0, column=1)
        self.UC = tk.Button(self.BL, text="Update Canvas", command=self.update_canvas)
        self.UC.grid(row=0, column=0)

    def try_create_figure(self, opts):
        if len(opts) != 7:
            return {}
        try:
            figure = {"coords": [float(x) for x in opts[:4]], "options": {}}
            re_color = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")
            if not re_color.match(opts[5]) or not re_color.match(opts[6]):
                return {}
            figure["options"]["width"] = opts[4]
            figure["options"]["outline"] = opts[5]
            figure["options"]["fill"] = opts[6]
            return figure
        except ValueError:
            return {}

    def parse_text(self, text):
        figures = []
        for i, line in enumerate(text.split("\n")):
            figure = self.try_create_figure(line.split(" "))
            if figure:
                figures.append(figure)
            else:
                self.T.tag_add("error", f"{i+1}.0", f"{i+1}.end")
        self.T.tag_configure("error", background="red")
        return figures

    def create_figures(self, figures):
        self.figures = {}
        for figure in figures:
            self.figures[self.C._create("oval", figure['coords'], figure['options'])] = figure

    def update_canvas(self):
        self.C.delete("all")
        self.T.tag_delete("error")
        self.create_figures(self.parse_text(self.T.get("1.0", "end-1c")))

    def move_start(self, event):
        self.cur_obj_id = self.C.find_overlapping(event.x, event.y, event.x, event.y)
        self.prev_coords = [event.x, event.y]
        self.new_figure_flag = False
        if not self.cur_obj_id:
            self.new_figure_flag = True
            self.cur_obj_id = self.C.create_oval(event.x, event.y, event.x, event.y, self.default_options)
            self.figures[self.cur_obj_id] = {"coords": [event.x, event.y, event.x, event.y],
                                             "options": self.default_options}
        else:
            self.cur_obj_id = self.cur_obj_id[-1]

    def move_move(self, event):
        if not self.new_figure_flag:
            self.C.move(self.cur_obj_id, event.x - self.prev_coords[0], event.y - self.prev_coords[1])
            self.prev_coords = [event.x, event.y]
        else:
            self.C.coords(self.cur_obj_id, self.prev_coords[0], self.prev_coords[1], event.x, event.y)

    def update_text(self):
        self.T.delete("1.0", "end")
        text = "\n".join( (" ".join(it.chain((str(c) for c in self.C.coords(obj)),
                                            self.figures[obj]["options"].values())) for obj in self.C.find_all()) )
        self.T.insert("1.0", text)


def main():
    app = Application()
    app.mainloop()


if __name__ == '__main__':
    main()
