

"""
Controlador refatorado com Padrão State.
ANTES (Entrega 3): tinha if/elif self.ferramenta_atual == "Linha": ...
AGORA (Entrega 4): delegamos tudo para self.estado_atual.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

# Importamos o modelo
from modelo.figuras import Desenho, Poligono, Linha, Oval, Retangulo, Rabisco, GrupoFiguras

# Importamos do tkinter para as janelas de Salvar/Abrir
from tkinter import messagebox
from tkinter import filedialog

# Importamos TODOS os estados do novo arquivo estado.py
from controlador.estado import (
    EstadoLinha,
    EstadoRabisco,
    EstadoOval,
    EstadoRetangulo,
    EstadoPoligono,
    EstadoMover, # adicionando o estado de mover que criamos na etapa 5
)

if TYPE_CHECKING:
    from visao.view import TelaDesenho


# Dicionário que mapeia o NOME da ferramenta (string que vem do menu)
# para a INSTÂNCIA do estado correspondente.
# Como os estados não guardam estado interno (só comportamento),
# a gente pode reusar a mesma instância para todo mundo.
# Mapeia o texto vindo do menu diretamente para as instâncias de estado correspondentes
_ESTADOS = {
    "Linha": EstadoLinha(),
    "Rabisco": EstadoRabisco(),
    "Oval": EstadoOval(),
    "Retângulo": EstadoRetangulo(),
    "Polígono": EstadoPoligono(),
    "Mover": EstadoMover(), # adicionando o estado de mover que criamos na etapa 5
}


class ControladorDesenho:
    def __init__(self, modelo, tela):
        self.tela = tela
        self.desenho = modelo
        self.poligono_em_construcao = None

        # Cores padrão
        self.cor_borda = "black"
        self.cor_preenchimento = ""

        # O estado inicial começa ativo na ferramenta Linha
        self.estado_atual = _ESTADOS["Linha"]

        # =========================================================================
        # MUDANÇA ENTREGA 5 — PARTE 3: CLIPBOARD PARA COPIAR/COLAR
        # =========================================================================
        # Guarda as figuras copiadas temporariamente.
        # É uma lista porque quando a seleção múltipla estiver pronta
        # vamos poder copiar várias figuras de uma vez.
        self._clipboard: list = []
        ## Mudança da etapa 5 na parte de mover: criamos esse atributo para saber qual figura foi selecionada ao clicarmos na interface
        self.figura_focada = None
         #  mudanças da etapa 5: criamos esses atributos para saber se o usuário está selecionando uma área do canvas para selecionar figuras
        self.selecao_ativa = False 
        self.inicio_selecao = None 
        self.fim_selecao = None
        #selecionar e mover figuras
        self.movendo = False
        self.ultimo_x = 0
        self.ultimo_y = 0
       

    def set_ferramenta(self, ferramenta):
        """Altera o comportamento das ferramentas trocando o objeto de estado."""
        self.estado_atual = _ESTADOS.get(ferramenta, _ESTADOS["Linha"])

    def set_cor_borda(self, cor):
        self.cor_borda = cor

    def set_cor_preenchimento(self, cor):
        self.cor_preenchimento = cor
        
    def iniciar_selecao(self, x, y):
    
   # Chamado quando o usuário pressiona o botão direito.
   # Não interfere no padrão State porque não estamos desenhando / Mudança etapa 5 - parte 6: adicionamos a lógica de seleção de figuras, que é independente do estado atual.
   # uma figura, apenas iniciando uma região de seleção.
     self.selecao_ativa = True
     self.inicio_selecao = (x, y)
     self.fim_selecao = (x, y)
     self.desenho.limpar_selecao()
     self._redesenhar()    

    def atualizar_selecao(self, x, y): # mudança etapa 5 - parte 6: Atualiza a região de seleção enquanto o usuário arrasta o mouse.
      
     if not self.selecao_ativa:
        return

     self.fim_selecao = (x, y)
     self._redesenhar()

    def finalizar_selecao(self, x, y): # mudança etapa 5: Finaliza a seleção e determina quais figuras estão dentro da região selecionada.

     if not self.selecao_ativa:
        return

     self.fim_selecao = (x, y)

     self.desenho.limpar_selecao()

     x1 = min(self.inicio_selecao[0], self.fim_selecao[0])
     y1 = min(self.inicio_selecao[1], self.fim_selecao[1])

     x2 = max(self.inicio_selecao[0], self.fim_selecao[0])
     y2 = max(self.inicio_selecao[1], self.fim_selecao[1])

    # percorremos todas as figuras procurando quais estão
    # completamente dentro do retângulo desenhado.

     for figura in self.desenho.figuras:

        if self.figura_dentro_da_area(figura, x1, y1, x2, y2):

            self.desenho.adicionar_selecao(figura)

     self.selecao_ativa = False

     self._redesenhar()

    def figura_dentro_da_area(self, figura, x1, y1, x2, y2): # mudança etapa 5 - parte 6: Verifica se uma figura está completamente dentro da área de seleção.
     coords = figura.coordenadas
     if isinstance(coords, tuple): #Linha, Oval, Retângulo

        fx1 = min(coords[0], coords[2])
        fy1 = min(coords[1], coords[3])
        fx2 = max(coords[0], coords[2])
        fy2 = max(coords[1], coords[3])

        return (fx1 >= x1 and fy1 >= y1 and fx2 <= x2 and fy2 <= y2)    
     else:# Rabisco, Polígono

        xs = [p[0] for p in coords]
        ys = [p[1] for p in coords]

        return (min(xs) >= x1 and min(ys) >= y1 and max(xs) <= x2 and max(ys) <= y2)


    # =========================================================================
    # EVENTOS DO MOUSE (DELEGADOS DIRETAMENTE PARA O ESTADO CORRENTE)
    # =========================================================================
    
    def ao_clicar(self, x, y):
        # Verifica se o clique foi em alguma figura selecionada
        for figura in self.desenho.figuras_selecionadas:
         if self.clique_dentro_da_figura(figura, x, y):
            self.movendo = True
            self.ultimo_x = x
            self.ultimo_y = y
            return
        self.estado_atual.ao_clicar(self, x, y)

    def ao_arrastar(self, x, y):
        # Se estamos movendo figuras selecionadas
     if self.movendo:
        dx = x - self.ultimo_x
        dy = y - self.ultimo_y
        self.mover_figuras_selecionadas(dx, dy)
        self.ultimo_x = x
        self.ultimo_y = y
        self.estado_atual.ao_arrastar(self, x, y)
        return
    # Caso contrário continua desenhando normalmente
     self.estado_atual.ao_arrastar(self, x, y)

    def ao_soltar(self, x, y):
        # Se estava movendo, apenas finaliza o movimento
     if self.movendo:
        self.movendo = False
        return

    # Caso contrário continua o comportamento da ferramenta atual
     self.estado_atual.ao_soltar(self, x, y)

    def ao_duplo_clique(self, x, y):
        self.estado_atual.duplo_clique(self, x, y)

    #clicar dentro da figura para selecionar a figura e mover ela
    def clique_dentro_da_figura(self, figura, x, y):

     coords = figura.coordenadas

     if isinstance(coords, tuple):

        fx1 = min(coords[0], coords[2])
        fy1 = min(coords[1], coords[3])
        fx2 = max(coords[0], coords[2])
        fy2 = max(coords[1], coords[3])

     else:

        xs = [p[0] for p in coords]
        ys = [p[1] for p in coords]

        fx1 = min(xs)
        fy1 = min(ys)
        fx2 = max(xs)
        fy2 = max(ys)

     return fx1 <= x <= fx2 and fy1 <= y <= fy2    


    def _redesenhar(self):
        """Informa a visão para atualizar a exibição das figuras no canvas."""
        self.tela.atualizar_canvas(
            self.desenho.figuras,
            self.desenho.figura_nova,
            self.poligono_em_construcao,
            self.desenho.figuras_selecionadas, #
            self.selecao_ativa,                # Adicionado na etapa 5 - parte 6: passamos para a visão se a seleção está ativa e as coordenadas da seleção
            self.inicio_selecao,               #
            self.fim_selecao                   #
        )

    # =========================================================================
    # FUNCIONALIDADES DO JSON: SALVAR E ABRIR
    # =========================================================================

    def salvar_desenho(self):
        """Inicia a janela de diálogo para salvar o projeto em JSON."""
        caminho = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            try:
                self.desenho.salvar_para_arquivo(caminho)
                messagebox.showinfo("Sucesso", "Desenho salvo com sucesso!")
            except Exception as erro:
                messagebox.showerror("Erro", "Falha ao salvar:\n" + str(erro))

    def abrir_desenho(self):
        """Inicia a janela para carregar e importar o arquivo JSON."""
        caminho = filedialog.askopenfilename(
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            try:
                self.desenho.carregar_de_arquivo(caminho)
                # Reseta dados temporários ativos e redesenha a tela carregada
                self.poligono_em_construcao = None
                self.desenho.limpar_figura_nova()
                self._redesenhar()
                messagebox.showinfo("Sucesso", "Desenho carregado com sucesso!")
            except Exception as erro:
                messagebox.showerror("Erro", "Falha ao abrir:\n" + str(erro))

    # =========================================================================
    # MUDANÇA ENTREGA 5 — PARTE 3: COPIAR E COLAR (CTRL+C / CTRL+V)
    # =========================================================================
    # 
    # NA ENTREGA 4 não existia isso. Agora precisamos permitir que o usuário
    # copie figuras já desenhadas e cole em outro lugar.
    # 
    # O fluxo é:
    #   1. Usuário seleciona uma figura (na visão, clica nela)
    #   2. Usuário aperta Ctrl+C -> chama copiar_figuras()
    #   3. As figuras selecionadas vão pro clipboard (self._clipboard)
    #   4. Usuário aperta Ctrl+V -> chama colar()
    #   5. Cria cópias das figuras do clipboard com um deslocamento (+10, +10)
    #      para não ficar EXATAMENTE em cima da original
    #   6. Adiciona as cópias ao desenho e redesenha

    def copiar_figuras(self, figuras):
        """
        Recebe uma lista de figuras e coloca no clipboard.
        Chamado pela visão quando o usuário aperta Ctrl+C.
        """
        # Guardamos CÓPIAS das figuras, não as originais.
        # Se guardássemos as originais e o usuário movesse depois,
        # o clipboard teria as coordenadas erradas.
        self._clipboard = [fig.copiar() for fig in figuras]

    def colar(self):
        """
        Cola as figuras do clipboard no canvas.
        Cada figura colada é deslocada em +10px pra direita e +10px pra baixo
        para não ficar exatamente em cima da original.
        """
        if not self._clipboard:
            # Nada no clipboard, não faz nada
            return

        for figura in self._clipboard:
            # Cria uma CÓPIA da cópia (para poder colar várias vezes)
            nova_figura = figura.copiar()
            # Desloca a figura para não sobrepor a original
            self._deslocar_figura(nova_figura, 10, 10)
            # Adiciona ao modelo
            self.desenho.adicionar_figura(nova_figura)

        self._redesenhar()

    def _deslocar_figura(self, figura, dx, dy):
        """
        Move uma figura em (dx, dy) pixels.
        Cada tipo de figura tem coordenadas diferentes, então
        precisamos tratar cada caso.
        """
        if isinstance(figura, (Linha, Oval, Retangulo)):
            # Tupla de 4 elementos: (x1, y1, x2, y2)
            x1, y1, x2, y2 = figura.coordenadas
            figura.coordenadas = (x1 + dx, y1 + dy, x2 + dx, y2 + dy)

        elif isinstance(figura, (Rabisco, Poligono)):
            # Lista de tuplas: [(x1,y1), (x2,y2), ...]
            figura.coordenadas = [
                (x + dx, y + dy) for x, y in figura.coordenadas
            ]

    def mover_figuras_selecionadas(self, dx, dy): #Move todas as figuras atualmente selecionadas.

        for figura in self.desenho.figuras_selecionadas:
            self._deslocar_figura(figura, dx, dy)

        self._redesenhar()
       
    ################# Lógica principal da movimentação para frente e para trás das figuras implementadas - Etapa 5 ######################

    def trazer_para_frente(self):
        # seguimos uma lógica de mover a figura atualmente focada para a frente, ou seja, no fim de uma lista, via .append
        if self.figura_focada and self.figura_focada in self.desenho.figuras:
            self.desenho.figuras.remove(self.figura_focada)
            self.desenho.figuras.append(self.figura_focada)
            self._redesenhar()

    def enviar_para_tras(self):
        # move a figura atualmente focada para o fundo, ou seja, início da lista, via .insert
        if self.figura_focada and self.figura_focada in self.desenho.figuras:
            self.desenho.figuras.remove(self.figura_focada)
            self.desenho.figuras.insert(0, self.figura_focada)

    def apagar_figura(self):
        """
        Apaga a figura atualmente focada pelo usuário.
        Chamado pela visão quando o usuário aperta a tecla Delete.
        """
        if self.figura_focada and self.figura_focada in self.desenho.figuras:
            # Remove a figura do modelo
            self.desenho.remover_figura(self.figura_focada)
            
            # Limpa a referência da figura focada (já que ela não existe mais)
            self.figura_focada = None 
            
            # Pede para a tela se atualizar sem a figura
            self._redesenhar()

    
    ###################### OPERAÇÕES DO COMPOSITE (AGRUPAR/DESAGRUPAR): ETAPA 6 ############################

    def agrupar_selecionadas(self):
        ## agrupa todas as figuras atualmente selecionadas em um único Composite!!!
        if len(self.desenho.figuras_selecionadas) < 2:
            messagebox.showwarning("Aviso", "Selecione pelo menos 2 figuras para agrupar.")
            return

        # cria o grupo contendo as figuras selecionadas
        grupo = GrupoFiguras(
            figuras_iniciais=list(self.desenho.figuras_selecionadas),
            cor_borda=self.cor_borda,
            cor_preenchimento=self.cor_preenchimento
        )

        # remove as figuras individuais do canvas principal
        for fig in self.desenho.figuras_selecionadas:
            self.desenho.remover_figura(fig)

        # adiciona o grupo recém-criado como uma única entidade
        self.desenho.adicionar_figura(grupo)

        # limpa as seleções antigas e foca no grupo criado
        self.desenho.limpar_selecao()
        self.desenho.adicionar_selecao(grupo)
        self.figura_focada = grupo

        self._redesenhar()
        messagebox.showinfo("Sucesso", "Figuras agrupadas com sucesso!")

    def desagrupar_selecionada(self):
        # desfaz o grupo selecionado, devolvendo as figuras originais ao canvas.
        grupos_para_desfazer = [fig for fig in self.desenho.figuras_selecionadas if isinstance(fig, GrupoFiguras)]

        if not grupos_para_desfazer:
            messagebox.showwarning("Aviso", "A figura selecionada não é um grupo.")
            return

        for grupo in grupos_para_desfazer:
            # devolve as subfiguras de volta para o desenho principal
            for fig in grupo.figuras:
                self.desenho.adicionar_figura(fig)
                self.desenho.adicionar_selecao(fig)

            # remove o grupo do canvas e limpa a seleção dele
            self.desenho.remover_figura(grupo)
            self.desenho.figuras_selecionadas.remove(grupo)
            if self.figura_focada == grupo:
                self.figura_focada = None

        self._redesenhar()
        messagebox.showinfo("Sucesso", "Grupo desfeito com sucesso!")

