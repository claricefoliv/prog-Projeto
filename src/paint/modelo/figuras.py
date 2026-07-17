
# a parte de modelo da organização MVC transforma o projeto ao incrementar a parte visual e funcional dos arquivos, transmitindo o que foi feito de forma mais clara.
## para o model, primeira etapa da organização, retomamos o arquivo que antes era denominado "Figura.py" e o transformamos no modelo.
### nesse caso, o modelo funciona como o _armazenamento de dados_, ou seja, lida apenas com a denominação da figura a ser criada.
#### abaixo segue o modelo reestruturado e comentado da anterior classe figuras!

## _mudança!!!_ adicionamos o json para atender ao formato de serializacao, que seria basicamente criarmos a possibilidade de armazenar a estrutura de dados envolvida em um projeto, 
## criando a possibilidade de clonarmos e recriarmos essa estrutura.
import json
# aqui a classe figura permanece sendo a classe mãe de todas as classes de tipos de figuras subsequentes, então apenas precisamos repassar (por isso o pass) as suas
# caracteristicas físicas
class Figuras:
    def __init__(self, coordenadas, cor_borda, cor_preenchimento):
        self.coordenadas = coordenadas
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

## mudança para incluir a mudança de conversao diretamente na classe figura, que dita o que todas as figuras terão em comum. essa seta é um pouco incomum mas é utilizada para
    def to_dict(self):
        ## utilizamos um dicionario para representar as figuras atraves de chaves e valores
        return {
            "tipo": self.__class__.__name__,  # esse valor pega o nome exato da classe
            "coordenadas": self.coordenadas,
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento
        }

    ## agora vem a mudança mais significativa: considerando que todas as classes filhas de "figuras" herdam as mesmas caracteritsticas e parametros da classe mãe, podemos criar um modelo
    ## dentro da propria classe mãe que reconstroi qualquer subclasse de uma forma "padrao" e generaliza os atributos comuns entre si, facilitando não só o entendimento mas também a clareza
    ## do codigo
    @classmethod
    def from_dict(cls, dados: dict):
        # aqui, se for rabisco ou poligono, as coordenadas devem ser mantidas como listas
        if cls.__name__ in ("Rabisco", "Poligono"):
            coords = dados["coordenadas"]
        else:
            # para linha, oval e retângulo, convertemos de volta para tuplas
            coords = tuple(dados["coordenadas"])
        # retornamos por fim um cls com as caracteristicas principais de todas as figuras: coordenadas, borda e preenchimento,
        return cls(
            coordenadas=coords,
            cor_borda=dados["cor_borda"],
            cor_preenchimento=dados["cor_preenchimento"]
        )

    # =========================================================================
    # MUDANÇA ENTREGA 5 — PARTE 3: COPIAR/COLAR
    # =========================================================================
    # Cada figura precisa saber se copiar. Em vez de o controlador
    # saber como copiar cada tipo de figura, a própria figura cria
    # uma cópia de si mesma. Isso é polimorfismo: cada subclasse
    # herda esse método e funciona corretamente.
    # 
    # A cópia é "profunda" para as coordenadas (criamos novas listas/tuplas)
    # para não compartilhar referência com a original.
    def copiar(self):
        # Cria uma NOVA instância da mesma classe com os MESMOS dados
        # mas com coordenadas copiadas (não referenciadas)
        return self.__class__(
            coordenadas=self._copiar_coordenadas(),
            cor_borda=self.cor_borda,
            cor_preenchimento=self.cor_preenchimento
        )
    
    #################### Mudança - Etapa 5 na parte de mover as figuras! #################
    ## a nossa primeira ideia aqui era de fato implementar a logica de deslocar as figuras pelo model, mas isso iria contra a ideia de que estamos apenas armazenando dados.
    ## desse modo, tiramos esse codigo e jogamos ele para o estado, respeitando o modelo mvc.
    '''
    def deslocar(self, dx, dy):
        # move as coordenadas da figura somando uma variação dx e dy: se o clique foi "dentro" dos limites de alguma figura, nós a selecionamos e guardamos onde o clique começou
        if isinstance(self.coordenadas, tuple):
            # para linha, oval e retangulo que usam tuplas de 4 pontos: x1, y1, x2, y2
            x1, y1, x2, y2 = self.coordenadas
            self.coordenadas = (x1 + dx, y1 + dy, x2 + dx, y2 + dy)
        else:
            # para rabisco e poligono que usam listas de pontos [(x,y), ...]
            self.coordenadas = [(x + dx, y + dy) for x, y in self.coordenadas]

    def contem_ponto(self, px, py):
        # verifica se o clique (px, py) ocorreu dentro dos limites da figura
        if isinstance(self.coordenadas, tuple):
            x1, y1, x2, y2 = self.coordenadas
            min_x = min(x1, x2)
            max_x = max(x1, x2)
            min_y = min(y1, y2)
            max_y = max(y1, y2)
        else:
            # para rabisco e polígono, percorre todos os vértices ate achar as extremidades
            todos_x = [ponto[0] for ponto in self.coordenadas]
            todos_y = [ponto[1] for ponto in self.coordenadas]
            min_x = min(todos_x)
            max_x = max(todos_x)
            min_y = min(todos_y)
            max_y = max(todos_y)
        
        # retorna true se o clique estiver dentro das extremidades. esse 5 é para criar uma margem de 5 pixels
        return (min_x - 5 <= px <= max_x + 5) and (min_y - 5 <= py <= max_y + 5)
        '''

    ## a funcao _copiar_coordenadas é a unica que permanece no figuras pois precisamos dela para duplicar os dados! ainda permanecemos delegando somente as funcoes do model para o model.
    def _copiar_coordenadas(self):
        # rabisco e poligono usam lista de tuplas e ai copiamos a lista
        if isinstance(self.coordenadas, list):
            return [tuple(p) for p in self.coordenadas]
        # linha, oval e retangulo usam tupla de 4 números e tambem copiamos a tupla
        else:
            return tuple(self.coordenadas)
        
