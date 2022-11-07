
#EXEMPLO DE USO DO DESIGN PATTERN CHAIN OF RESPONSABILITY E ADIÇÃO DE LOGS EM 5 NÍVEIS

from abc import ABC, abstractstaticmethod
import logging

logging.basicConfig(level=logging.DEBUG,
                    filename='logs.txt',
                    format="%(asctime)s - %(levelname)s - %(message)s ")


class Item:
    #método construtor
    def __init__(self, nome: str, valor: int):
        self.nome = nome
        self.valor = valor

    def __repr__(self):
        return f'Item({self.nome}, {self.valor})'


class Carrinho:

    #inicializa a lista de itens
    def __init__(self):
        self.itens = []

    #adiciona os itens numa lista
    def adicionar_item(self, item: Item):
        self.itens.append(item)
        if self.valor == 0:
            logging.critical("Há algum produto com valor zerado no carrinho")
        #para visualizar a lista no console: carrinho.itens

    #soma de todos os itens da lista
    @property
    def valor(self):
        return sum(map(lambda item: item.valor, self.itens))
        #para visualizar a soma no console : carrinho.valor


#de fato uma promoção; uma interface
#classe abstrata: o modo de como a classe será implementada
class Promocao(ABC):

    @abstractstaticmethod
    def calcular(self, valor):
        ...


class PromocaoMaisDeMil(Promocao):
    # def __init__(self, next=None):
    #    self.next = next

    def calcular(self, carrinho: Carrinho):
        if carrinho.valor > 10000:
            logging.warning("Cuidado, carrinho com valor muito alto")
        if carrinho.valor >= 1_000:
            logging.info("Promoção Mais de Mil aplicada !")
            return carrinho.valor - (carrinho.valor * 0.2)
        return self.next.calcular(
            carrinho
        )  #se não estiver mais de mil reais no carrinho, chama a próxima promoção


class Promocao5NoCarrinho(Promocao):
    #def __init__(self, next=None):
    #  self.next = next

    def calcular(self, carrinho: Carrinho):

        if len(carrinho.itens) >= 5:
            logging.info("Promoção Mais de 5 aplicada !")
            return carrinho.valor - (carrinho.valor * 0.1)
            return self.next.calcular(
                carrinho)  #se não tiver 5 itens, chama a próxima promoção


class SemPromocao(Promocao):

    def calcular(self, carrinho: Carrinho):
        logging.info("Nenhuma promoção aplicada!")
        return carrinho.valor  #perceba que aqui não tem chamada para um próximo método, pois aqui é o ponto de parada


class CalculadoraDePromocoes:
    # a ideia não é ser cumulativo, mas se ele nao cair na promoção MaiDeMil, ele tem que retornar o próximo
    def calcular(self, valor):

        p1 = PromocaoMaisDeMil()
        p2 = Promocao5NoCarrinho()
        p3 = SemPromocao()

        p1.next = p2
        p2.next = p3
        return p1.calcular(valor)


logging.debug("Entrou na Calculadora de Promoções")
carrinho = Carrinho()

#Para testar a promoção mais de 5
carrinho.adicionar_item(Item(nome='kitkat', valor=0))
carrinho.adicionar_item(Item(nome='kitkat', valor=10))
carrinho.adicionar_item(Item(nome='kitkat', valor=10))
carrinho.adicionar_item(Item(nome='kitkat', valor=10))
carrinho.adicionar_item(Item(nome='kitkat', valor=10))
# para testar a promoção mais de mil"
carrinho.adicionar_item(Item(nome='kindle', valor=10005))
# para testar o acionamento de nenhuma promoção
carrinho.adicionar_item(Item(nome='kiwi', valor=1))

calculadora = CalculadoraDePromocoes()

#Este erro só é acionado se não tiver nenhum produto no carrinho
if not len(carrinho.itens):
    logging.error("Não há itens adicionados no carrinho")
''''' apenas para facilitar o teste do error acima
teste_itens_zerados=[]   
if not len(teste_itens_zerados) :
 logging.error("Não há itens adicionados no carrinho") ''' ''

logging.info(f'Valor sem promocao: {carrinho.valor}')
logging.info(f'Valor com promocao: {calculadora.calcular(carrinho)}')

logging.info(
    '<<<<<<<<<<<<<<<<<< Execução realizada >>>>>>>>>>>>>>>>>>>>>>>>>>')
