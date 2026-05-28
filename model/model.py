from database import meteo_dao

class Model:
    def __init__(self):
        self.cities = ["Milano", "Torino", "Genova"]

        self.best_sol = []
        self.best_cost = float("inf")

        self.meteo = {}

    def getAllSituazioni(self):
        return meteo_dao.MeteoDao.get_all_situazioni()

    def calcola_umidita_media(self, mese):
        lista_meteo = self.getAllSituazioni()
        somma = {m.localita: 0 for m in lista_meteo}
        conteggio = {m.localita: 0 for m in lista_meteo}
        for m in lista_meteo:
            if m.data.month == mese:
                somma[m.localita] += m.umidita
                conteggio[m.localita] += 1
        risultato = {}

        for loc in somma:
            risultato[loc] = somma[loc]/conteggio[loc]
        return risultato

    def calcola_sequenza(self, mese):
        self.best_sol = []
        self.best_cost = float("inf")

        self.meteo = self._build_meteo(mese)

        self._ricorsione(
            giorno=1,
            citta_attuale=None,
            consec=0,
            count={"Milano": 0, "Torino": 0, "Genova": 0},
            costo=0,
            sol=[]
        )

        return self.best_sol, self.best_cost

        # ------------------------------------
        # RICORSIONE
        # ------------------------------------

    def _ricorsione(self, giorno, citta_attuale, consec, count, costo, sol):

        # CASO BASE
        if giorno == 16:
            if costo < self.best_cost:
                self.best_cost = costo
                self.best_sol = sol.copy()
            return

        for citta in self.cities:

            # max 6 giorni
            if count[citta] == 6:
                continue

            # vincolo 3 giorni consecutivi
            if citta != citta_attuale and citta_attuale is not None:
                if consec < 3:
                    continue
                nuovo_consec = 1
            else:
                nuovo_consec = consec + 1

            # prendo situazione del giorno
            if giorno not in self.meteo:
                continue

            if citta not in self.meteo[giorno]:
                continue

            s = self.meteo[giorno][citta]

            nuovo_costo = costo + s.umidita

            # aggiorno stato
            count[citta] += 1
            sol.append(s)

            # ricorsione
            self._ricorsione(
                giorno + 1,
                citta,
                nuovo_consec,
                count,
                nuovo_costo,
                sol
            )

            # backtrack
            sol.pop()
            count[citta] -= 1

    def _build_meteo(self, mese):

        lista = self.getAllSituazioni()

        meteo = {}

        for s in lista:

            if s.data.month != mese:
                continue

            giorno = s.data.day

            if giorno not in meteo:
                meteo[giorno] = {}

            meteo[giorno][s.localita] = s

        return meteo
