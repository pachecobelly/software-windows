import tkinter as tk

from BaseApp import BaseApp
from elementosbotoes import ElementosApp
from keywords import KeywordsApp



class PaginaInicial(BaseApp):
    """Classe da Página Inicial"""
    def __init__(self):
        super().__init__("Home Page", "700x500")
        
        
        frame = tk.Frame(self, bg="#f8f9fa")
        frame.pack(expand=True)

        btn_keys = tk.Button(frame, text="Keywords", command=self.abrir_keys, width=10, height=2, bg="#e0e0e0")
        btn_keys.pack(pady=10)

        btn_metodos = tk.Button(frame, text="Methods", command=self.abrir_metodos, width=10, height=2, bg="#e0e0e0")
        btn_metodos.pack(pady=10)

    def abrir_keys(self):
        KeywordsApp()  # Agora chama diretamente a classe da interface de Keywords

    def abrir_metodos(self):
        ElementosApp()  # Agora chama diretamente a classe da Tabela Periódica



if __name__ == "__main__":
    app = PaginaInicial()
    #app.iconbitmap("software_assistant_icon.ico")
    app.mainloop()
