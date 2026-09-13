import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._sceltaCategory = None
        self._nodoStart = None
        self._nodoEnd = None

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

        self._popolaDDNodo()
        self._view.update_page()

    def handleBestProdotti(self, e):
        if self._model.getAllNodi() == []:
            self._view.create_alert("Crea prima il grafo!")
            return

        try:
            listaProdotti = self._model.getBestProduct(5)
        except Exception as errore:
            self._view.create_alert(f"Errore: {errore}")
            return

        self._view.txt_result.controls.append(ft.Text("I cinque prodotti più venduti sono: "))
        for nodo, bilancio in listaProdotti:
            self._view.txt_result.controls.append(ft.Text(f"{nodo.product_name} with score {bilancio}"))

        self._view.update_page()

    def _popolaDDNodo(self):
        self._view._ddProdStart.options.clear()
        self._view._ddProdEnd.options.clear()

        for nodo in self._model.getAllNodi():
            opzione_dropdown_nodoStart = ft.dropdown.Option(data=nodo, text=str(nodo.product_name), on_click = self._pickNodoStart)
            opzione_dropdown_nodoEnd = ft.dropdown.Option(data=nodo, text=str(nodo.product_name), on_click= self._pickNodoEnd)
            self._view._ddProdStart.options.append(opzione_dropdown_nodoStart)
            self._view._ddProdEnd.options.append(opzione_dropdown_nodoEnd)
        self._view._ddProdStart.disabled = False
        self._view._ddProdEnd.disabled = False
        self._view.update_page()

    def _pickNodoStart(self, e):
        self._nodoStart = e.control.data

    def _pickNodoEnd(self, e):
        self._nodoEnd = e.control.data

    def handleCercaCammino(self, e):
        if self._nodoStart is None or self._nodoEnd is None:
            self._view.create_alert("Seleziona sia il nodo di partenza che quello di arrivo!")
            return

        strLun = self._view._txtInLun.value
        if strLun is None or strLun.strip() =="":
            self._view.create_alert("Inserisci la lunghezza del cammino")
            return

        lun = int(strLun)
        if lun <= 0:
            self._view.create_allert("La lunghezza deve essere positiva")
            return

        camminoOttimo, pesoOttimo = self._model.getCamminoOttimo(
            self._nodoStart.product_id, self._nodoEnd.product_id, lun)

        print(f"Sono arrivato prima e il cammino ottimo è -> {camminoOttimo}")
        if camminoOttimo is None:
            self._view.create_alert("Non esiste un cammino di questa lunghezza tra i due nodi!")
            return
        print("Sono arrivato dopo")
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Cammino Ottimo (peso {pesoOttimo})"))
        for nodo in camminoOttimo:
            self._view.txt_result.controls.append(ft.Text(str(nodo)))

        self._view.update_page()


    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
