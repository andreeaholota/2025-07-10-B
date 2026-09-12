import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        return DAO.getAllCategories()

    def creaGrafo(self, category, dataI, dataF):
        self._graph.clear()
        self._idMap.clear()

        vertici = DAO.getAllProducts(category)
        for v in vertici:
            self._idMap[v.product_id] = v

        self._graph.add_nodes_from(vertici)

        for v1, v2, weight in DAO.getProductByOrder(category, dataI, dataF):
            self._graph.add_edge(self._idMap[v1], self._idMap[v2], weight=weight)

    def getNumVertici(self):
        return self._graph.number_of_nodes()

    def getNumArchi(self):
        return self._graph.number_of_edges()

    def getAllNodi(self):
        return list(self._graph.nodes())

    def getBestProduct(self, n):
        listaProdotti = []

        for prodotto in self._graph.nodes():
            pesoTotaleUscente = 0
            for _, _, data in self._graph.out_edges(prodotto, data= True):
                pesoTotaleUscente = pesoTotaleUscente + data["weight"]

            pesoTotaleEntrante = 0
            for _, _, data in self._graph.in_edges(prodotto, data=True):
                pesoTotaleEntrante = pesoTotaleEntrante + data["weight"]

            bilancio = pesoTotaleUscente - pesoTotaleEntrante

            listaProdotti.append((prodotto, bilancio))

        return listaProdotti[:n]

