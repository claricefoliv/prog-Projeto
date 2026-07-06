
class Figuras:
    def __init__(self, coordenadas, cor, cor_preenchimento):
        self.coordenadas = coordenadas  # para linha/retangulo/oval será x1, y1, x2, y2
        self.cor = cor
        self.cor_preenchimento = cor_preenchimento

    def desenhar(self, canvas, dash=None):
        # Este método será implementado pelas classes filhas
        pass


class Linha(Figuras):
    def desenhar(self, canvas, dash=None):
        x1, y1, x2, y2 = self.coordenadas
        return canvas.create_line(x1, y1, x2, y2, fill=self.cor, dash=dash)


class Oval(Figuras):
    def desenhar(self, canvas, dash=None):
        x1, y1, x2, y2 = self.coordenadas
        return canvas.create_oval(x1, y1, x2, y2, outline=self.cor, fill=self.cor_preenchimento, dash=dash)


class Retangulo(Figuras):
    def desenhar(self, canvas, dash=None):
        x1, y1, x2, y2 = self.coordenadas
        return canvas.create_rectangle(x1, y1, x2, y2, outline=self.cor, fill=self.cor_preenchimento, dash=dash)


class Rabisco(Figuras):
    def desenhar(self, canvas, dash=None):
        # O rabisco recebe uma lista de pontos [(x1,y1), (x2,y2)...]
        return canvas.create_line(self.coordenadas, fill=self.cor, dash=dash)

# Nova ferramenta solicitada: Polígono
# MUDANÇA: agora o polígono funciona clicando em vários pontos e fechando com duplo clique
class Poligono(Figuras):
    def __init__(self, coordenadas, cor, cor_preenchimento):
        # coordenadas agora é uma LISTA de pontos: [(x1,y1), (x2,y2), ...]
        # antes era uma tupla: (x1, y1, x2, y2, x3, y3)
        super().__init__(coordenadas, cor, cor_preenchimento)
    
    def adicionar_ponto(self, x, y):
        """Adiciona um novo ponto ao polígono."""
        self.coordenadas.append((x, y))
    
    def desenhar(self, canvas, dash=None):
        # O Tkinter cria polígonos recebendo uma lista de pontos ou tupla de coordenadas
        if len(self.coordenadas) >= 3:
            return canvas.create_polygon(
                self.coordenadas,
                outline=self.cor,
                fill=self.cor_preenchimento,
                dash=dash
            )
        elif len(self.coordenadas) == 2:
            # Preview: mostra linha entre os pontos enquanto usuário clica
            return canvas.create_line(
                self.coordenadas,
                fill=self.cor,
                dash=dash
            )
