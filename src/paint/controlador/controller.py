"""
Controlador refatorado com Padrão State.
ANTES (Entrega 3): tinha if/elif self.ferramenta_atual == "Linha": ...
AGORA (Entrega 4): delegamos tudo para self.estado_atual.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

# Importamos o modelo
from modelo.figuras import Desenho, Poligono

# Importamos do tkinter para as janelas de Salvar/Abrir
from tkinter import messagebox
from tkinter import filedialog

# Importamos TODOS os estados do novo arquivo estado.py
# ESSA IMPORTAÇÃO NÃO EXISTIA NA ENTREGA 3.
# Na entrega 3, o controlador "sabia" de tudo e fazia tudo sozinho.
# Agora ele DELEGA para os estados.
from controlador.estado import (
    EstadoLinha,
    EstadoRabisco,
    EstadoOval,
    EstadoRetangulo,
    EstadoPoligono,
)

if TYPE_CHECKING:
    from visao.view import TelaDesenho


# Dicionário que mapeia o NOME da ferramenta (string que vem do menu)
# para a INSTÂNCIA do estado correspondente.
# Como os estados não guardam estado interno (só comportamento),
# a gente pode reusar a mesma instância para todo mundo.
# Mapeia o texto vindo do menu diretamente para as instâncias de estado correspondentes
# 
# NA ENTREGA 3, isso era uma string: self.ferramenta_atual = "Linha"
# AGORA, é um dicionário de OBJETOS. A ferramenta atual é um objeto de estado.
_ESTADOS = {
    "Linha": EstadoLinha(),
    "Rabisco": EstadoRabisco(),
    "Oval": EstadoOval(),
    "Retângulo": EstadoRetangulo(),
    "Polígono": EstadoPoligono(),
}


class ControladorDesenho:
    def __init__(self, modelo, tela):
        self.tela = tela
        self.desenho = modelo
        self.poligono_em_construcao = None

        # Cores padrão
        self.cor_borda = "black"
        self.cor_preenchimento = ""

        # ============================================
        # MUDANÇA PRINCIPAL DO STATE (ENTREGA 4)
        # ============================================
        # Antes (Entrega 3): self.ferramenta_atual: str = "Linha"
        # Depois (Entrega 4): self.estado_atual guarda um OBJETO de estado
        # 
        # Por que isso é melhor?
        # - Antes: para adicionar uma nova ferramenta, tinha que abrir o controlador
        #   e adicionar mais um elif no ao_clicar, ao_arrastar, ao_soltar...
        # - Agora: para adicionar uma nova ferramenta, basta criar uma nova classe
        #   que herda de EstadoBase e adicionar no dicionário _ESTADOS.
        #   O controlador NÃO MUDA. Ele só delega.
        self.estado_atual = _ESTADOS["Linha"]

    def set_ferramenta(self, ferramenta):
        """
        A visão chama isso quando o usuário muda a ferramenta no menu dropdown.
        Em vez de guardar uma string, trocamos o objeto de estado.
        
        NA ENTREGA 3:
            self.ferramenta_atual = ferramenta  # só uma string
        
        AGORA:
            self.estado_atual = _ESTADOS[ferramenta]  # um objeto com comportamento
        """
        self.estado_atual = _ESTADOS.get(ferramenta, _ESTADOS["Linha"])

    def set_cor_borda(self, cor):
        self.cor_borda = cor

    def set_cor_preenchimento(self, cor):
        self.cor_preenchimento = cor

    # =========================================================================
    # EVENTOS DO MOUSE (DELEGADOS DIRETAMENTE PARA O ESTADO CORRENTE)
    # =========================================================================
    # 
    # NA ENTREGA 3, cada método aqui tinha um MONTE de if/elif:
    #     def ao_clicar(self, x, y):
    #         if self.ferramenta_atual == "Linha":
    #             ...
    #         elif self.ferramenta_atual == "Oval":
    #             ...
    #         elif self.ferramenta_atual == "Retângulo":
    #             ...
    # 
    # AGORA, cada método tem UMA LINHA SÓ:
    #     self.estado_atual.ao_clicar(self, x, y)
    # 
    # O estado atual (que é um objeto) sabe o que fazer.
    # O controlador não precisa saber QUAL ferramenta está ativa.
    # Ele só passa a mensagem adiante.
    
    def ao_clicar(self, x, y):
        # Antes: um monte de if/elif aqui dentro
        # Agora: uma linha só. O estado sabe o que fazer.
        self.estado_atual.ao_clicar(self, x, y)

    def ao_arrastar(self, x, y):
        self.estado_atual.ao_arrastar(self, x, y)

    def ao_soltar(self, x, y):
        self.estado_atual.ao_soltar(self, x, y)

    def ao_duplo_clique(self, x, y):
        # Só o estado do polígono implementa duplo_clique.
        # Os outros estados herdam o pass (fazem nada) do EstadoBase.
        self.estado_atual.duplo_clique(self, x, y)

    def _redesenhar(self):
        """Método interno que pede pra visão redesenhar tudo."""
        self.tela.atualizar_canvas(
            self.desenho.figuras,
            self.desenho.figura_nova,
            self.poligono_em_construcao
        )

    # =========================================================================
    # FUNCIONALIDADES DO JSON: SALVAR E ABRIR
    # =========================================================================
    # 
    # Esses métodos também são da Entrega 4 (persistência).
    # Eles não são do padrão State, mas fazem parte da minha parte do controller.
    # A serialização/desserialização fica no modelo (cada figura sabe se converter
    # para/de dicionário), mas o controller chama o modelo e cuida da UI
    # (filedialog para escolher arquivo, messagebox para mostrar erro/sucesso).

    def salvar_desenho(self):
        """Inicia a janela de diálogo para salvar o projeto em JSON."""
        caminho = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            try:
                # Delega para o modelo fazer a serialização JSON
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
                # Delega para o modelo fazer a desserialização JSON
                self.desenho.carregar_de_arquivo(caminho)
                # Reseta dados temporários ativos e redesenha a tela carregada
                self.poligono_em_construcao = None
                self.desenho.limpar_figura_nova()
                self._redesenhar()
                messagebox.showinfo("Sucesso", "Desenho carregado com sucesso!")
            except Exception as erro:
                messagebox.showerror("Erro", "Falha ao abrir:\n" + str(erro))
