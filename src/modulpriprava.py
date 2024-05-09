# ZDO - SP
# Ondrej Valtr

import numpy as np
import skimage
import copy

def priprav_data(skel1, skel2):
  """
  metoda pripravujici data pro spocteni stehu a pripadnou vizualizaci
  vstup: skel1 - skelet (bud rany nebo stehu) - 2D numpy array - hodnoty 1 nebo 0
         skel2 - skelet (bud rany nebo stehu, zalezi na tom, co je skel1)
  vystup: bodyRana  - seznam, jehoz prvni polozka je opet seznam souradnic bodu rany, ktery je nejvice nalevo,
                                    druha polozka je opet seznam souradnic bodu rany, ktery je nejvice napravo
          bodyStehy - seznam seznamu pro stehy, vnitrni seznam kazdeho stehu opet obsahuje
                      souradnice - seznam - krajnich bodu, tentokrate nejvice dole a nahore
  """

  # identifikace, ktery ze skeletonu skel1 a skel2 je rana, a ktery stehy:
  # nejcasteji ten skelet, ktery ma bod nejvice nalevo je rana
  yy, xx = np.nonzero(skel1)
  indx = np.argmin(xx)
  l_point1 = xx[indx], yy[indx]

  yy, xx = np.nonzero(skel2)
  indx = np.argmin(xx)
  l_point2 = xx[indx], yy[indx]

  # pokud ma skel2 krajni bod vice nalevo, jedna se pravdepodbne o ranu
  if l_point2[0] < l_point1[0]:
    pom = copy.deepcopy(skel1)
    skel1 = copy.deepcopy(skel2)
    skel2 = copy.deepcopy(pom)
  # odtud jiz skel1 skeleton rany a skel2 skeleton stehu

  bodyRana = []
  # krajni body rany urceny jako ten nejvice vlevo a ten nejvice vpravo:
  yy, xx = np.nonzero(skel1)
  indx = np.argmax(xx)
  r_point = xx[indx], yy[indx]
  indx = np.argmin(xx)
  l_point = xx[indx], yy[indx]
  bodyRana.append([[l_point[0],l_point[1]],[r_point[0],r_point[1]]])

  label = skimage.morphology.label(skel2,background=0) # stehy
  bodyStehy =[]
  for i in range(np.max(label)):
    steh = (label==(i+1)) # +1 kvuli pozadi
    z = np.nonzero(steh)
    # predpoklad toho, ze steh bude spise ve vertikalnim smeru, proto krajni body vybrany jako ty
    # nejvice dole a nahore
    #bodyStehy.append([[z[1][0],z[0][0]], [z[1][-1],z[0][-1]]])
    bodyStehy.append([[z[1][0]-1,z[0][0]], [z[1][-1],z[0][-1]+1]])
    # -1 a +1 z duvodu vykresleni: pokud ma steh a rana spolecny pouze krajni bod stehu, metoda
    # neurci, ze maji spolecny prunik: proto jemne rozsireni usecky stehu o 1 bod nahoru a dolu
    # (pouze aproximace: muze trochu zkreslit vysledny uhel sevreni, coz ale v teto uloze tolik nevadi)
    
  return bodyRana, bodyStehy
 
