from fpdf import FPDF
import requests 
import urllib.parse
from google_images_download import google_images_download
import glob, os
from PIL import Image
import random

adjunctKeyword = " particle physics"

def getImage(keyword, limit=2):
  argumnets = {
    "keywords": keyword,
    "limit": limit,
    "print_urls": True
  }
  response = google_images_download.googleimagesdownload()
  imageURL = response.download(argumnets)
  print(imageURL)

def downloadImages(keywords):
  for keyword in keywords:
    getImage(keyword + adjunctKeyword)
  wordLen = len(keywords)  
  getImage("magic school bus", limit=wordLen)

def randBackColorGen():
  return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] 

def getColorInverse(r, g, b):
  return [225 - r, 255 - g, 255 - b]

def generatePdf(keywords):
  pdf = FPDF()
  for keyword in keywords:
    pdf.add_page()
    pdf.set_line_width(1)
    color = randBackColorGen()
    pdf.set_fill_color(*color)
    pdf.rect(-5, -5, 1000, 2000, "DF")
    inverseColor = getColorInverse(*color)
    pdf.set_text_color(*inverseColor)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=keyword, ln=1, align="C")
    dir = './downloads/' + keyword + adjunctKeyword
    offsetY = 50
    offsetX = 20
    for file in os.listdir(dir):
      path = os.path.join(dir, file)
      if file.endswith(".jpg"):
        im = Image.open(path)
        width, height = im.size
        pdf.image(path, x=offsetX, y=offsetY, w=100)
        offsetY += 20 + height * (100 / width)
      elif file.endswith(".png|||||"): # todo put back in on refresh
        im = Image.open(path)
        rgb_im = im.convert('RGB')
        width, height = im.size
        rgb_im.save(path + '.jpg')
        pdf.image(path + '.jpg', x=offsetX, y=offsetY, w=100)
        offsetY += 20 + height * (100 / width)
      offsetX += 20      
  pdf.output("simple_demo.pdf")

def main():
  keywords = [
    "antibaryon", "antiparticle", "baryon", "boson", "bottom (quark)", "charm (quark)", "delta resonance baryon", "down (quark)"
    #, "electron", "electron neutrino", "eta-c meson", "eta resonance meson", "fermion", "gluon", "kaon", "k-star resonance meson",
    # "lambda baryon", "lambda resonance baryon", "leptons", "meson", "muon", "muon neutrino", "N resonance baryon", "neutron", 
    # "omega baryon", "omega resonance baryon", "omega resonance", "particle", "phi resonance meson", "photon", "pion", "proton",
    # "quark", "rho meson", "rho resonance", "sigma", "strange (quark)", "tau fermion", "tau neutrino", "top (quark)", 
    # "up (quark)", "W boson", "xi baryon", "Z-zero boson"
  ]
  # downloadImages(keywords)
  generatePdf(keywords)

main()

# https://pixabay.com/api/?key=12695003-ba68960e9e3c4f78e821208ff&q=yellow+flowers&image_type=photo