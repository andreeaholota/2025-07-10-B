import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._sceltaCategory = None

    def fillDDCategories(self):
        for category in self._model.getCategories():
            id, nome = category
            opzione_dropdown = ft.dropdown.Option(data=id, text=nome, on_click=self._pickCategory)
            self._view._ddcategory.options.append(opzione_dropdown)

    def _pickCategory(self, e):
        self._sceltaCategory = e.control.data

    def handleCreaGrafo(self, e):
        if self._sceltaCategory is None:
            self._view.create_alert("Seleziona un filtro!")
            return

        d1 = self._view._dp1.value
        d2 = self._view._dp2.value

        if d1 is None or d2 is None:
            self._view.create_alert("Seleziona entrambe le date!")
            return
        if d1 > d2:
            self._view.create_alert("Start date deve essere <= End date!")
            return


        self._model.creaGrafo(self._sceltaCategory, d1, d2)


        numero_nodi = self._model.getNumVertici()
        numero_archi = self._model.getNumArchi()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi:{numero_nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi:{numero_archi}"))
        self._view.update_page()

    def handleBestProdotti(self, e):
        if self._model.getAllNodi() == []:
            self._view.create_alert("Crea prima il grafo!")
            return


        listaProdotti = self._model.getBestProduct(5)


        self._view.txt_result.controls.append(ft.Text("I cinque prodotti più venduti sono: "))
        for nodo, bilancio in listaProdotti:
            self._view.txt_result.controls.append(ft.Text(f"{nodo.product_name} with score {bilancio}"))

        self._view.update_page()

    def handleCercaCammino(self, e):
        pass



    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
