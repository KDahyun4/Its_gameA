import tkinter as tk
window = tk.Tk()
window.title("game_test")
#배경 뽑기판
back_img = tk.PhotoImage(file="lotto_background_1.png")
back_label = tk.Label(window, image=back_img)
back_label.pack()

window.mainloop()