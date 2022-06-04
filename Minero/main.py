#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "altsys"
__license__ = "GNU General Public License v3.0"
__version__ = "0.0.04"
__email__ = "info@altsys.es"

import os
from googlesearch import search


class GMM:
    def __init__(self):
        if not os.path.exists('Dataset'):
            os.mkdir('Dataset')

        self.path_work = 'Dataset/pre/'

    # Buscar en google
    def buscar_google(self, query, num, lang):
        return search(query, num_results=num, lang=lang)

    # Obtencion de urls
    def get_urls(self, keys=[], prefixs=[], subfixs=[]):
        for key in keys:
            # limpiar keyword
            key = key.strip()

            if not os.path.exists(self.path_work + key):
                print('Proyecto creado: ', key)
                os.makedirs(self.path_work + key)

            if not os.path.exists(self.path_work + key + '/urls'):
                with open(self.path_work + key + '/urls', 'w') as f:
                    f.write("")
                    f.close()

                with open(self.path_work + key + '/urls-ko', "w") as f:
                    f.write("")
                    f.close()

                with open(self.path_work + key + '/urls-ok', "w") as f:
                    f.write("")
                    f.close()

            for prefix in prefixs:
                for subfix in subfixs:
                    try:
                        urls = self.buscar_google(prefix + " " + key + " " + subfix, 5, "es")
                        newurls = 0

                        with open(self.path_work + key + '/urls', "r") as tf:
                            lines = tf.read().split('\n')
                            tf.close()

                        with open(self.path_work + key + '/urls-ko', "r") as tf:
                            linesko = tf.read().split('\n')
                            tf.close()

                        with open(self.path_work + key + '/urls-ok', "r") as tf:
                            linesok = tf.read().split('\n')
                            tf.close()

                        for web in urls:
                            if web not in lines:
                                if web not in linesko:
                                    if web not in linesok:
                                        print("Pagina añadida: ", web)

                                        newurls += 1

                                        with open(self.path_work + key + '/urls', 'a') as f:
                                            f.write(web + os.linesep)
                                            f.close()
                    except:
                        print("¡¡¡Ha habido problemas para obtener las urls.!!!")
                        print("Listado resultado query:\n", urls)
                        print(type(urls))
                        print("Query: \n", web)

        print("Ha terminado la obtención de urls a explorar.")
        print("Nuevas urls añadidas: ", str(newurls))

    def process_urls(self, keys):
        from includes.webs import Webs

        for key in keys:
            # Cargar URLS
            if not os.path.exists(self.path_work + key + '/urls'):
                with open(self.path_work + key + '/urls', "w") as tf:
                    tf.write("")
                    tf.close()
            else:
                with open(self.path_work + key + '/urls', "r") as tf:
                    lines = tf.read().split('\n')
                    tf.close()

            numpages = 0

            if not os.path.exists(self.path_work + key + '/urls-ko'):
                with open(self.path_work + key + '/urls-ko', 'w') as f:
                    f.write("")
                    f.close()

            if not os.path.exists(self.path_work + key + '/urls-ok'):
                with open(self.path_work + key + '/urls-ko', 'w') as f:
                    f.write("")
                    f.close()

            if not os.path.exists(self.path_work + key + '/tmp'):
                os.mkdir(self.path_work + key + '/tmp')

            for url in lines:
                result = Webs().connect(url)
                numpages += 1

                if result is not None:

                    # Comprobar si ya existe el archivo a crear
                    if os.path.exists(self.path_work + key + '/tmp/' + str(numpages)):
                        numpages += 1

                    with open(self.path_work + key + '/tmp/' + str(numpages), 'w') as f:
                        f.write(result)
                        f.close()

                    with open(self.path_work + key + '/urls-ok', 'a') as f:
                        f.write(url + os.linesep)
                        f.close()

                else:
                    with open(self.path_work + key + '/urls-ko', 'a') as f:
                        f.write(url + os.linesep)
                        f.close()

                    # Descontamos 1 para que la key invalida no cuente
                    numpages -= 1

GMM().get_urls(
    keys=['Fresas', 'Tomates', 'Cebollas', 'Ajos'],
    prefixs=['Plantar', 'Sembrar'],
    subfixs=['Maceta', 'Jardineras'])

GMM().process_urls(
    keys=['Fresas', 'Tomates', 'Cebollas', 'Ajos'])
