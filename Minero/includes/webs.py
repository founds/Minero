#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "altsys"
__license__ = "GNU General Public License v3.0"
__version__ = "0.0.02"
__email__ = "info@altsys.es"

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import os
import re
from bs4 import BeautifulSoup


class Webs():
    def __init__(self):
        pass

    # Analizar la pagina web
    def scraping(self, source):
        tags = []
        links = []
        formatted_article_text = ""
        try:
            url = source.find("meta", property="og:url")["content"]
            pre_tags = source.find_all("meta", property="article:tag")
            paragraphs = source.findAll('p')

            article_text = ""

            for p in paragraphs:
                article_text += p.text

            # Removing Square Brackets and Extra Spaces
            article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
            article_text = re.sub(r'\s+', ' ', article_text)

            # Removing special characters and digits
            # formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
            formatted_article_text = re.sub(r'\s+', ' ', article_text)

            for tag in pre_tags:
                tags.append(tag["content"])

            # Detectar todas las URLS
            for link in source.find_all('a', href=True):
                links.append(link['href'])
        except:
            tags.append('')
            url = ""
            links.append('')

        return tags, url, links, formatted_article_text

    # Conectar con la fuente
    def connect(self, web):
        try:
            # Quitar los warnings de HTTPS no verificados
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

            # si no hay enlace a youtube descargar texto
            if "youtube" not in web:
                # con , verify=False nos saltamos la verificación ssl
                # timeout=20 dar un timeout a los 20 segundos
                response = requests.get(web, time.sleep(5), verify=False, timeout=10, allow_redirects=False)

                if response.status_code == 200:
                    print("URL a Analizar: ", web)
                    texto = BeautifulSoup(response.text, "html.parser")

                    tags, web, links, parrafos = self.scraping(texto)

                    return parrafos
            else:
                print("youtube")

        except:
            pass