import tkinter as tk
from tkinter import messagebox
import random


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky="NEWS")
        self.createWidgets()
        
    def init_positions(self):
        self.num2pos = {num: [el // 4 + 1, el % 4] for num, el in enumerate(random.sample(range(16), 16))}

    def move(self, num):
        if abs(self.num2pos[num][0] - self.num2pos[15][0]) == 1 and self.num2pos[num][1] == self.num2pos[15][1]:
            self.num2pos[num][0], self.num2pos[15][0] = self.num2pos[15][0], self.num2pos[num][0]
        elif abs(self.num2pos[num][1] - self.num2pos[15][1]) == 1 and self.num2pos[num][0] == self.num2pos[15][0]:
            self.num2pos[num][1], self.num2pos[15][1] = self.num2pos[15][1], self.num2pos[num][1]
        self.draw()
        if self.num2pos == self.win_combination:
            messagebox.showinfo("", "You win :-)")

    def draw(self):
        self.new_button.grid(row=0, column=0, columnspan=2, sticky="NS")
        self.exit_button.grid(row=0, column=2, columnspan=2, sticky="NS")
        for i, b in enumerate(self.num_buttons):
            b.grid(row=self.num2pos[i][0], column=self.num2pos[i][1], sticky="NEWS")

    def new(self):
        self.init_positions()
        self.draw()

    def createWidgets(self):
        self.init_positions()
        self.win_combination = {num: [el // 4 + 1, el % 4] for num, el in enumerate(range(16))}
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        for i in range(4):
            self.columnconfigure(i, weight=2)
            self.rowconfigure(i + 1, weight=2)
        self.num_buttons = [tk.Button(self, text=f"{i + 1}", command=lambda num=i: self.move(num)) for i in range(15)]
        self.num_buttons.append(tk.Button(self, text="", command=lambda : None))
        self.new_button = tk.Button(self, text="New", command=self.new)
        self.exit_button = tk.Button(self, text="Exit", command=self.quit)
        self.draw()


def main():
    app = Application()
    app.master.title("15")
    app.mainloop()


if __name__ == "__main__":
  main()
