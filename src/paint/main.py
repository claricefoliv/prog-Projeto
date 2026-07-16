import tkinter as tk

# MUDANÇA 13: imports ajustados para a estrutura de pacotes MVC
# cada camada importa do seu pacote: paint.modelo, paint.visao, paint.controlador
from modelo.figuras import Desenho
from visao.view import TelaDesenho
from controlador.controller import ControladorDesenho


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Paint")

    modelo = Desenho()
    visao = TelaDesenho(root)
    controlador = ControladorDesenho(modelo, visao)

    # MUDANÇA 14: ESSENCIAL! Liga o controlador na view
    # no código original isso não existia, então a View tinha self.controlador = None
    # e nunca chamava os métodos do controlador (menus não funcionavam, cliques não funcionavam)
    visao.set_controlador(controlador)

    root.mainloop()
