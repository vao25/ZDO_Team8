# ZDO - SP 2024
# Ondrej Valtr
# spousteci skript

import skimage
import sys
import numpy as np

from hlavnimodul import zpracuj_obr
from modulpriprava import priprav_data
from modulvizualizace import spocti_stehy_viz
from modulvystup import zapis_vystup

nazvy = [] # seznam pro nazvy obrazku
poctyStehu = [] # seznam, kde na stejnem indexu jako v seznamu nazvy je odhadnuty pocet stehu v obr.
v = False # vizualizace (visual mode)
j = 0
nazevSouboru = sys.argv[1] # nazev vystupniho .csv souboru
if sys.argv[2] == "-v":
  v = True
  j = 1

# popis metod, jejich vstupnich parametru a vystupu vzdy v prislusnem modulu
for i in range(len(sys.argv)-2-j):
  print("Zpracovava se " + str(i+1) + ". obr.")
  obr = sys.argv[i+2+j]
  nazvy.append(obr)
  im = skimage.io.imread("images/"+obr, as_gray=True)
  imRGB = skimage.io.imread("images/"+obr)
  skel1, skel2, skel = zpracuj_obr(im)

  # pokud promenne nereprezentuji skeletony, pravdepodobne je v obr. 0 stehu
  if np.all(skel1==0) or np.all(skel2==0):
    poctyStehu.append(0)
    if v:
      plt.imshow(imRGB)
      plt.title('Počet stehů: ' + str(0))
      plt.show()
    continue

  bodyRana, bodyStehy = priprav_data(skel1, skel2)
  pStehu = spocti_stehy_viz(bodyRana, bodyStehy, v, imRGB)
  poctyStehu.append(pStehu)

zapis_vystup(nazvy, poctyStehu, nazevSouboru)
print("hotovo")
 
