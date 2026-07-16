

import tkinter as tk
from  modelo.figuras import Linha, Oval, Retangulo, Rabisco, Poligono

class TelaDesenho:
    """
    Nossa classe de Visão. Ela não pensa, só obedece o controlador 
    e desenha a interface na tela. Tudo que o usuário faz aqui, 
    ela "fofoca" pro controlador resolver.
    """

    def __init__(self, root: tk.Tk) -> None:
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
        self.canvas.bind('<Delete>', self._ao_apagar)
        self.canvas.bind('<BackSpace>', self._ao_apagar)

        # =========================================================================
        # MUDANÇA ENTREGA 5 — PARTE 3: BIND DE TECLAS PARA COPIAR/COLAR
        # =========================================================================
        # Capturamos Ctrl+C e Ctrl+V no canvas.
        # O Tkinter usa '<Control-c>' (com hífen) para o atalho.
        # Quando o usuário aperta, chamamos o controlador.
        self.canvas.bind('<Control-c>', self._ao_copiar)
        self.canvas.bind('<Control-v>', self._ao_colar)
        #mudança etapa 5 - parte 6: adicionando o bind do botão direito do mouse para seleção de figuras
        self.canvas.bind('<Button-3>', self._iniciar_selecao)
        self.canvas.bind('<B3-Motion>', self._atualizar_selecao)
        self.canvas.bind('<ButtonRelease-3>', self._finalizar_selecao)
        #seleção
    def _iniciar_selecao(self, event):
      if self.controlador:
        self.controlador.iniciar_selecao(event.x, event.y)

    def _atualizar_selecao(self, event):
      if self.controlador:
        self.controlador.atualizar_selecao(event.x, event.y)

    def _finalizar_selecao(self, event):
      if self.controlador:
        self.controlador.finalizar_selecao(event.x, event.y)


    def set_controlador(self, controlador) -> None:
        """Chamado pelo main pra conectar o cérebro (controlador) na tela"""
        self.controlador = controlador

    def _criar_menus(self) -> None:
        """Monta a barra de menu superior e os dropdowns na tela."""
        
        # 1. Criação do menu Arquivo (Barra Superior)
        barra_menus = tk.Menu(self.root)
        self.root.config(menu=barra_menus)

        menu_arquivo = tk.Menu(barra_menus, tearoff=0)
        barra_menus.add_cascade(label="Arquivo", menu=menu_arquivo)
        
        menu_arquivo.add_command(
            label="Abrir", 
            command=lambda: self.controlador.abrir_desenho() if self.controlador else None
        )
        menu_arquivo.add_command(
            label="Salvar", 
            command=lambda: self.controlador.salvar_desenho() if self.controlador else None
        )

        ############### Adicionando um menu de organização das camadas de figuras - Etapa 5: Mover figuras para frente e atrás ########################
        menu_organizar = tk.Menu(barra_menus, tearoff=0)
        barra_menus.add_cascade(label="Organizar Figuras", menu=menu_organizar)
        
        menu_organizar.add_command(
            label="Mover para Frente",
            command=lambda: self.controlador.trazer_para_frente() if self.controlador else None
        )
        menu_organizar.add_command(
            label="Mover para Trás",
            command=lambda: self.controlador.enviar_para_tras() if self.controlador else None
        )
        ############################ Finalizando o Menu da etapa 5: movimentação de camadas ############################

        ################### Adicionando o "mover" como uma ferramenta de botão #########################################
        self.btn_mover = tk.Button(
            self.frame_controles, 
            text="Mover Figura", 
            relief=tk.RAISED,
            bg="#f0f0f0",
            command=self._ativar_modo_mover
        )
        self.btn_mover.pack(side=tk.LEFT, padx=(0, 20)) # dá um espaçamento maior para separar o botão dos seletores, puramente estetico

        ##################### Finalizando o botão

        # 2. Criação dos controles de Ferramentas e Cores (Barra Inferior/Frame)
        # Menu de qual ferramenta estamos usando
        tk.Label(self.frame_controles, text='Ferramenta/Figuras:').pack(side=tk.LEFT, padx=(0, 5))
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
            command=self._set_cor_borda
        )
        menu_cor.pack(side=tk.LEFT, padx=(0, 15))

        # Menu do preenchimento interno
        tk.Label(self.frame_controles, text='Preenchimento:').pack(side=tk.LEFT, padx=(0, 5))
        self.var_preenchimento = tk.StringVar(value='')
        menu_preenchimento = tk.OptionMenu(
            self.frame_controles, self.var_preenchimento,
            '', 'red', 'blue', 'green', 'yellow', 'orange', 'purple',
            command=self._set_cor_preenchimento
        )
        menu_preenchimento.pack(side=tk.LEFT)

    # Callbacks dos menus (Avisando o controlador)

    def _mudar_ferramenta(self, valor: str) -> None:
        if self.controlador:
            self.controlador.set_ferramenta(valor)
## Adicionando o modo de mover como um botão -  Etapa 5: parte de botao visualmente levantado
            self.btn_mover.config(relief=tk.RAISED, bg="#f0f0f0")

    def _ativar_modo_mover(self) -> None:
        ## chamado ao clicar no botão de Mover e avisa o controlador
        if self.controlador:
            self.controlador.set_ferramenta("Mover")
            # deixa o botão visualmente clicado para mostrar que está ativo
            self.btn_mover.config(relief=tk.SUNKEN, bg="#ddd")
