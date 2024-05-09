# ZDO - SP
# Ondrej Valtr
# posledni uprava: 2. 5. 2024

import numpy as np
from modulmaska import vytvor_masku
from skimage.transform import rotate

def zjisti_smer(imShape, spek):
  """
  metoda pro nalezeni smeru nejvetsich hodnot poskytnuteho frekvencniho spektra:
  nejprve vytvori obdelnikovou masku ve smeru vertikalni (kratsi) osy (0˚)
  pote s krokem 5°: <0; 175> vzdy obdelnik o dany uhel rotuje a vytvorenou maskou pronasobi predane spektrum
  nasledne vybere uhel pro nejvetsi odezvu

  vstupni parametry: imShape - image.shape - rozmery obr.
                     spek - frekvencni spektrum
  vystup: uhel - ve [˚]
  """

  center = (int(imShape[0]/2), int(imShape[1]/2)) # bod, misto pro rotaci
  suma =  np.zeros(36) # pole pro sumy hodnot bodu zbylych po pronasobeni
  # spektra maskou (obdelnikem orotovanym o dany uhel; 180/5 = 36)
  maskaR = vytvor_masku(90, imShape, delkaRel=1) # referencni maska, urcuje velikost rotovaneho obdelniku
  suma[0] = np.sum(maskaR*spek)
  for i in range(35):
    imR = rotate(maskaR, 5*(i+1), True, center)

    # nasleduje uprava velikosti imR na rozmery puvodniho obr.:
    # pokud je imR vetsi, krajni nulove hodnoty se "zahodi"
    pocatek = (int((imR.shape[0] - imShape[0])/2),int((imR.shape[1] - imShape[1])/2))
    imR = imR[pocatek[0]:pocatek[0]+imShape[0], pocatek[1]:pocatek[1]+imShape[1]]

    # pokud je imR v dane ose mensi, kraje se vyplni nulami
    if imR.shape[0] < imShape[0]:
      imR = np.pad(imR, pad_width=((int((imShape[0]-imR.shape[0])/2), int((imShape[0]-imR.shape[0])/2)), (0,0)))
      if imR.shape[0] != imShape[0]:
        imR = np.pad(imR, pad_width=((0,1),(0,0)))
    if imR.shape[1] < imShape[1]:
      imR = np.pad(imR, pad_width=((0,0), (int((imShape[1]-imR.shape[1])/2), int((imShape[1]-imR.shape[1])/2))))
      if imR.shape[1] != imShape[1]:
        imR = np.pad(imR, pad_width=((0,0), (0, 1)))
        
    suma[i+1] = np.sum(imR*spek) # aplikovani masky a secteni hodnot

  index = suma.argmax()
  uhel = 5*index
  return uhel
 
