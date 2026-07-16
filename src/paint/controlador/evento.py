"""
Padrão State — Parte 1 da Entrega 4.

O problema da Entrega 3: o nosso ControladorDesenho tinha um monte de
if/elif self.ferramenta_atual == "Linha": ... elif == "Oval": ...
Isso é código condicional de tipo. Se a gente quiser adicionar uma nova
ferramenta no futuro, precisa abrir o controlador e mexer nele.

A solução do State: cada ferramenta vira uma CLASSE que sabe sozinha
como reagir a clique, arraste e soltar. O controlador só guarda
"qual estado está ativo agora" e delega os eventos para ele.

Isso elimina completamente os if/elif do controlador.
"""
from future import annotations
from typing import TYPE_CHECKING

Importamos as figuras do modelo para criar os objetos
Cada estado precisa instanciar a figura correspondente (Linha, Oval, etc.)
from modelo.figuras import Linha, Oval, Retangulo, Rabisco, Poligono

if TYPE_CHECKING:
# Import condicional para evitar circular.
# O estado precisa conhecer o controlador para acessar
# self.desenho, self.cor_borda, etc.
# Usamos TYPE_CHECKING porque se importássemos direto, poderia dar
# import circular: controller importa estado, estado importa controller.
from controlador.controller import ControladorDesenho


class EstadoBase:
"""
Classe base (abstrata) de todos os estados.
Cada ferramenta herda dela e sobrescreve os métodos que precisa.

Por padrão, os métodos fazem nada. As subclasses implementam
o comportamento específico de cada ferramenta.

ESSA CLASSE NÃO EXISTIA NA ENTREGA 3.
Na entrega 3, o controlador tinha if/elif para cada ferramenta.
Agora, cada ferramenta é um estado concreto que herda desta base.
"""

def ao_clicar(self, ctrl: ControladorDesenho, x: int, y: int) -> None:
"""Chamado quando o usuário clica no canvas."""
pass

def ao_arrastar(self, ctrl: ControladorDesenho, x: int, y: int) -> None:
"""Chamado quando o usuário arrasta o mouse."""
pass

def ao_soltar(self, ctrl: ControladorDesenho, x: int, y: int) -> None:
"""Chamado quando o usuário solta o botão do mouse."""
pass

def duplo_clique(self, ctrl: ControladorDesenho, x: int, y: int) -> None:
"""Chamado no duplo clique. Só o Polígono usa."""
pass


class EstadoLinha(EstadoBase):
"""
Estado da ferramenta Linha.
Clica -> cria linha na origem. Arrasta -> atualiza destino. Soltar -> salva.

NA ENTREGA 3, isso era um bloco if dentro do ao_clicar() do controlador:
if self.ferramenta_atual == "Linha":
self.desenho.figura_nova = Linha(...)

AGORA, isso é uma classe separada. O controlador só faz:
self.estado_atual.ao_clicar(self, x, y)
E o EstadoLinha sabe o que fazer.
"""

def ao_clicar(self, ctrl, x, y):
# Criamos a linha com origem e destino no mesmo ponto (ainda não arrastou)
# Acessamos ctrl.desenho (o modelo) e ctrl.cor_borda (a cor escolhida na UI)
ctrl.desenho.figura_nova = Linha(
(x, y, x, y), ctrl.cor_borda, ctrl.cor_preenchimento
)

def ao_arrastar(self, ctrl, x, y):
# Atualizamos o destino da linha mantendo a origem fixa
# coordenadas[0], [1] = x1, y1 (origem fixa)
# coordenadas[2], [3] = x2, y2 (destino que muda com o mouse)
if ctrl.desenho.figura_nova:
x1, y1 = ctrl.desenho.figura_nova.coordenadas[0], ctrl.desenho.figura_nova.coordenadas[1]
ctrl.desenho.figura_nova.coordenadas = (x1, y1, x, y)
# Chamamos redesenhar para a UI mostrar a linha "esticando" em tempo real
ctrl._redesenhar()

def ao_soltar(self, ctrl, x, y):
# Só salvamos se o usuário realmente arrastou (origem != destino)
# Se clicou e soltou no mesmo lugar, não cria uma linha invisível
fig = ctrl.desenho.figura_nova
if fig and (fig.coordenadas[0], fig.coordenadas[1]) != (fig.coordenadas[2], fig.coordenadas[3]):
ctrl.desenho.adicionar_figura(fig)
# Limpamos a figura temporária (figura_nova) porque já salvamos no modelo
ctrl.desenho.limpar_figura_nova()
ctrl._redesenhar()


class EstadoRabisco(EstadoBase):
"""
Estado da ferramenta Rabisco (mão livre).
Clica -> cria lista com 1 ponto. Arrasta -> vai adicionando pontos.

NA ENTREGA 3, isso era outro bloco elif:
elif self.ferramenta_atual == "Rabisco":
self.desenho.figura_nova = Rabisco(...)

AGORA é uma classe própria com sua lógica de arrastar (append de pontos).
"""

def ao_clicar(self, ctrl, x, y):
# Rabisco guarda uma LISTA de pontos, não uma tupla fixa
# Começa com apenas 1 ponto (onde o usuário clicou)
ctrl.desenho.figura_nova = Rabisco(
[(x, y)], ctrl.cor_borda, ctrl.cor_preenchimento
)

