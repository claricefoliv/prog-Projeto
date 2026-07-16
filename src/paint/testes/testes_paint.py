import pytest

from modelo.figuras import Linha, Oval, Retangulo, Rabisco, Poligono, Desenho

class TestGeometriaFiguras:
    """Testes focados na criação das figuras e armazenamento de coordenadas"""

    def test_criacao_linha(self):
        linha = Linha((10, 10, 50, 50), "black", "")
        assert linha.coordenadas == (10, 10, 50, 50)
        assert linha.cor_borda == "black"
        assert linha.cor_preenchimento == ""

    def test_criacao_rabisco(self):
        # O rabisco recebe uma lista de tuplas
        rabisco = Rabisco([(1, 2), (3, 4), (5, 6)], "red", "")
        assert len(rabisco.coordenadas) == 3
        assert rabisco.coordenadas[0] == (1, 2)

    def test_poligono_adicionar_ponto(self):
        # Garante que o polígono inicializa como lista e adiciona novos vértices corretamente
        poligono = Poligono([(0, 0), (10, 0)], "blue", "yellow")
        poligono.adicionar_ponto(5, 10)
        
        assert isinstance(poligono.coordenadas, list)
        assert len(poligono.coordenadas) == 3
        assert poligono.coordenadas == [(0, 0), (10, 0), (5, 10)]


class TestSerializacaoRoundTrip:
    """Testes para o ciclo de serialização"""

    def test_round_trip_retangulo(self):
        retangulo_original = Retangulo((10, 20, 30, 40), "green", "black")
        
        # Converte para dicionário
        dados = retangulo_original.to_dict()
        assert dados["tipo"] == "Retangulo"
        assert dados["coordenadas"] == (10, 20, 30, 40)
        
        # Converte de volta para objeto
        retangulo_recriado = Retangulo.from_dict(dados)
        assert isinstance(retangulo_recriado, Retangulo)
        assert retangulo_recriado.coordenadas == (10, 20, 30, 40)
        assert retangulo_recriado.cor_borda == "green"
        assert retangulo_recriado.cor_preenchimento == "black"

    def test_round_trip_poligono(self):
        # Teste importante devido à lógica de manter coordenadas como lista no from_dict
        poligono_original = Poligono([(0, 0), (10, 10), (0, 10)], "red", "blue")
        dados = poligono_original.to_dict()
        
        poligono_recriado = Poligono.from_dict(dados)
        assert isinstance(poligono_recriado, Poligono)
        assert isinstance(poligono_recriado.coordenadas, list) # Tem que continuar sendo lista
        assert poligono_recriado.coordenadas == [(0, 0), (10, 10), (0, 10)]


class TestCicloSalvarAbrir:
    """Testes para garantir que o Desenho realiza o ciclo salvar e abrir"""

  
    def desenho_original(self):
        desenho = Desenho()
        desenho.adicionar_figura(Linha((0, 0, 100, 100), "black", ""))
        desenho.adicionar_figura(Oval((10, 10, 50, 50), "red", "yellow"))
        return desenho

    def test_salvar_e_carregar_arquivo(self, desenho_original, tmp_path):
        # O tmp_pathcria um arq. temporário
        arquivo_temp = tmp_path / "desenho_teste.json"
        
        # Salva o desenho original no arquivo
        desenho_original.salvar_para_arquivo(arquivo_temp)
        
        # Cria um novo desenho vazio e tenta carregar os dados
        desenho_carregado = Desenho()
        desenho_carregado.carregar_de_arquivo(arquivo_temp)
        
        # Verifica se os dados carregados batem com os originais
        assert len(desenho_carregado.figuras) == 2
        
        figura_1 = desenho_carregado.figuras[0]
        assert isinstance(figura_1, Linha)
        assert figura_1.coordenadas == (0, 0, 100, 100)
        
        figura_2 = desenho_carregado.figuras[1]
        assert isinstance(figura_2, Oval)
        assert figura_2.cor_borda == "red"
        assert figura_2.cor_preenchimento == "yellow”

class TesteNovasFuncionalidades:
    """Testes para as funcionalidades inseridas na Etapa"""
    
    def test_copiar_figura_profundamente(self):
        """Garante que a cópia não compartilha a mesma referência de memória das coordenadas."""
        linha_original = Linha((10, 10, 20, 20), "black", "white")
        linha_copia = linha_original.copiar()
        
        # Verifica se os dados são iguais, mas os objetos (espaços na memória) são diferentes
        assert linha_copia is not linha_original
        assert linha_copia.coordenadas == linha_original.coordenadas
        assert linha_copia.cor_borda == linha_original.cor_borda

    def test_gerenciamento_selecao_multipla(self):
        """Testa se o modelo adiciona e limpa figuras selecionadas corretamente"""
        desenho = Desenho()
        figura1 = Oval((0, 0, 10, 10), "red", "")
        figura2 = Retangulo((20, 20, 30, 30), "blue", "")
        
        desenho.adicionar_selecao(figura1)
        desenho.adicionar_selecao(figura2)
        
        assert len(desenho.figuras_selecionadas) == 2
        assert figura1 in desenho.figuras_selecionadas
        
        # Testar se limpar_selecao esvazia a lista sem deletar as figuras reais
        desenho.limpar_selecao()
        assert len(desenho.figuras_selecionadas) == 0

    def test_remover_figura(self):
        """Testa se uma figura é devidamente deletada dos dados principais. """
        desenho = Desenho()
        figura = Linha((0, 0, 10, 10), "red", "")
        desenho.adicionar_figura(figura)
        
        assert len(desenho.figuras) == 1
        desenho.remover_figura(figura)
        
        # A lista de figuras principais deve ficar vazia
        assert len(desenho.figuras) == 0

