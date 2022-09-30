#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "altsys"
__license__ = "GNU General Public License v3.0"
__version__ = "0.0.04"
__email__ = "info@altsys.es"

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
from bs4 import BeautifulSoup
from PIL import Image
import re
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


class Webs():
    def __init__(self):
        pass

    # Buscar en google
    def buscar_google(self, query, num, lang):
        webs = []
        for j in search(query, tld="co.in", num=num, stop=num, pause=3):
            if "youtube" not in j:
                webs.append(j)

        return webs

    def clean_html(self, html):
        for data in html(['a[href^="mailto:"]', 'style', 'script', 'noscript', 'footer', 'meta', 'code', 'button',
                          'header', 'img', 'nav', {'class': 'aawp', 'class': 'snippet-box', 'class': 'entry-related',
                           'id': 'comments', 'class': 'social-share_box', 'class': 'author-box',
                           'class': 'entry-comments', 'class': 'footer-widgets', 'class': 'site-header',
                           'id': 'toc_container', 'class': 'tags', 'class': 'related_articles',
                           'class': 'kk-star-ratings'}]):
            # Remove tags
            data.decompose()

        return html

    def clean_text(self, pretexts):
        # Make lower
        text = pretexts.lower()

        # Remove line breaks
        text = re.sub(r'\n\n', '', text)

        # Remove symbols
        symbols = r'[,;.:¡!¿?@#$%&[\](){}<>~=+\-*/|\\_^`"\']'
        texto = re.sub(symbols, ' ', text)

        # dígits [0-9]
        text = re.sub('\d', ' ', text)

        # tildes y diacríticas
        text = re.sub('á', 'a', text)
        text = re.sub('é', 'e', text)
        text = re.sub('í', 'i', text)
        text = re.sub('ó', 'o', text)
        text = re.sub('ú', 'u', text)
        text = re.sub('ü', 'u', text)
        text = re.sub('ñ', 'n', text)
        text = re.sub('δ', 'o', text)

        return text

    # Analizar la pagina web
    def scraping(self, source):
        paragraphs = []
        titleweb = ""
        datahtml = source
        dataText = self.clean_html(datahtml)
        dataFormat = self.clean_text(dataText.text.strip())

        # Title
        for title in source.find_all('title'):
            if title.text is not None:
                titleweb = title.text
                titleweb = titleweb.lstrip()
            else:
                titleweb = "No se ha podido obtener el titulo de la web."

        paragraphs.append([titleweb, dataFormat, ])

        return paragraphs

    # Conectar con la fuente
    def connect(self, web):
        # Quitar los warnings de HTTPS no verificados
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        headers = requests.utils.default_headers()

        headers.update(
            {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/51.0.2704.103 Safari/537.36',
            }
        )

        # si no hay enlace a youtube descargar texto
        if "youtube" not in web:
            try:
                response = requests.get(web, time.sleep(5), verify=False, timeout=10, allow_redirects=False,
                                        headers=headers)

                if response.status_code == 200:
                    print("URL a Analizar: ", web)
                    source = BeautifulSoup(response.content, "html.parser")

                    data = self.scraping(source)

                    for items in data:
                        title = items[0]
                        textos = items[1]

                    return title, textos

            except requests.exceptions.Timeout:
                pass
                return web, "timeout"
