# ZDO - SP
# Ondrej Valtr

import numpy as np
import skimage
import matplotlib.pyplot as plt
from scipy import ndimage
import copy

from modulmaska import vytvor_masku
from modulsmer import zjisti_smer


def zpracuj_obr(im):
  """
  hlavni metoda vykonavajici zadanou ulohu
  vstup: im - nacteny sedotonovy obrazek
  vystup: skel1 - skelet (bud rany nebo stehu) - 2D numpy array - hodnoty 1 nebo 0
          skel2 - skelet (bud rany nebo stehu, zalezi na tom, co je skel1)
          skel - vysledny skelet (rana se stehy)
  """

  prumerRef = 0.6881 # referencni jasovy prumer
  im2 = skimage.exposure.rescale_intensity(im, out_range=(0, 1))
  # jasovy rozdil obr. se zvysenym kontrastem a referencniho jasoveho prumeru:
  jasRozdil = np.mean(im2) - prumerRef
  im3 = im2 + jasRozdil # jasova korekce

  ft = np.fft.fft2(im3)
  ftshift = np.fft.fftshift(ft)
  spektrum = 20*np.log(np.abs(ftshift))

  uhel = zjisti_smer(im.shape, spektrum)
  # v metode zjisti_smer plati nulovy uhel pro vertikalni osu, kdezto v metode vytvor_masku pro horizontalni
  if uhel < 90:
    uhel = uhel + 90
  else:
    uhel = uhel - 90
  maska1 = vytvor_masku(uhel, im.shape)

  ftshift_mask = ftshift*maska1 # maskovani ziskanou maskou:
  # ponechani koeficientu (frekvenci) v "nejintenzivnejsim smeru"
  ftishift_back = np.fft.ifftshift(ftshift_mask)
  im_back = np.fft.ifft2(ftishift_back)
  im_back = np.abs(im_back) # obr. vznikly ponechanim pouze frekvenci z masky

  # segmentace v ziskanem obr. im_back pomoci metody Watershed:
  elevation_map = skimage.filters.sobel(im_back)
  plt.clf()
  a, b, c = plt.hist(im_back.ravel(), 255, cumulative=True, density=True) # vypocet kumulativniho histogramu
  # hledani prahu jasu pro markery pozadi - predp. velka cast obr., proto hodnota az 50%
  aPoz = np.where(a>0.5) # indexy (jasy pixelu) pro nez plati, ze jsou minimalne vyssi nez polovina jasu pixelu v obr.
  indPoz = aPoz[0][0] # hodnota jasu - pulka jasu v obr. je mensi (v tomto pripade tedy vysel median)
  # hledani prahu jasu pro markery Rany nebo Stehu - predp. mala cast obr., proto hodnota pouze 2.5%
  aRS = np.where(a<0.025) # indexy (jasy pixelu) pro nez plati, ze jejich hodnota je maximalne vetsi nez 2.5% hodnot jasu pixelu v obr.
  indRS = aRS[0][-1] # index (jas) 2.5%-kvantil v obr.
  markers = np.zeros_like(im_back)
  markers[im_back < b[indRS]] = 2 # "oznackovani" pixelu pro ranu nebo stehy
  markers[im_back > b[indPoz]] = 1 # "oznackovani" pixelu pozadi
  imSegm1 = skimage.segmentation.watershed(elevation_map, markers) - 1 # -1 proto, aby hodnota pozadi byla 0 a rany nebo stehu 1
  imSegm1 = ndimage.median_filter(imSegm1, 3) # filtrace sumu nebo malych segmentu, ktere nemuzou byt stehy
  skel1 = skimage.morphology.skeletonize(imSegm1)

  # cast pro nalezeni druheho skeletonu (rany nebo stehu)

  spektrumU = copy.deepcopy(spektrum)
  indexy = np.argwhere(maska1==1)
  spektrumU[indexy[:,0],indexy[:,1]] = np.min(spektrum) # zakryti jiz nalezene, nejvice intenzivni casti spektra (v podstate vyruseni)

  uhel2 = zjisti_smer(im.shape, spektrumU) # urceni smeru (uhlu) druhe "nejintenzivnejsi" casti spektra
  # v metode zjisti_smer plati nulovy uhel pro vertikalni osu, kdezto v metode vytvor_masku pro horizontalni
  if uhel2 < 90:
    uhel2 = uhel2 + 90
  else:
    uhel2 = uhel2 - 90
  maska2 = vytvor_masku(uhel2, im.shape)

  ftshift_mask2 = ftshift*maska2 # maskovani ziskanou maskou:
  # ponechani koeficientu (frekvenci) ve "2. nejintenzivnejsim smeru"
  ftishift_back2 = np.fft.ifftshift(ftshift_mask2)
  im_back2 = np.fft.ifft2(ftishift_back2)
  im_back2 = np.abs(im_back2) # obr. vznikly ponechanim pouze frekvenci po pouziti masky

  # segmentace v ziskanem obr. im_back2 pomoci metody Watershed:
  elevation_map2 = skimage.filters.sobel(im_back2)
  plt.clf()
  a, b, c = plt.hist(im_back2.ravel(), 255, cumulative=True, density=True) # vypocet kumulativniho histogramu
  # hledani prahu jasu pro markery pozadi - predp. velka cast obr., proto hodnota az 50%
  aPoz = np.where(a>0.5) # indexy (jasy pixelu) pro nez plati, ze jsou minimalne vyssi nez polovina jasu pixelu v obr.
  indPoz = aPoz[0][0] # hodnota jasu - pulka jasu v obr. je mensi (v tomto pripade tedy vysel median)
  # hledani prahu jasu pro markery Rany nebo Stehu - predp. mala cast obr., proto hodnota pouze 2.5%
  aRS = np.where(a<0.025) # indexy (jasy pixelu) pro nez plati, ze jejich hodnota je maximalne vetsi nez 2.5% hodnot jasu pixelu v obr.
  indRS = aRS[0][-1] # index (jas) 2.5%-kvantil v obr.
  markers2 = np.zeros_like(im_back2)
  markers2[im_back2 < b[indRS]] = 2 # "oznackovani" pixelu pro ranu nebo stehy
  markers2[im_back2 > b[indPoz]] = 1 # "oznackovani" pixelu pozadi
  imSegm2 = skimage.segmentation.watershed(elevation_map2, markers2) - 1 # -1 proto, aby hodnota pozadi byla 0 a rany nebo stehu 1
  imSegm2 = ndimage.median_filter(imSegm2, 3) # filtrace sumu nebo malych segmentu, ktere nemuzou byt stehy
  skel2 = skimage.morphology.skeletonize(imSegm2)
  skel = skel1 + skel2 # spojeni skeletu rany a stehu

  # filtrace vetsich segmentu, ktere ale neprotinaji ranu a nejsou tedy stehy
  label = skimage.morphology.label(skel,background=0)
  props = skimage.measure.regionprops(label+1)
  maxSkel = 1 # label nejvetsiho (zhlediska poctu bodu) skeletu
  # identifikace nejvetsiho skeletu, tedy nejpravdepodobneji utvaru reprezentujici ranu se stehy:
  for i in range(np.max(label)):
    if props[i+1].area > props[maxSkel].area:
      maxSkel = i+1
  skel = label[0] + label[maxSkel] # do vysledneho skeletu bran pouze ten nejvetsi
  skel = np.zeros(im.shape)
  skel[np.where(label==maxSkel)] = 1
  # filtrace i samostatnych skeletonu - rany a stehu zvlast:
  skel1 = skel1 * skel
  skel2 = skel2 * skel

  return skel1, skel2, skel
 
