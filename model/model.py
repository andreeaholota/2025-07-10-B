import copy

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

    def getCamminoOttimo(self, nodo_start_str, nodo_end_str, lun):
        nodo_start = self._idMap[nodo_start_str]
        nodo_end = self._idMap[nodo_end_str]

        self._bestPath = None
        self._bestScore = -1
        print(f"Chiamo la funzione  con {nodo_start_str} e {nodo_end_str}\n\n")
        self._ricorsione(nodo_start, nodo_end, [nodo_start], 0 , lun+1)
        print(f"->-> Best path: {self._bestPath}")
        return self._bestPath, self._bestScore

    def _ricorsione(self, nodo_corrente, nodo_end, parziale, peso, lun):
        if len(parziale) == lun:
            print(f"Raggiunta la lunghezza massima")
            if nodo_corrente == nodo_end and peso > self._bestScore:
                print(f"Trovato nuovo massimo: {peso} \n\n")
                self._bestScore = peso
                self._bestPath = copy.deepcopy(parziale)
            return
        print("---------------------------------")
        for vicino in self._graph.successors(nodo_corrente):
            print(f"Raggiunto il nodo vicino {vicino}")
            if vicino not in parziale:
                pesoArco = self._graph[nodo_corrente][vicino]["weight"]
                parziale.append(vicino)
                self._ricorsione(vicino, nodo_end, parziale, peso + pesoArco, lun)
                parziale.pop()





