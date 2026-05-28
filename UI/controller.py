import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        risultati = self._model.calcola_umidita_media(self._mese)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("L'umidita media del mese selezionato è :"))
        for localita, media in risultati.items():
            self._view.lst_result.controls.append(
                ft.Text(f"{localita}: {media}")
            )

        self._view.update_page()

    def handle_sequenza(self, e):
        mese = int(self._mese)

        sol, costo = self._model.calcola_sequenza(mese)

        self._view.lst_result.controls.clear()

        self._view.lst_result.controls.append(
            ft.Text(f"Costo minimo: {costo}")
        )

        for s in sol:
            self._view.lst_result.controls.append(
                ft.Text(
                    f"[{s.localita} - {s.data}] Umidita = {s.umidita}"
                )
            )

        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)
        print("VALUE:", e.control.value)

