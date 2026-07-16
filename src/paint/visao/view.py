import tkinter as tk

from paint.modelo.figuras import Linha, Oval, Retangulo, Rabisco, Poligono

class TelaDesenho:
    """
    Nossa classe de Visão. Ela não pensa, só obedece o controlador 
    e desenha a interface na tela. Tudo que o usuário faz aqui, 
    ela "fofoca" pro controlador resolver.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        
        # Só preenchemos isso depois usando o set_controlador()
        self.controlador = None

        # Preparando o terreno: a barrinha superior pros menus e o quadro branco (canvas)
        self.frame_controles = tk.Frame(self.root)
        self.frame_controles.pack(fill=tk.X, padx=5, pady=5)

        self.canvas = tk.Canvas(self.root, bg='white', width=600, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._criar_menus()

        # Ouvindo os eventos do mouse SÓ aqui na View.
        # Concentrar isso aqui evita bugar com cliques duplicados.
        self.canvas.bind('<ButtonPress-1>', self._ao_clicar)
        self.canvas.bind('<B1-Motion>', self._ao_arrastar)
        self.canvas.bind('<ButtonRelease-1>', self._ao_soltar)
        self.canvas.bind('<Double-Button-1>', self._ao_duplo_clique)

    def set_controlador(self, controlador):
        """Chamado pelo main pra conectar o cérebro (controlador) na tela"""
        self.controlador = controlador

    def _criar_menus(self):
        """Monta os dropdowns na tela e já configura quem avisar quando algo mudar"""
        
        # Menu de qual ferramenta estamos usando
        tk.Label(self.frame_controles, text='Ferramenta:').pack(side=tk.LEFT, padx=(0, 5))
        self.var_ferramenta = tk.StringVar(value='Linha')
        menu_ferramenta = tk.OptionMenu(
            self.frame_controles, self.var_ferramenta,
            'Linha', 'Rabisco', 'Oval', 'Retângulo', 'Polígono',
            command=self._mudar_ferramenta
        )
        menu_ferramenta.pack(side=tk.LEFT, padx=(0, 15))

        # Menu da cor da linha
        tk.Label(self.frame_controles, text='Borda:').pack(side=tk.LEFT, padx=(0, 5))
        self.var_cor_borda = tk.StringVar(value='black')
        menu_cor = tk.OptionMenu(
            self.frame_controles, self.var_cor_borda,
            'black', 'red', 'blue', 'green', 'orange', 'purple',
            command=self._mudar_cor_borda
        )
        menu_cor.pack(side=tk.LEFT, padx=(0, 15))

        # Menu do preenchimento interno
        tk.Label(self.frame_controles, text='Preenchimento:').pack(side=tk.LEFT, padx=(0, 5))
        self.var_preenchimento = tk.StringVar(value='')
        menu_preenchimento = tk.OptionMenu(
            self.frame_controles, self.var_preenchimento,
            '', 'red', 'blue', 'green', 'yellow', 'orange', 'purple',
            command=self._mudar_preenchimento
        )
        menu_preenchimento.pack(side=tk.LEFT)

        # Adicionando botões para Salvar e Abrir projeto JSON
        tk.Frame(self.frame_controles, width=20).pack(side=tk.LEFT) # Espaçador visual
        
        btn_salvar = tk.Button(self.frame_controles, text="Salvar Projeto", command=self._ao_clicar_salvar)
        btn_salvar.pack(side=tk.LEFT, padx=5)

        btn_abrir = tk.Button(self.frame_controles, text="Abrir Projeto", command=self._ao_clicar_abrir)
        btn_abrir.pack(side=tk.LEFT, padx=5)

    # Callbacks dos menus (Avisando o controlador)

    def _mudar_ferramenta(self, valor: str):
        if self.controlador:
            self.controlador.set_ferramenta(valor)

    def _mudar_cor_borda(self, valor: str):
        if self.controlador:
            self.controlador.set_cor_borda(valor)

    def _mudar_preenchimento(self, valor: str):
        if self.controlador:
            self.controlador.set_cor_preenchimento(valor)

    # Callbacks dos botões de persistência
    
    def _ao_clicar_salvar(self):
        if self.controlador:
            self.controlador.salvar_desenho()

    def _ao_clicar_abrir(self):
        if self.controlador:
            self.controlador.abrir_desenho()

    # Eventos do mouse

    def _ao_clicar(self, event):
        if self.controlador:
            self.controlador.ao_clicar(event.x, event.y)

    def _ao_arrastar(self, event):
        if self.controlador:
            self.controlador.ao_arrastar(event.x, event.y)

    def _ao_soltar(self, event):
        if self.controlador:
            self.controlador.ao_soltar(event.x, event.y)

    def _ao_duplo_clique(self, event):
        # Usado mais pro Polígono, pra saber a hora de fechar a forma
        if self.controlador:
            self.controlador.ao_duplo_clique(event.x, event.y)

    #  Desenhando na tela de fato

    def atualizar_canvas(self, figuras, figura_nova, poligono_em_construcao):
        self.canvas.delete("all")

        # Repassa a limpo tudo que já tá desenhado definitivamente
        for figura in figuras:
            self._desenhar_figura(figura)

        # Se estamos criando algo agora, desenha pontilhado.
        # Detalhe: se for um polígono em construção, não desenhamos a 'figura_nova' aqui
        # senão o Tkinter vai tentar preencher o polígono pela metade e fica esquisito.
        if figura_nova and poligono_em_construcao is None:
            self._desenhar_figura(figura_nova, dash=(4, 2))

        # Renderiza o "esqueleto" do polígono que o usuário ainda tá clicando
        if poligono_em_construcao:
            self._desenhar_preview_poligono(poligono_em_construcao)

    def _desenhar_figura(self, figura, dash=None):
        """Faz o trabalho sujo de converter as classes do modelo em tinta no Tkinter"""
        
        if isinstance(figura, Linha):
            x1, y1, x2, y2 = figura.coordenadas
            self.canvas.create_line(x1, y1, x2, y2, fill=figura.cor_borda, dash=dash)

        elif isinstance(figura, Oval):
            x1, y1, x2, y2 = figura.coordenadas
            self.canvas.create_oval(
                x1, y1, x2, y2,
                outline=figura.cor_borda,
                fill=figura.cor_preenchimento,
                dash=dash
            )

        elif isinstance(figura, Retangulo):
            x1, y1, x2, y2 = figura.coordenadas
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline=figura.cor_borda,
                fill=figura.cor_preenchimento,
                dash=dash
            )

        elif isinstance(figura, Rabisco):
            # Truque necessário: o rabisco tem tuplas de pontos [(x,y), ...], 
            # mas o create_line precisa de uma lista "achatada" [x, y, x, y].
            flat = [c for ponto in figura.coordenadas for c in ponto]
            self.canvas.create_line(flat, fill=figura.cor_borda, dash=dash)

        elif isinstance(figura, Poligono):
            # Mesmo macete do achatamento de lista do rabisco
            flat = [c for ponto in figura.coordenadas for c in ponto]
            
            if len(figura.coordenadas) >= 3:
                self.canvas.create_polygon(
                    flat,
                    outline=figura.cor_borda,
                    fill=figura.cor_preenchimento,
                    dash=dash
                )
            elif len(figura.coordenadas) == 2:
                # Com só 2 pontos, ainda é só uma reta
                self.canvas.create_line(flat, fill=figura.cor_borda, dash=dash)

    def _desenhar_preview_poligono(self, poligono):
        """Faz a linha guia tracejada acompanhando o clique do usuário no polígono"""
        pontos = poligono.coordenadas

        if len(pontos) > 1:
            flat = [c for ponto in pontos for c in ponto]
            self.canvas.create_line(flat, fill=poligono.cor_borda, dash=(4, 2))

        # Coloca umas bolinhas nas pontas pra ficar fácil de ver os vértices
        for x, y in pontos:
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=poligono.cor_borda)
