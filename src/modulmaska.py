# ZDO - SP
# Ondrej Valtr
# posledni uprava: 2. 5. 2024

import numpy as np
from math import pi

def vytvor_masku(uhel, imShape, delkaRel=0.5):
  """
  metoda pro vytvoreni masky obdelnikoviteho tvaru pro zachovani chtenych frekvenci (koeficentu spektra)
  vstupni parametry: uhel - uhel natoceni masky ve [˚], 0° - obdelnik rovnobezny s horizontalni osou
                     imShape - image.shape - rozmery obr.
                     delkaRel - delka "obdelniku" pro dany smer zadany v parametru uhel;
                                <0; 1>: 1 maximalni mozna delka "obdelniku" vzhledem k imShape
  vystup: maska - 2D numpy array: hodnoty 0 a 1 (v miste vytvoreneho obdelnikoviteho utvaru)
  """


  maska = np.zeros(imShape)
  center = (int(imShape[0]/2), int(imShape[1]/2)) # bod, misto "rotace"!
  aPul = 2 # (priblizna) sirka "obdelniku"

  # trivialni pripad pro 90° osetren zvlast
  if uhel == 90:
    bPul = int(imShape[0]*(delkaRel/2))
    maska[center[0]-bPul:center[0]+bPul, center[1]-aPul:center[1]+aPul] = 1

  # trivialni pripad pro 0° osetren zvlast
  elif uhel == 0:
    bPul = int(imShape[1]*(delkaRel/2))
    maska[center[0]-aPul:center[0]+aPul, center[1]-bPul:center[1]+bPul] = 1

  else:
    # tvorba primky (usecky) se zadanym uhlem natoceni
    alfa = uhel * pi / 180 # prevod uhlu na rad
    k = np.tan(alfa) # smernice k: i = k*j
    j = np.arange(maska.shape[1]) - int(maska.shape[1]/2)
    i = k*j
    i = np.round(i).astype(int)
    # souradny system j i (nikoliv x y)
    i = np.flip(i+center[0])
    indexy = np.where(((i<imShape[0]) & (i>=0)))
    i = i[indexy]
    j = j + center[1]
    j = j[indexy]
    maska[i,j] = 1

    # pri tomto principu tvorby primky vznikaji pro strme primky velke mezery, diry
    # cast kodu pro zaplneni mezer, vysledek souvisla usecka
    lenj = len(j)
    n = 0
    p = 0
    for k in range(lenj-2):
      p = p + n + 1
      n = 0
      dira = np.abs(i[p] - i[p+1])
      zn = np.sign(i[p] - i[p+1])
      iv = []
      for l in range(dira-1):
        j = np.insert(j, p, j[p])
        iv.append(i[p]+zn*(-l-1))
        n = n + 1
      i = np.insert(i, p+1, iv)

    # cast kodu pro omezeni, zkraceni usecky dle zadane relativni delky
    x = np.nonzero(maska[0])
    podm = x[0].size
    l = 0
    while podm < 1:
      l = l + 1
      x = np.nonzero(maska[l])
      podm = x[0].size
    r = np.linalg.norm((np.array((0,x[0][0])) - np.array(center))) * delkaRel
    indexy = []
    for k in range(len(i)):
      p1 = np.array((i[k],j[k]))
      dist = np.linalg.norm(p1 - np.array(center))
      if dist < r:
        indexy.append(k)
    i = i[indexy]
    j = j[indexy]
    maska = np.zeros(imShape)
    maska[i,j] = 1

    # tvorba obdelnikoviteho utvaru z vytvorene usecky:
    # pro kazdy bod usecky (mimo prvni a posledni 2 body) pridany v matici
    # masky dalsi 2 body dolu, nahoru, doprava, doleva
    for k in range(len(j)-4):
      k = k + 2
      for l in range(5):
        l = l - 2
        maska[i[k]+l, j[k]] = 1
        maska[i[k], j[k]+l] = 1

  return maska
 
