import tkinter as tk

# Variáveis globais
ferramenta = "oval" 
figura_atual = None  


def oval():
    global ferramenta
    ferramenta = "oval"

def retangulo():
    global ferramenta
    ferramenta = "retangulo"
    
def marca_inicio(event):
    global ini_x, ini_y, figura_atual
    ini_x = event.x
    ini_y = event.y
    
    if ferramenta == "oval":
        figura_atual = canvas.create_oval(
            ini_x, ini_y, ini_x, ini_y, outline="black"
        )
    elif ferramenta == "retangulo":
        figura_atual = canvas.create_rectangle(
            ini_x, ini_y, ini_x, ini_y, outline="black"
        )

def atualiza_fim(event):
    global ini_x, ini_y, figura_atual
    # Em vez de canvas.delete("all"), atualizamos apenas as coordenadas da figura atual
    if figura_atual:
        canvas.coords(figura_atual, ini_x, ini_y, event.x, event.y)


root = tk.Tk()
root.title("Projeto de Programação A - Desenho")


bot_oval = tk.Button(root, text="OVAL", command=oval)
bot_oval.pack()

bot_retangulo = tk.Button(root, text="RETÂNGULO", command=retangulo)
bot_retangulo.pack()

canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

ini_x = None
ini_y = None

canvas.bind('<ButtonPress-1>', marca_inicio)
canvas.bind('<B1-Motion>', atualiza_fim)

root.mainloop()