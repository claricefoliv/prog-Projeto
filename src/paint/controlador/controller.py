

"""
Controlador refatorado com Padrão State.
ANTES (Entrega 3): tinha if/elif self.ferramenta_atual == "Linha": ...
AGORA (Entrega 4): delegamos tudo para self.estado_atual.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

# Importamos o modelo
from modelo.figuras import Desenho, Poligono, Linha, Oval, Retangulo, Rabisco

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

    def set_ferramenta(self, ferramenta):
        """Altera o comportamento das ferramentas trocando o objeto de estado."""
        self.estado_atual = _ESTADOS.get(ferramenta, _ESTADOS["Linha"])

    def set_cor_borda(self, cor):
        self.cor_borda = cor

    def set_cor_preenchimento(self, cor):
        self.cor_preenchimento = cor

    # =========================================================================
    # EVENTOS DO MOUSE (DELEGADOS DIRETAMENTE PARA O ESTADO CORRENTE)
    # =========================================================================
    
    def ao_clicar(self, x, y):
        self.estado_atual.ao_clicar(self, x, y)

    def ao_arrastar(self, x, y):
        self.estado_atual.ao_arrastar(self, x, y)

    def ao_soltar(self, x, y):
        self.estado_atual.ao_soltar(self, x, y)

    def ao_duplo_clique(self, x, y):
        self.estado_atual.duplo_clique(self, x, y)

    def _redesenhar(self):
        """Informa a visão para atualizar a exibição das figuras no canvas."""
        self.tela.atualizar_canvas(
            self.desenho.figuras,
            self.desenho.figura_nova,
            self.poligono_em_construcao
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
            self._redesenhar()