def ao_arrastar(self, ctrl, x, y):
# Diferente da Linha/Oval/Retângulo, aqui NÃO substituímos coordenadas
# Em vez disso, APENDAMOS novos pontos à lista
# Isso cria o traçado "mão livre"
if ctrl.desenho.figura_nova:
ctrl.desenho.figura_nova.coordenadas.append((x, y))
ctrl._redesenhar()

def ao_soltar(self, ctrl, x, y):
# Só salvamos se tem mais de 1 ponto (formou uma linha)
# Um único ponto não é um desenho válido
fig = ctrl.desenho.figura_nova
if fig and len(fig.coordenadas) > 1:
ctrl.desenho.adicionar_figura(fig)
ctrl.desenho.limpar_figura_nova()
ctrl._redesenhar()


class EstadoOval(EstadoBase):
"""Estado da ferramenta Oval. Mesma lógica da Linha/Retângulo (clica e arrasta)."""

def ao_clicar(self, ctrl, x, y):
# Mesmo padrão da Linha: cria com origem=destino=(x,y)
ctrl.desenho.figura_nova = Oval(
(x, y, x, y), ctrl.cor_borda, ctrl.cor_preenchimento
)

def ao_arrastar(self, ctrl, x, y):
# Mesmo padrão da Linha: atualiza destino mantendo origem
if ctrl.desenho.figura_nova:
x1, y1 = ctrl.desenho.figura_nova.coordenadas[0], ctrl.desenho.figura_nova.coordenadas[1]
ctrl.desenho.figura_nova.coordenadas = (x1, y1, x, y)
ctrl._redesenhar()

def ao_soltar(self, ctrl, x, y):
# Mesmo padrão da Linha: valida se houve movimento antes de salvar
fig = ctrl.desenho.figura_nova
if fig and (fig.coordenadas[0], fig.coordenadas[1]) != (fig.coordenadas[2], fig.coordenadas[3]):
ctrl.desenho.adicionar_figura(fig)
ctrl.desenho.limpar_figura_nova()
ctrl._redesenhar()


class EstadoRetangulo(EstadoBase):
"""Estado da ferramenta Retângulo. Mesma lógica da Linha/Oval."""

def ao_clicar(self, ctrl, x, y):
ctrl.desenho.figura_nova = Retangulo(
(x, y, x, y), ctrl.cor_borda, ctrl.cor_preenchimento
)

def ao_arrastar(self, ctrl, x, y):
if ctrl.desenho.figura_nova:
x1, y1 = ctrl.desenho.figura_nova.coordenadas[0], ctrl.desenho.figura_nova.coordenadas[1]
ctrl.desenho.figura_nova.coordenadas = (x1, y1, x, y)
ctrl._redesenhar()

def ao_soltar(self, ctrl, x, y):
fig = ctrl.desenho.figura_nova
if fig and (fig.coordenadas[0], fig.coordenadas[1]) != (fig.coordenadas[2], fig.coordenadas[3]):
ctrl.desenho.adicionar_figura(fig)
ctrl.desenho.limpar_figura_nova()
ctrl._redesenhar()


class EstadoPoligono(EstadoBase):
"""
Estado da ferramenta Polígono.
Diferente das outras: não usa arrastar. Cada clique adiciona um vértice.
Duplo clique fecha e salva.

NA ENTREGA 3, o polígono era o caso mais complicado no controlador,
com lógica especial no ao_clicar, ao_soltar e ao_duplo_clique.

AGORA, toda essa lógica especial está encapsulada AQUI.
O controlador nem sabe que o polígono é diferente — só delega.
"""

def ao_clicar(self, ctrl, x, y):
# Se não tem polígono em construção, criamos um novo
# ctrl.poligono_em_construcao é uma variável do controlador
# que o EstadoPoligono usa para saber se está no meio de um polígono
if ctrl.poligono_em_construcao is None:
ctrl.poligono_em_construcao = Poligono(
[(x, y)], ctrl.cor_borda, ctrl.cor_preenchimento
)
# figura_nova é o que aparece "ao vivo" no canvas antes de salvar
ctrl.desenho.figura_nova = ctrl.poligono_em_construcao
else:
# Já tem polígono em andamento -> adicionamos mais um vértice
ctrl.poligono_em_construcao.adicionar_ponto(x, y)
ctrl._redesenhar()

def ao_soltar(self, ctrl, x, y):
# Polígono NÃO salva no soltar (diferente das outras ferramentas)
# O polígono só é salvo no duplo_clique
# Por isso, ao_soltar faz nada (herdaria pass do EstadoBase mesmo)
pass

def duplo_clique(self, ctrl, x, y):
# Fechamos o polígono: adicionamos o último ponto e salvamos
if ctrl.poligono_em_construcao is None:
return
ctrl.poligono_em_construcao.adicionar_ponto(x, y)
# Só salvamos se tem pelo menos 3 pontos (forma fechada)
# Menos que 3 pontos não forma um polígono válido
if len(ctrl.poligono_em_construcao.coordenadas) >= 3:
ctrl.desenho.adicionar_figura(ctrl.poligono_em_construcao)
# Limpamos o estado para poder criar outro polígono depois
ctrl.poligono_em_construcao = None
ctrl.desenho.limpar_figura_nova()
ctrl._redesenhar()
