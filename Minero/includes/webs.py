#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "altsys"
__license__ = "GNU General Public License v3.0"
__version__ = "0.0.03"
__email__ = "info@altsys.es"

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
from bs4 import BeautifulSoup
import re
#from lxml.html.clean import Cleaner


class Webs():
    def __init__(self):
        pass

    def clean_html(self, html):

        for data in html(['style', 'script', 'noscript', 'footer', 'meta', 'code', 'button', 'header', 'img', 'nav',
                          {'class': 'aawp', 'class': 'snippet-box', 'class': 'entry-related',
                           'id': 'comments', 'class': 'social-share_box', 'class': 'author-box',
                           'class': 'entry-comments', 'class': 'footer-widgets', 'class': 'site-header'}]):
            # Remove tags
            data.decompose()

        return html

    def clean_text(self, pretexts):
        # Make lower
        text = pretexts.lower()

        # Remove line breaks
        text = re.sub(r'\n\n\n', '', text)

        return text

    # Analizar la pagina web
    def scraping(self, source):
        paragraphs = []
        titleweb = ""
        datahtml = source
        dataText = self.clean_html(datahtml)
        dataFormat = self.clean_text(dataText.text.strip())

        for title in source.find_all('title'):
            titleweb = title.text

        paragraphs.append([titleweb, dataFormat,])

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
