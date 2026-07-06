# main.py
import tkinter as tk
from tkinter import ttk
# Importamos as nossas classes do módulo figuras
from figuras import Linha, Oval, Retangulo, Rabisco, Poligono

# quando mouse é somente pressionado
### MUDANÇA ### Adicionada variável para guardar o polígono em construção
poligono_em_construcao = None

def iniciar_figura_nova(event):
    global figura_nova
    ### MUDANÇA ### Adicionado global para poligono_em_construcao
    global poligono_em_construcao
    
    # implementando getters para pegar a ferramenta e cor selecionadas
    ferramenta_atual = tipo_figura_var.get()
    cor_atual = cor_borda_var.get()
    cor_preenchimento = cor_preenchimento_var.get() #pega a cor de preenchimento selecionada no momento
    
    ### MUDANÇA ### Polígono agora funciona clicando em pontos, não arrastando
    if ferramenta_atual == 'Polígono':
        if poligono_em_construcao is None:
            # Primeiro clique: cria o polígono com lista de pontos
            poligono_em_construcao = Poligono(
                [(event.x, event.y)],  # lista com primeiro ponto
                cor_atual,
                cor_preenchimento
            )
            figura_nova = poligono_em_construcao
        else:
            # Próximos cliques: adiciona mais um ponto
            poligono_em_construcao.adicionar_ponto(event.x, event.y)
        
        desenhar()
        desenhar_preview_poligono()
        return  # Sai da função, não executa o resto
    
    # criamos o objeto correto baseado na seleção, mas ainda na coordenada zero 
    if ferramenta_atual == 'Linha':
        # modificamos a criação do objeto para usar a classe Linha, que antes entrava como elemento da lista de figuras
        figura_nova = Linha((event.x, event.y, event.x, event.y), cor_atual, cor_preenchimento)
    elif ferramenta_atual == 'Oval':
        figura_nova = Oval((event.x, event.y, event.x, event.y), cor_atual, cor_preenchimento)
    elif ferramenta_atual == 'Retângulo':
        figura_nova = Retangulo((event.x, event.y, event.x, event.y), cor_atual, cor_preenchimento)
    elif ferramenta_atual == 'Rabisco':
        figura_nova = Rabisco(([event.x, event.y]), cor_atual, cor_preenchimento)


# quando mouse é movido com o botão pressionado 
def atualizar_figura_nova(event):
    global figura_nova

    if not figura_nova: 
        return
    
    ### MUDANÇA ### Polígono não usa arrastar
    if tipo_figura_var.get() == 'Polígono':
        return
    
    ##if not isinstance(figura_nova, Rabisco):
    ##    figura_nova.cor_preenchimento = cor_atual
    
    # verificamos o tipo do objeto usando isinstance
    if isinstance(figura_nova, Rabisco):
        figura_nova.coordenadas.append((event.x, event.y))
    elif isinstance(figura_nova, Poligono):
        ### MUDANÇA ### Removido - polígono agora não usa arrastar
        pass
    else: 
        # modifica os atributos do objeto para refletir a nova posição do mouse, mantendo a origem fixa
        origem_x, origem_y = figura_nova.coordenadas[0], figura_nova.coordenadas[1]
        figura_nova.coordenadas = (origem_x, origem_y, event.x, event.y)
        
    desenhar()
    desenhar_figura_nova()

# quando mouse é solto
def incluir_figura_nova(event):
    global figura_nova
    
    ### MUDANÇA ### Polígono não salva ao soltar botão
    if tipo_figura_var.get() == 'Polígono':
        return
    
    if figura_nova and not incompleta(figura_nova):
        figuras.append(figura_nova) # guardamos o objeto real na lista
    desenhar()


### MUDANÇA ### FUNÇÃO NOVA: fecha o polígono no duplo clique
def fechar_poligono(event):
    """Chamado no duplo clique para fechar o polígono."""
    global poligono_em_construcao, figura_nova
    
    if poligono_em_construcao is None:
        return
    
    # Adiciona o último ponto (onde deu o duplo clique)
    poligono_em_construcao.adicionar_ponto(event.x, event.y)
    
    # Só salva se tiver pelo menos 3 pontos
    if len(poligono_em_construcao.coordenadas) >= 3:
        figuras.append(poligono_em_construcao)
    
    # Limpa o estado para poder criar outro polígono depois
    poligono_em_construcao = None
    figura_nova = None
    
    desenhar()


