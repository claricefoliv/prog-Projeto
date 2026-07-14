from __future__ import annotations
from typing import TYPE_CHECKING

# MUDANÇA 10: import ajustado para o pacote paint.modelo.figuras
# antes era "from module.base import ..." que não funcionava na estrutura MVC
from paint.modelo.figuras import Figuras, Linha, Oval, Retangulo, Rabisco, Poligono, Desenho

if TYPE_CHECKING:
    # MUDANÇA 11: import condicional para evitar import circular
    # o Controlador precisa saber o tipo TelaDesenho, mas se importasse direto
    # daria circular (View importa Controlador? não, mas é boa prática evitar)
    from paint.visao.view import TelaDesenho


class ControladorDesenho:
    def __init__(self, modelo: Desenho, tela: TelaDesenho) -> None:
        self.tela = tela
        self.desenho = modelo
        self.poligono_em_construcao: Poligono | None = None

        self.ferramenta_atual: str = "Linha"
        self.cor_borda: str = "black"
        self.cor_preenchimento: str = ""

        # MUDANÇA 12: REMOVIDO os self.canvas.bind() daqui!
        # no código original, o Controlador fazia bind nos eventos do canvas
        # mas a View JÁ faz isso e chama os métodos do controlador via callback
        # ter bind nos dois lugares causava duplicação de eventos e comportamento errático

    def set_ferramenta(self, ferramenta: str) -> None:
        self.ferramenta_atual = ferramenta

    def set_cor_borda(self, cor: str) -> None:
        self.cor_borda = cor

    def set_cor_preenchimento(self, cor: str) -> None:
        self.cor_preenchimento = cor

    def ao_clicar(self, x: int, y: int) -> None:
        if self.ferramenta_atual == "Polígono":
            self._clicar_poligono(x, y)
            return

        if self.ferramenta_atual == "Linha":
            self.desenho.figura_nova = Linha((x, y, x, y), self.cor_borda, self.cor_preenchimento)
        elif self.ferramenta_atual == "Oval":
            self.desenho.figura_nova = Oval((x, y, x, y), self.cor_borda, self.cor_preenchimento)
        elif self.ferramenta_atual == "Retângulo":
            self.desenho.figura_nova = Retangulo((x, y, x, y), self.cor_borda, self.cor_preenchimento)
        elif self.ferramenta_atual == "Rabisco":
            self.desenho.figura_nova = Rabisco([(x, y)], self.cor_borda, self.cor_preenchimento)

        self._redesenhar()

    def ao_arrastar(self, x: int, y: int) -> None:
        if self.desenho.figura_nova is None:
            return

        if self.ferramenta_atual == "Polígono":
            return

        if isinstance(self.desenho.figura_nova, Rabisco):
            self.desenho.figura_nova.coordenadas.append((x, y))
        else:
            origem_x, origem_y = self.desenho.figura_nova.coordenadas[0], self.desenho.figura_nova.coordenadas[1]
            self.desenho.figura_nova.coordenadas = (origem_x, origem_y, x, y)

        self._redesenhar()

    def ao_soltar(self, x: int, y: int) -> None:
        if self.ferramenta_atual == "Polígono":
            return

        if self.desenho.figura_nova and not self._incompleta(self.desenho.figura_nova):
            self.desenho.adicionar_figura(self.desenho.figura_nova)

        self.desenho.limpar_figura_nova()
        self._redesenhar()

    def ao_duplo_clique(self, x: int, y: int) -> None:
        if self.poligono_em_construcao is None:
            return

        self.poligono_em_construcao.adicionar_ponto(x, y)

        if len(self.poligono_em_construcao.coordenadas) >= 3:
            self.desenho.adicionar_figura(self.poligono_em_construcao)

        self.poligono_em_construcao = None
        self.desenho.limpar_figura_nova()
        self._redesenhar()

    def _clicar_poligono(self, x: int, y: int) -> None:
        if self.poligono_em_construcao is None:
            self.poligono_em_construcao = Poligono(
                [(x, y)], self.cor_borda, self.cor_preenchimento
            )
            self.desenho.figura_nova = self.poligono_em_construcao
        else:
            self.poligono_em_construcao.adicionar_ponto(x, y)

        self._redesenhar()

    def _incompleta(self, figura: Figuras) -> bool:
        if isinstance(figura, Rabisco):
            return len(figura.coordenadas) <= 1
        elif isinstance(figura, Poligono):
            return len(figura.coordenadas) < 3
        else:
            return (figura.coordenadas[0], figura.coordenadas[1]) == (figura.coordenadas[2], figura.coordenadas[3])

    def _redesenhar(self) -> None:
        self.tela.atualizar_canvas(
            self.desenho.figuras,
            self.desenho.figura_nova,
            self.poligono_em_construcao
        )
