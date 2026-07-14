# a parte de modelo da organização MVC transforma o projeto ao incrementar a parte visual e funcional dos arquivos, transmitindo o que foi feito de forma mais clara.
## para o model, primeira etapa da organização, retomamos o arquivo que antes era denominado "Figura.py" e o transformamos no modelo.
### nesse caso, o modelo funciona como o _armazenamento de dados_, ou seja, lida apenas com a denominação da figura a ser criada.
#### abaixo segue o modelo reestruturado e comentado da anterior classe figuras!

# aqui a classe figura permanece sendo a classe mãe de todas as classes de tipos de figuras subsequentes, então apenas precisamos repassar (por isso o pass) as suas
# caracteristicas físicas
class Figuras:
    def __init__(self, coordenadas, cor_borda, cor_preenchimento=""):
        self.coordenadas = coordenadas  
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

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

    def adicionar_figura(self, figura):
        self.figuras.append(figura)

    def limpar_figura_nova(self):
        self.figura_nova = None
