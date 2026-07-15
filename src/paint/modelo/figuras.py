# a parte de modelo da organização MVC transforma o projeto ao incrementar a parte visual e funcional dos arquivos, transmitindo o que foi feito de forma mais clara.
## para o model, primeira etapa da organização, retomamos o arquivo que antes era denominado "Figura.py" e o transformamos no modelo.
### nesse caso, o modelo funciona como o _armazenamento de dados_, ou seja, lida apenas com a denominação da figura a ser criada.
#### abaixo segue o modelo reestruturado e comentado da anterior classe figuras!

## _mudança da etapa 4!!!_ adicionamos o json para atender ao formato de serializacao, que seria basicamente criar a possibilidade de armazenar a estrutura de dados envolvida em um projeto, 
## pavimentando a possibilidade de clonarmos e recriarmos essa estrutura.
import json
# aqui a classe figura permanece sendo a classe mãe de todas as classes de tipos de figuras subsequentes, então apenas precisamos repassar (por isso o pass) as suas
# caracteristicas físicas
class Figuras:
    def __init__(self, coordenadas, cor_borda, cor_preenchimento):
        self.coordenadas = coordenadas
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

## mudança para incluir a mudança de conversao diretamente na classe figura, que dita o que todas as figuras terão em comum.
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

class Desenho:
    def __init__(self):
        # permanece gerenciando a lista de figuras criadas
        self.figuras = []
        self.figura_nova = None

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
            "Poligono": Poligono
        }
        
        for dados in dados_figuras:
            tipo = dados["tipo"]
            if tipo in mapeamento_classes:
                classe_figura = mapeamento_classes[tipo]
                # usamos o método herdado from_dict para criar o objeto correto, utilizando o dicionario como manual de instrucoes
                figura_reconstruida = classe_figura.from_dict(dados)
                self.adicionar_figura(figura_reconstruida)