# utilizamos o polimorfismo para desenhar cada figura, chamando o método desenhar de cada objeto
def desenhar():
    canvas.delete("all") 
    for figura in figuras:
        figura.desenhar(canvas) 

def desenhar_figura_nova():
    if not figura_nova: 
        return
    # passamos o parâmetro dash para fazer a linha guia pontilhada, identificando que é uma figura em construção
    figura_nova.desenhar(canvas, dash=(4, 2))


### MUDANÇA ### FUNÇÃO NOVA: mostra preview do polígono enquanto clica
def desenhar_preview_poligono():
    """Desenha o polígono em construção com linhas pontilhadas."""
    if poligono_em_construcao is None:
        return
    
    pontos = poligono_em_construcao.coordenadas
    
    # Desenha linhas entre os pontos
    if len(pontos) > 1:
        canvas.create_line(pontos, fill=poligono_em_construcao.cor, dash=(4, 2))
    
    # Desenha círculos nos pontos para visualizar onde clicou
    for x, y in pontos:
        canvas.create_oval(x-3, y-3, x+3, y+3, fill=poligono_em_construcao.cor)


def incompleta(figura):
    # lógica para determinar se a figura está incompleta de sempre
    if isinstance(figura, Rabisco):
        return len(figura.coordenadas) <= 1
    ### MUDANÇA ### Adicionado verificação para Polígono
    elif isinstance(figura, Poligono):
        return len(figura.coordenadas) < 3
    else: 
        return (figura.coordenadas[0], figura.coordenadas[1]) == (figura.coordenadas[2], figura.coordenadas[3])


figuras = []      
figura_nova = None 


def main():
    global canvas, tipo_figura_var, cor_borda_var, cor_preenchimento_var

    root = tk.Tk()
    root.title("UFS Paint - Adicionando o Método Orientado a Objetos")
    frame = tk.Frame(root)

    paddings = {'padx': 5, 'pady': 5}

    # cor da ferramenta

    label = ttk.Label(frame, text='Escolha a Ferramenta:')
    label.grid(column=0, row=0, sticky=tk.W, **paddings)

    tipo_figura_var = tk.StringVar(root)
    ####### menu atualizado incluindo o polígono solicitado ########
    ### MUDANÇA ### Troquei 'Polígono (Triângulo)' por 'Polígono'
    option_menu = ttk.OptionMenu(frame, tipo_figura_var, 'Linha', 'Linha', 'Rabisco', 'Oval', 'Retângulo', 'Polígono')
    option_menu.grid(column=1, row=0, sticky=tk.W, **paddings)

    # cor da borda
    label_cor = ttk.Label(frame, text='Cor da Borda:')
    label_cor.grid(column=2, row=0, sticky=tk.W, **paddings)

    cor_borda_var = tk.StringVar(root)
    cor_preenchimento_var = tk.StringVar(root)
    
    option_menu_cor = ttk.OptionMenu(frame, cor_borda_var, 'black', 'black', 'red', 'blue', 'green', 'orange', 'purple')
    option_menu_cor.grid(column=3, row=0, sticky=tk.W, **paddings)

    # cor do preenchimento
    label_fill = ttk.Label(frame, text='Preenchimento:')
    label_fill.grid(column=4, row=0, sticky=tk.W, **paddings)

    cor_preenchimento_var = tk.StringVar(root)
    #adicionado o seletor de cor de preenchimento com algumas opções básicas
    option_menu_fill = ttk.OptionMenu(frame, cor_preenchimento_var,'', '','red','blue','green','yellow','orange','purple')

    option_menu_fill.grid(column=5, row=0, sticky=tk.W, **paddings)

    canvas = tk.Canvas(frame, bg='white', width=600, height=600)
    canvas.grid(column=0, row=1, columnspan=6, sticky=tk.W, **paddings)

    frame.pack()

    ## realizando as operações de bind para os eventos do mouse, chamando as funções correspondentes
    canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
    canvas.bind('<B1-Motion>', atualizar_figura_nova)
    canvas.bind('<ButtonRelease-1>', incluir_figura_nova)
    
    ### MUDANÇA ### Adicionado evento de duplo clique para fechar polígono
    canvas.bind('<Double-Button-1>', fechar_poligono)

    root.mainloop()

if __name__ == "__main__":
    main()
