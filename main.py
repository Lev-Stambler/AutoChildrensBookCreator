from fpdf import FPDF
import requests 
import urllib.parse
from google_images_download import google_images_download
import glob, os
from PIL import Image
import random
import wikipedia
import urllib.parse

adjunctKeyword = " particle physics"
sentenceBuilder =[["Then", "Hence forth", "After that", "Thereafter", "Later", "Like a coolio", "After--for the fun of PHYSICS--"], ["Jumbo", "the physics student", "Mr. Feynminster"], ["went to see the", "explored the", "saw the", "learned about the"]]

def getImage(keyword, limit=2):
  argumnets = {
    "keywords": keyword,
    "limit": limit,
    "print_urls": False
  }
  response = google_images_download.googleimagesdownload()
  imageURL = response.download(argumnets)

def downloadImages(keywords):
  for keyword in keywords:
    getImage(keyword + adjunctKeyword)
  wordLen = len(keywords)  
  getImage("magic school bus", limit=wordLen)

def randBackColorGen():
  return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] 

def getColorInverse(r, g, b):
  if ((r + g + b) / 3) > 127:
    return [0, 0, 0]
  return [255, 255, 255]

def getDefinition(word):
  # replace stops errs
  encoded = wikipedia.summary(word).replace('–', '-').encode('ascii', 'replace')
  return encoded.decode("ascii").replace('?', '-').split('.')[0]

def buildPageTxt(keyWords):
  txts = []
  count = 0
  for keyword in keyWords:
    starterWord = ''
    if count is 0:
      starterWord = 'We start with a student'
    else:
      starterWord = sentenceBuilder[0][count % len(sentenceBuilder[0])]
    sentence = "{}, {} {} {} ({})".format(starterWord, sentenceBuilder[1][count % len(sentenceBuilder[1])], sentenceBuilder[2][count % len(sentenceBuilder[2])], keyword, getDefinition(keyword))
    charsPerLine = 80
    if len(sentence) > charsPerLine:
      sentSplit = []
      lenTot = 0
      while lenTot < len(sentence):
        lenEnd = lenTot+charsPerLine
        if lenEnd > len(sentence):
          lenEnd = len(sentence)
        nonWordSplit = sentence[lenTot:lenEnd]
        words = nonWordSplit.split(' ')
        lastSpace = nonWordSplit.find(' ', (len(nonWordSplit) - len(words[len(words) - 1]) - 1))
        print(lastSpace, len(nonWordSplit))
        if lastSpace <= 0 or lastSpace > len(nonWordSplit) - 15:
          lastSpace = len(nonWordSplit)
        sentSplit.append(nonWordSplit[0:lastSpace])
        lenTot += lastSpace
      txts.append(sentSplit)
    else:
      txts.append([sentence])
    count += 1
  return txts

def getMagicSchoolBusPaths():
  paths = []
  dir = 'downloads/magic school bus'
  for file in os.listdir(dir):
    path = os.path.join(dir, file)
    if file.endswith(".jpg"):
      paths.append(path)
    elif file.endswith(".png"): # todo put back in on refresh
      im = Image.open(path)
      rgb_im = im.convert('RGB')
      width, height = im.size
      rgb_im.save(path + '.jpg')
      paths.append(path + '.jpg')
  return paths

def generatePdf(keywords):
  mbPaths = getMagicSchoolBusPaths()
  txts = buildPageTxt(keywords)
  pdf = FPDF()
  pageNumb = 0
  for keyword in keywords:
    pdf.add_page()
    pdf.set_line_width(1)
    color = randBackColorGen()
    # create color
    pdf.set_fill_color(*color)
    pdf.rect(-5, -5, 1000, 2000, "DF")
    inverseColor = getColorInverse(*color)
    pdf.set_text_color(*inverseColor)
    pdf.set_font("Arial", size=20)
    pdf.cell(200, 10, txt=keyword.title(), ln=1, align="C")
    dir = './downloads/' + keyword + adjunctKeyword
    offsetY = 0
    try:
      im = Image.open(mbPaths[pageNumb])
      width, height = im.size
      imgHeight = 40
      pdf.image(mbPaths[pageNumb], x=random.randint(100, 150), y=60, w=imgHeight)
      offsetY = 70 + height * (imgHeight / width)
    except:
      offsetY = 70
    offsetX = 20
    for file in os.listdir(dir):
      path = os.path.join(dir, file)
      if file.endswith(".jpg"):
        try:
          im = Image.open(path)
          width, height = im.size
          pdf.image(path, x=offsetX, y=offsetY, w=100)
          offsetY += 20 + height * (100 / width)
        except:
          print("error with jpg file shtuff")
      elif file.endswith(".png"): # todo put back in on refresh
        im = Image.open(path)
        rgb_im = im.convert('RGB')
        width, height = im.size
        rgb_im.save(path + '.jpg')
        pdf.image(path + '.jpg', x=offsetX, y=offsetY, w=100)
        offsetY += 20 + height * (100 / width)
      offsetX += 20
    pdf.set_font("Arial", size=12)
    for txtSnip in txts[pageNumb]:
      pdf.cell(200, 13, txt=txtSnip, ln=1, align="L")
      pdf.ln(1)
    pageNumb += 1
  pdf.output("simple_demo.pdf")

def main():
  keywords = [
    "antibaryon", "antiparticle", "baryon", "boson", "bottom quark", "charm quark", "delta resonance baryon", "down quark"
    , "electron", "electron neutrino", "eta-c meson", "eta resonance meson", "fermion", "gluon", "kaon", "k-star resonance meson",
    "lambda baryon", "lambda resonance baryon", "leptons", "meson", "muon", "muon neutrino", "N resonance baryon", "neutron", 
    "omega baryon", "omega resonance baryon", "omega resonance", "particle", "phi resonance meson", "photon", "pion", "proton",
    "quark", "rho meson", "rho resonance", "sigma", "strange (quark)", "tau fermion", "tau neutrino", "top (quark)", 
    "up (quark)", "W boson", "xi baryon", "Z-zero boson"
  ]
  # downloadImages(keywords)
  generatePdf(keywords)

main()