## Etapa finalizada!!!

    def _set_cor_borda(self, cor):
        """Atualiza a cor da borda futura e altera a cor da figura atualmente focada, se houver."""
        self.cor_borda = cor
        
        # Se o usuário clicou em uma figura com a ferramenta "Mover" (focando nela), mudamos a cor dela
        if self.controlador.figura_focada:
            self.controlador.figura_focada.cor_borda = cor
            self.controlador._redesenhar()

    def _set_cor_preenchimento(self, cor):
        """Atualiza a cor de preenchimento futura e altera a cor da figura atualmente focada, se houver."""
        self.cor_preenchimento = cor
        
        # Se o usuário clicou em uma figura com a ferramenta "Mover" (focando nela), mudamos a cor dela
        if self.controlador.figura_focada:
            self.controlador.figura_focada.cor_preenchimento = cor
            self.controlador._redesenhar()

    # Eventos do mouse

    def _ao_clicar(self, event) -> None:
        ## adicionando essa parte para focar na figura que queremos copiar e colar
        self.canvas.focus_set()
        if self.controlador:
            self.controlador.ao_clicar(event.x, event.y)

    def _ao_arrastar(self, event) -> None:
        if self.controlador:
            self.controlador.ao_arrastar(event.x, event.y)

    def _ao_soltar(self, event) -> None:
        if self.controlador:
            self.controlador.ao_soltar(event.x, event.y)

    def _ao_duplo_clique(self, event) -> None:
        # Usado mais pro Polígono, pra saber a hora de fechar a forma
        if self.controlador:
            self.controlador.ao_duplo_clique(event.x, event.y)

    # =========================================================================
    # CALLBACKS DE COPIAR/COLAR (ENTREGA 5 — PARTE 3)
    # =========================================================================
    # 
    # Esses métodos são chamados quando o usuário aperta Ctrl+C ou Ctrl+V.
    # Eles perguntam pro controlador o que fazer.
    # 
    # NOTA: O evento do Tkinter passa um objeto, mas não precisamos dele.
    # Usamos '_' para ignorar o parâmetro (convenção Python).

    def _ao_copiar(self, _evento) -> None:
        """
        Chamado quando o usuário aperta Ctrl+C no canvas.
        Pede pro controlador copiar as figuras selecionadas.
        """
        if self.controlador:
            # POR ENQUANTO: como a seleção múltipla ainda não está pronta,
            # copiamos a última figura desenhada para testar.
            # Quando a seleção estiver integrada, trocamos para
            # passar as figuras selecionadas.
            if self.controlador.desenho.figuras:
                self.controlador.copiar_figuras([self.controlador.desenho.figuras[-1]])

    def _ao_colar(self, _evento) -> None:
        """
        Chamado quando o usuário aperta Ctrl+V no canvas.
        Pede pro controlador colar o que está no clipboard.
        """
        if self.controlador:
            self.controlador.colar()

    # Desenhando na tela de fato

    def atualizar_canvas(self, figuras, figura_nova, poligono_em_construcao,figuras_selecionadas,selecao_ativa, inicio_selecao, fim_selecao) -> None:
        """
        O controlador grita "Atualiza!" e a gente refaz o quadro branco.
        """
        self.canvas.delete("all")
        # mudança da etapa 5 - parte 6: desenha as figuras selecionadas com uma borda mais grossa, foi colocado um parâmetro a mais na função para receber as figuras selecionadas chamado largura
        for figura in figuras:
            largura = 3 if figura in figuras_selecionadas else 1
            self._desenhar_figura(figura, largura=largura)

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
            #cria o retangulo da selecao
        if (selecao_ativa and inicio_selecao is not None and fim_selecao is not None):
             self.canvas.create_rectangle(inicio_selecao[0],inicio_selecao[1],fim_selecao[0],fim_selecao[1],outline="blue",dash=(5, 3))    

    def _desenhar_figura(self, figura, dash=None, largura=1) -> None:
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
                dash=dash,
                width=largura
            )

        elif isinstance(figura, Retangulo):
            x1, y1, x2, y2 = figura.coordenadas
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline=figura.cor_borda,
                fill=figura.cor_preenchimento,
                dash=dash,
                width=largura
            )

        elif isinstance(figura, Rabisco):
            # Truque necessário: o rabisco tem tuplas de pontos [(x,y), ...], 
            # mas o create_line precisa de uma lista "achatada" [x, y, x, y].
            flat = [c for ponto in figura.coordenadas for c in ponto]
            self.canvas.create_line(flat, fill=figura.cor_borda, dash=dash,width=largura)

        elif isinstance(figura, Poligono):
            # Mesmo macete do achatamento de lista do rabisco
            flat = [c for ponto in figura.coordenadas for c in ponto]
            
            if len(figura.coordenadas) >= 3:
                self.canvas.create_polygon(
                    flat,
                    outline=figura.cor_borda,
                    fill=figura.cor_preenchimento,
                    dash=dash,
                    width=largura
                )
            elif len(figura.coordenadas) == 2:
                # Com só 2 pontos, ainda é só uma reta
                self.canvas.create_line(flat, fill=figura.cor_borda, dash=dash)

    def _desenhar_preview_poligono(self, poligono) -> None:
        """Faz a linha guia tracejada acompanhando o clique do usuário no polígono"""
        pontos = poligono.coordenadas

        if len(pontos) > 1:
            flat = [c for ponto in pontos for c in ponto]
            self.canvas.create_line(flat, fill=poligono.cor_borda, dash=(4, 2))

        # Coloca umas bolinhas nas pontas pra ficar fácil de ver os vértices
        for x, y in pontos:
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=poligono.cor_borda)

    def _ao_apagar(self, _evento) -> None:
        """
        Chamado quando o usuário aperta Delete ou Backspace no canvas.
        Pede pro controlador apagar a figura que está atualmente focada.
        """
        if self.controlador:
            self.controlador.apagar_figura()
