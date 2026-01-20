import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self.load_all_artists()
        self.lista_artisti_album = []
        self.lista_artisti_genere = []
        self.id_map = {}
        self.nodes = []
        self.edges = []

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        self.lista_artisti_album = DAO.prendi_artisti_con_album_maggiore(min_albums)

    def build_graph(self):
        self._graph.clear()
        for artista in self.lista_artisti_album:
            self.nodes.append(artista)
        self._graph.add_nodes_from(self.nodes)
        self.id_map = {}
        for nodo in self.nodes:
            self.id_map[nodo[0]] = nodo
        archi_pesati = []
        for id1, id2, peso in DAO.prendi_artisti_con_canzone_stesso_genere():
            if id1 in self.id_map and id2 in self.id_map:
                archi_pesati.append((self.id_map[id1], self.id_map[id2], peso))
        self._graph.add_weighted_edges_from(archi_pesati)

    def get_artisti_collegati(self, artista):
        vicini = self._graph.neighbors(artista)
        vicini_tupla = []
        for v in vicini:
            vicini_tupla.append((v, self._graph[artista][v]["weight"]))
            vicini_tupla.sort(key=lambda x: x[1], reverse=False)
        return vicini_tupla

    def compute_path(self):
        self.path = []
        self.path_edge = []
        self.sol_best = 0
        partial = []






