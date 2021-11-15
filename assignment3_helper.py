#!/usr/bin/env python
#Creative Computing 2021
#RTS, updated Nov 9, 2021
#-------------------------
import os, sys
import numpy
import math, random
from matplotlib import pyplot
import io as iio
from PIL import Image
from skimage import io
from datetime import datetime
import pytz

from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import requests 

import nltk

nltk.download('punkt')
nltk.download("stopwords")
nltk.download('averaged_perceptron_tagger')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words("english"))

from wordcloud import WordCloud, STOPWORDS
#---------------------------------------------------------
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True
    
#-------------------------------------------------------
def get_subdomains(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    term = 'https'
    alist = []
    subdomains = []
    for tag in soup.find_all('a', href=True):
        text = tag['href']
        if(text.find(term) != -1):
            alist.append(text)

    [subdomains.append(x) for x in alist if x not in subdomains]
    return(subdomains)

#--------------------------------------------------------
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return (u" ".join(t.strip() for t in visible_texts))
    
#---------------------------------------------------------
# Text filter function; filter based on some conditions
def filter_words(x):
    # Not in common English words
    cond_1 = x.lower() not in stop_words
    # Not a number
    cond_2 = not x.isnumeric()
    # Length of at least 3
    cond_3 = len(x)>2
    return (cond_1 and cond_2 and cond_3)
    
#--------------------------------------------------------

def create_random_collage(width, height, listofimages, factor):
    thumbnail_width = int(width/factor)
    thumbnail_height = int(height/factor)
    size = thumbnail_width, thumbnail_height
    new_im = Image.new('RGB', (width, height))
    ims = []

    for url in listofimages:
        response = requests.get(url)
        im = Image.open(iio.BytesIO(response.content))
        im.thumbnail(size)
        #add some image manipulation if you like
        ims.append(im)

    n = len(listofimages)
    i = 0
    for i in range(1, n):
        x = random.randint(thumbnail_width, (width-thumbnail_width))
        y = random.randint(thumbnail_height, (height-thumbnail_height))
        new_im.paste(ims[i], (x, y))
        i = i+1
        
    return(new_im)
    
#--------------------------------------------------------------------------
def create_collage(cols, rows, width, height, listofimages, show_positions):
    thumbnail_width = width//cols
    thumbnail_height = height//rows
    size = thumbnail_width, thumbnail_height
    new_im = Image.new('RGB', (width, height))
    ims = []

    for url in listofimages:
        response = requests.get(url)
        im = Image.open(iio.BytesIO(response.content))
        im.thumbnail(size)
        #add some image manipulation if you like
        ims.append(im)
    i = 0
    x = 0
    y = 0
    for col in range(cols):
        for row in range(rows):
            if(show_positions):
              print(i, x, y)
            new_im.paste(ims[i], (x, y))
            i += 1
            y += thumbnail_height
        x += thumbnail_width
        y = 0
        
    return(new_im)
    
#----------------------------------------------------------------
def get_unique_images(url, imagetype):
    images = []
    unique_images = []
    #get all images of imagetype (.png or .jpg from a url)
    htmldata = getdata(url) 
    soup = BeautifulSoup(htmldata, 'html.parser') 
    for item in soup.find_all('img'):
        if((str(item['src'])).endswith(imagetype)):
            images.append(item['src'])

    #remove duplicates
    [unique_images.append(x) for x in images if x not in unique_images]

    return(unique_images)
#----------------------------------------------------------------
#get data from a url  
def getdata(url): 
    r = requests.get(url) 
    return (r.text) 
    
#-----------------------------------------------------------------
def create_wordcloud(token_text, xdim, ydim, rstate, contourcolor, contourwidth, apply_mask, maskname, save_fig, savename):
    
    wordcloud = ''
    
    if(apply_mask == False):
        wordcloud = WordCloud(width=xdim,height=ydim,random_state=rstate,contour_width=contourwidth,contour_color=contourcolor).generate(" ".join(token_text))
    
    else:
        img = Image.open(maskname)
        img = img.resize((xdim, ydim),Image.ANTIALIAS) 
        wave_mask = numpy.array(img)
        wordcloud = WordCloud(width=xdim, height=ydim, mask=wave_mask, random_state=rstate,  contour_width=contourwidth, contour_color=contourcolor).generate(" ".join(token_text))
    
    if(save_fig):
        image = wordcloud.to_image()
        quality_val = 100
        image.save(savename, 'JPEG', quality=quality_val)
        
        
    return(wordcloud)
    
#-----------------------------------------------------------------
def create_timestamp(location):
    tz = pytz.timezone(location)
    now = datetime.now(tz)
    current_time = now.strftime("%d-%m-%Y-%H-%M")
    return(current_time)   
    
#-----------------------------------------------------------------