# ZDO - SP
# Ondrej Valtr

import csv

def zapis_vystup(nazvy, pStehu, nazevSouboru):
  """
  metoda pro zapis vysledku do .csv souboru
  vstupni parametry: nazvy - seznam s nazvy obrazku
                     pStehu - seznam, kde na stejnem indexu jako v seznamu
                              nazvy je odhadnuty pocet stehu v obr.
                     nazevSouboru - do jakeho souboru se zapisou vysledky
  """

  hlavicka = ["filename", "n_stiches"]
  data = []
  for i in range(len(nazvy)):
    data.append([nazvy[i], pStehu[i]])

  with open(nazevSouboru, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(hlavicka)
    writer.writerows(data)
  print("Vysledek zapsan do souboru " + nazevSouboru)