################### Fim das mudanças de mover a figura no model #########################


# permanecem o mesmo
class Linha(Figuras):
    pass

class Oval(Figuras):
    pass

class Retangulo(Figuras):
    pass

class Rabisco(Figuras):
    pass

# aqui a classe polígono é a única diferente pois é a única classe que possui uma função interna (def adicionar_ponto) para manipular os próprios dados antes da figura ser finalizada. 
# ao inves de pass na classe poligono, possuímos um conjunto de funcões pra conseguir manipular os vertices do poligono.
class Poligono(Figuras):
    def __init__(self, coordenadas, cor, cor_preenchimento=""):
        # garante que coordenadas nasça como uma lista, assim podemos dar .append() e seguir com a lógica do poligono
        super().__init__(list(coordenadas), cor, cor_preenchimento)
    
    def adicionar_ponto(self, x, y):
        # adiciona um novo ponto ao polígono
        self.coordenadas.append((x, y))

# agora temos a classe desenho, que surge com o intuito de transformar a classe figuras em um modelo de fato. essa parte substitui a variavel global anterior que tinhamos no arquivo
# main.py, denominado figuras = [], e a parte figura_nova = none
class Desenho:
    def __init__(self):
        # permanece gerenciando a lista de figuras criadas
        self.figuras = []
        self.figura_nova = None
   # NOVO: Selecionar figuras 
        # guarda todas as figuras atualmente selecionadas
        self.figuras_selecionadas = []
    #NOVO 
    def limpar_selecao(self):
        self.figuras_selecionadas.clear()
    #NOVO
    def adicionar_selecao(self, figura):
        if figura not in self.figuras_selecionadas:
            self.figuras_selecionadas.append(figura)
     

    def adicionar_figura(self, figura):
        self.figuras.append(figura)

    def limpar_figura_nova(self):
        self.figura_nova = None

    ## aqui colocamos as modificacoes para salvar e abrir JSON!!
    def salvar_para_arquivo(self, caminho_arquivo: str) -> None:
        # converte todas as figuras salvas para dicionário atraves do to_dict()
        dados_figuras = [fig.to_dict() for fig in self.figuras]
        # aqui é fundamental para guardar as informacoes em um arquivo JSON: abre o caminho no sistema operacional para um arquivo, denomina como modo de escrita através do w (que significa
        # write) e decodifica elementos do arquivo como acentos ou sinais envolvidos no projeto, como "retângulo" ou :
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            # o indent serve para formatacao do arquivo e o dump serve para fazer a conversao de dados em JSON.
            json.dump(dados_figuras, arquivo, indent=4)

    # Adicionando a função de apagar desenho
    
    def remover_figura(self, figura):
        """Remove a figura selecionada da lista de figuras do desenho."""
        if figura in self.figuras:
            self.figuras.remove(figura)


    def carregar_de_arquivo(self, caminho_arquivo: str) -> None:
        # lê (o r ali significa read) o arquivo JSON e carrega os objetos de figuras da mesma maneira que testado anteriormente na tela
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            dados_figuras = json.load(arquivo)
        
        self.figuras = []  # limpa o canvas atual para receber o novo desenho
        
        # mapeamento em formato de biblioteca para sabermos qual classe instanciar de acordo com o texto do JSON
        mapeamento_classes = {
            "Linha": Linha,
            "Oval": Oval,
            "Retangulo": Retangulo,
            "Rabisco": Rabisco,
            "Poligono": Poligono,
            "GrupoFiguras": GrupoFiguras
        }
        
        for dados in dados_figuras:
            tipo = dados["tipo"]
            if tipo in mapeamento_classes:
                classe_figura = mapeamento_classes[tipo]
                # usamos o método herdado from_dict para criar o objeto correto, utilizando o dicionario como manual de instrucoes
                figura_reconstruida = classe_figura.from_dict(dados)
                self.adicionar_figura(figura_reconstruida)



