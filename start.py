from tkinter import *


class GameButton(Button):
    def __init__(self, *args, x=0, y=0, **kwargs):
        self.text = StringVar()
        Button.__init__(self, textvariable=self.text, *args, **kwargs)
        self.activated = False
        self.permitted = False
        self.value = 0

        self.x = x
        self.y = y

    def set_val(self, val):
        self.value = val
        if val == 0:
            self.text.set(f'     ')
        else:
            self.text.set(f'  {val}  ')

    def reset(self):
        self.activated = False
        self.permitted = False
        self.set_val(0)


class App:
    default_color = 'lightgreen'
    current_active_color = '#ff99bb'
    previuos_active_color = '#ffccbb'
    highlighted_color = '#00ccbb'

    def __init__(self, master):
        self.master = master
        self.counter = 0
        self.number_of_returns = 1
        self.grid_size = 10
        self.mtr = [[GameButton() for y in range(self.grid_size)] for x in range(self.grid_size)]
        self.current_button = GameButton()
        self.previous_button = GameButton()
        self.highlighted = []

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.mtr[i][j] = GameButton(self.master, x=i, y=j, bg=self.default_color, height=2, width=5)
                self.mtr[i][j].set_val(0)
                self.mtr[i][j].bind('<Button-1>', lambda event, i=i, j=j: self.increment(i, j))
                self.mtr[i][j].bind('<Button-3>', lambda event, i=i, j=j: self.decrement(i, j))
                self.mtr[i][j].grid(row=i, column=j)

    def increment(self, i, j):
        if (not self.mtr[i][j].activated and self.mtr[i][j].permitted) or self.counter == 0:
            self.counter += 1
            self.mtr[i][j].configure(bg=self.current_active_color)
            self.mtr[i][j].set_val(self.counter)
            self.mtr[i][j].activated = True
            if self.counter > 1:
                self.current_button.configure(bg=self.previuos_active_color)
                self.previous_button = self.current_button
                self.number_of_returns = 1
            self.current_button = self.mtr[i][j]
            self.highlight_possibilities(i, j)

    def decrement(self, i, j):
        if self.mtr[i][j].activated and self.mtr[i][j].value == self.counter and self.number_of_returns > 0:
            self.counter -= 1
            if self.counter == 0:
                self.reset_game()
            else:
                self.mtr[i][j].configure(bg=self.current_active_color)
                self.mtr[i][j].set_val(0)
                self.mtr[i][j].activated = False
                self.previous_button.configure(bg=self.current_active_color)
                self.current_button = self.previous_button
                self.number_of_returns = 0
                self.highlight_possibilities(self.current_button.x, self.current_button.y)

    def highlight(self, x, y, dx, dy):
        try:
            if not self.mtr[x+dx][y+dy].activated and x+dx >= 0 and y+dy >= 0:
                self.mtr[x+dx][y+dy].configure(bg=self.highlighted_color)
                self.mtr[x+dx][y+dy].permitted = True
                self.highlighted.append(self.mtr[x+dx][y+dy])
        except IndexError:
            pass

    def highlight_possibilities(self, x, y):
        for it in self.highlighted:
            if not it.activated:
                it.configure(bg=self.default_color)
                it.permitted = False
        self.highlighted = []
        possible_values = [
            (1, -2),
            (2, -1),
            (2, 1),
            (1, 2),
            (-1, 2),
            (-2, 1),
            (-2, -1),
            (-1, -2)
        ]

        for vals in possible_values:
            self.highlight(x, y, *vals)

    def reset_game(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.mtr[i][j].reset()
                self.mtr[i][j].configure(bg=self.default_color)
        self.current_button = GameButton()
        self.previous_button = GameButton()
        self.counter = 0
        self.number_of_returns = 1


if __name__ == '__main__':
    root = Tk()
    root.title("Knight's tour")
    app = App(root)
    root.bind('<space>', lambda e: app.reset_game())
    root.bind('<Escape>', lambda e: root.destroy())
    root.mainloop()
