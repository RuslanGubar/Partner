import tkinter as tk
from partner_module import PartnerModule
from style_guide import BG_COLOR
from PIL import Image, ImageTk
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Партнеры системы")
        self.geometry("800x600")
        self.configure(bg=BG_COLOR)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        try:
            self.icon_image = tk.PhotoImage(file="assets/icon.png")  # Fallback to PNG
            self.iconphoto(False, self.icon_image)
        except tk.TclError as e:
            print(f"Error loading icon: {e}")

        self.partner_module = PartnerModule(self)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()