####################################### MUDANÇA 6 -  COMPOSITE ##################################################
## a ideia do padrão composite é tratar tudo que é selecionado como uma única figura, gerenciando as ações implementadas para todo esse grupo. seguimos com a lógica de listas que utilizamos em todo o projeto, 
## determinando as ações para conjuntos de listas.

class GrupoFiguras(Figuras):
 # método aplicado para determinar as caracteristicas nas figuras 
    def __init__(self, figuras_iniciais=None, cor_borda="black", cor_preenchimento=""):
        super().__init__([], cor_borda, cor_preenchimento)
        self.figuras = figuras_iniciais if figuras_iniciais else []
 # adicionamos a figura a uma lista de elementos para fazer funcionar a seleção grupal
    def adicionar(self, figura):
        if figura not in self.figuras:
            self.figuras.append(figura)
# aqui removemos alguma figura de dentro do conjunto
    def remover(self, figura):
        if figura in self.figuras:
            self.figuras.remove(figura)

## esse @property permite que a gente agrupe um metodo em um atributo puramente gerenciado, tratando como se fossem variaveis comuns
    @property
    def coordenadas(self):
        ## retorna a caixa envolvente (chamada bounding box) de todas as figuras do grupo.
        if not self.figuras:
            return (0, 0, 0, 0)
        
        todos_x = []
        todos_y = []
        for fig in self.figuras:
            coords = fig.coordenadas
            if isinstance(coords, tuple):
                todos_x.extend([coords[0], coords[2]])
                todos_y.extend([coords[1], coords[3]])
            else:
                todos_x.extend([p[0] for p in coords])
                todos_y.extend([p[1] for p in coords])
                
        return (min(todos_x), min(todos_y), max(todos_x), max(todos_y))
## caracteristicas normais vistas anteriormente
    def set_cor_borda(self, cor):
        self.cor_borda = cor
        for fig in self.figuras:
            if isinstance(fig, GrupoFiguras):
                fig.set_cor_borda(cor)
            else:
                fig.cor_borda = cor

    def set_cor_preenchimento(self, cor):
        self.cor_preenchimento = cor
        for fig in self.figuras:
            if isinstance(fig, GrupoFiguras):
                fig.set_cor_preenchimento(cor)
            else:
                fig.cor_preenchimento = cor

    def copiar(self):
        """Copia profunda do grupo e de todos os seus membros."""
        subfiguras_copiadas = [fig.copiar() for fig in self.figuras]
        return GrupoFiguras(subfiguras_copiadas, self.cor_borda, self.cor_preenchimento)

    def to_dict(self):
        """Serialização recursiva para salvar no JSON."""
        return {
            "tipo": "GrupoFiguras",
            "cor_borda": self.cor_borda,
            "cor_preenchimento": self.cor_preenchimento,
            "figuras": [fig.to_dict() for fig in self.figuras]
        }

## esse classmethod transforma um metodo qualquer em um metodo de classe
    @classmethod
    def from_dict(cls, dados: dict):
        # mapeamento dinâmico para reconstruir as subfiguras internas
## dicionario para conseguir utilizar as ferramentas
        mapeamento = {
            "Linha": Linha, "Oval": Oval, "Retangulo": Retangulo,
            "Rabisco": Rabisco, "Poligono": Poligono, "GrupoFiguras": GrupoFiguras
        }
        figuras_reconstitudas = []
        for d in dados["figuras"]:
            classe_fig = mapeamento.get(d["tipo"])
            if classe_fig:
                figuras_reconstitudas.append(classe_fig.from_dict(d))
                
        return cls(
            figuras_iniciais=figuras_reconstitudas,
            cor_borda=dados["cor_borda"],
            cor_preenchimento=dados["cor_preenchimento"]
        )

