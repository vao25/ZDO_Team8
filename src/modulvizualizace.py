# ZDO - SP
# Ondrej Valtr


import numpy as np
import matplotlib.pyplot as plt
from modulprunik import intersectLines

def spocti_stehy_viz(bodyRany, bodyStehy, v, im):
  '''
  upravena metoda poskytnuta k zadani SP na urceni poctu stehu a pripadnou vizualizaci
  vstup: bodyRany - seznam, jehoz prvni polozka je opet seznam souradnic bodu rany, ktery je nejvice nalevo,
                                  druha polozka je opet seznam souradnic bodu rany, ktery je nejvice napravo
         bodyStehy - seznam seznamu pro stehy, vnitrni seznam kazdeho stehu opet obsahuje
                     souradnice - seznam - krajnich bodu, tentokrate nejvice dole a nahore
         v - boolean - pokud True, vykresli vysledky (visual mode)
         im - zadany obr. s ranou a stehy
  vystup: pStehu - odhadnuty pocet stehu v obr.
  '''

  incisions = np.array(bodyRany)
  stitches = np.array(bodyStehy)
  
  ############
  incision_alphas = []
  incision_lines = []
  for incision in incisions:
      for (p_1, p_2) in zip(incision[:-1],incision[1:]):
          p1 = np.array(p_1)
          p2 = np.array(p_2)
          dx = p2[0]-p1[0]
          dy = p2[1]-p1[1]
          if dy == 0:
              alpha = 90.0
          elif dx == 0:
              alpha = 0.0
          else:
              alpha = 90 + 180.*np.arctan(dy/dx)/np.pi
          incision_alphas.append(alpha)
          incision_lines.append([p1, p2])

  stitche_alphas = []
  stitche_lines = []
  for stitche in stitches:
      for (p_1, p_2) in zip(stitche[:-1],stitche[1:]):
          p1 = np.array(p_1)
          p2 = np.array(p_2)
          dx = p2[0]-p1[0]
          dy = p2[1]-p1[1]
          if dy == 0:
              alpha = 90.0
          elif dx == 0:
              alpha = 180.0
          else:
              alpha = 90 + 180.*np.arctan(dy/dx)/np.pi
          stitche_alphas.append(alpha)
          stitche_lines.append([p1, p2])


  ###############
  # analyze alpha for each pair of line segments
  intersections = []
  intersections_alphas = []
  pStehu = 0 # oproti originalu pridana promenna pro pocet stehu
  for (incision_line, incision_alpha) in zip(incision_lines, incision_alphas):
      for (stitche_line, stitche_alpha) in zip(stitche_lines, stitche_alphas):

          p0, p1 = incision_line
          pA, pB = stitche_line
          (xi, yi, valid, r, s) = intersectLines(p0, p1, pA, pB)
          if valid == 1:
              intersections.append([xi, yi])
              alpha_diff = abs(incision_alpha - stitche_alpha)
              alpha_diff = 180.0 - alpha_diff if alpha_diff > 90.0 else alpha_diff
              alpha_diff = 90 - alpha_diff
              intersections_alphas.append(alpha_diff)
              pStehu = pStehu + 1


  # visualize
  if v:
    plt.imshow(im)
    plt.title('Přibližná pozice rány a stehů; počet stehů: ' + str(pStehu))

    # vyznaceni rany
    for p_i in incisions:
      p = np.array(p_i)
      plt.plot(p[:,0], p[:,1])
    # vyznaceni stehu
    for p_s in stitches:
      p = np.array(p_s)
      plt.plot(p[:,0], p[:,1])

    for ((xi,yi), alpha) in zip(intersections, intersections_alphas):
        plt.plot(xi, yi, 'o')
        plt.text(xi, yi,'{:2.1f}'.format(alpha), c='green', bbox={'facecolor': 'white', 'alpha': 1.0, 'pad': 1}, size='large')

    plt.show()

  return pStehu 
