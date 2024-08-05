from typing import Tuple
import customtkinter as ctk

class Screen_Record(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Edição de Fichas')
        self.geometry('400x610')
        self.screen()

    def screen(self):
        pass

if __name__ == '__main__':
    sys = Screen_Record()
    sys.mainloop()