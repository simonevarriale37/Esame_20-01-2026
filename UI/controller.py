import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        try:
            n_alb = int(self._view.txtNumAlbumMin.value)
            if n_alb < 0:
                self._view.show_alert("Inserire un numero maggiore di zero")
                return
        except ValueError:
            self._view.show_alert("inserire un valore numerico")
            return
        self._model.load_artists_with_min_albums(n_alb)
        self._model.build_graph()
        opzioni = []
        for artista in self._model.lista_artisti_album:
            opzioni.append(ft.dropdown.Option(artista[1]))
        self._view.ddArtist.options = opzioni
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato: {len(self._model._graph.nodes)} nodi (artisti), {len(self._model._graph.edges)} archi")
        )
        self._view.ddArtist.disabled = False
        self._view.btnArtistsConnected.disabled = False
        self._view.btnSearchArtists.disabled = False
        self._view.txtMinDuration.disabled = False
        self._view.txtMaxArtists.disabled = False
        self._view.update_page()

    def handle_connected_artists(self, e):
        artista_selezionato = self._view.ddArtist.value
        if artista_selezionato is None:
            self._view.show_alert("Inserire un artista dal dropdown")
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Artisti direttamente collegati all'artista: {artista_selezionato}, {len(self._model.get_artisti_collegati(artista_selezionato))}")
        )
        vicini_tupla = self._model.get_artisti_collegati(artista_selezionato)
        for v in vicini_tupla:
            self._view.txt_result.controls.append(
                ft.Text(f"{v[1]} - Numero di generi in comune: {v[0]}")
            )
        self._view.update_page()



