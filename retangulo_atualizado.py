import tkinter as tk

ferramenta = "linha"
figura_atual = None

def selecionar_linha():
    global ferramenta
    ferramenta = "linha"

def selecionar_retangulo():
    global ferramenta
    ferramenta = "retangulo"

def marca_inicio(event):
    global ini_x, ini_y, figura_atual
    ini_x = event.x
    ini_y = event.y
    
    if ferramenta == "linha":
        figura_atual = canvas.create_line(ini_x, ini_y, ini_x, ini_y)
    elif ferramenta == "retangulo":
        figura_atual = canvas.create_rectangle(ini_x, ini_y, ini_x, ini_y)

def atualiza_fim(event):
    global ini_x, ini_y, figura_atual
    if figura_atual:
        canvas.coords(figura_atual, ini_x, ini_y, event.x, event.y)


root = tk.Tk()

bot_linha = tk.Button(root, text="Linha", command=selecionar_linha)
bot_linha.pack()

bot_retangulo = tk.Button(root, text="Retangulo", command=selecionar_retangulo)
bot_retangulo.pack()

canvas = tk.Canvas(root, bg='white', width=600, height=600)
canvas.pack()

ini_x = None  
ini_y = None
fim_x = None
fim_y = None

canvas.bind('<ButtonPress-1>', marca_inicio)
canvas.bind('<B1-Motion>', atualiza_fim)

root.mainloop()