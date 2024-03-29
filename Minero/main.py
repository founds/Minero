#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "altsys"
__license__ = "GNU General Public License v3.0"
__version__ = "0.0.08"
__email__ = "info@altsys.es"

import sys
import os
from includes.tools import Tools
import configparser
from colorama import Fore
import argparse

BLUE = Fore.BLUE
RED = Fore.RED
GREEN = Fore.GREEN
RESET = Fore.RESET


class GMM:
    def __init__(self):
        self.path = os.path.abspath(os.path.dirname(sys.argv[0]))

        #print(f"{BLUE}Path de ejecución:{RESET} %s" % (self.path,))

        if not os.path.exists(self.path + '/config.cfg'):
            print(f"{RED}No existe el archivo de configuración.{RESET}")
            Tools().create_config(self.path + '/config.cfg', self.path + '/Dataset')

        config = configparser.ConfigParser()
        config.read(self.path + '/config.cfg')

        self.path_dataset = config.get('CONFIG', 'path_dataset')

        if not os.path.exists(self.path_dataset):
            os.mkdir(self.path_dataset)

        #print(f"{BLUE}Path del Dataset:{RESET} %s" % self.path_dataset)

    # Obtencion de urls
    def get_urls(self, keys=[], prefixs=[], subfixs=[], num_search=1):
        from includes.webs import Webs

        newurls = 0
        urlsok = 0
        urlsok2 = 0
        urlsko = 0

        path_work = self.path_dataset + "/pre/"

        for key in keys:
            # limpiar keyword
            key = key.strip()
            key = key.lower()

            if not os.path.exists(path_work + key):
                print(f"Proyecto creado: {GREEN}%s{RESET}" % key)
                os.makedirs(path_work + key)
                Tools().create_structure(path_work, key)

            with open(path_work + key + '/urls', "r") as tf:
                lines = tf.read().split('\n')
                tf.close()

            with open(path_work + key + '/urls-ko', "r") as tf:
                linesko = tf.read().split('\n')
                tf.close()

            with open(path_work + key + '/urls-ok', "r") as tf:
                linesok = tf.read().split('\n')
                tf.close()

            with open(path_work + key + '/urls-end', "r") as tf:
                linesend = tf.read().split('\n')
                tf.close()

            for prefix in prefixs:
                for subfix in subfixs:
                    print(f" ## KEYWORD: %s PREFIJO: %s SUBFIJO: %s ##" % (key, prefix, subfix))
                    urls = Webs().buscar_google(prefix + " " + key + " " + subfix, num_search, "es")
                    for numurl, url in enumerate(urls):
                        newurls = numurl + 1
                        if url not in lines:
                            if url not in linesko:
                                urlsok += 1
                                if url not in linesok:
                                    if url not in linesend:
                                        print(f"{GREEN}     - Pagina añadidas para analisis:{RESET} %s" % url)
                                        with open(path_work + key + '/urls-ok', 'a') as f:
                                            f.write(url + os.linesep)
                                            f.close()
                                        urlsok2 += 1
                                else:
                                    urlsko += 1
                            else:
                                urlsko += 1

        if urlsok2 == 0:
            print(f"      {BLUE}- ¡Ninguna url para analizar!{RESET}")

        print(f"{GREEN}\nHa terminado la obtención de urls a explorar.{RESET}")
        print("\nNúmero de urls: %s" % newurls)
        print(f"Número de urls validas: {BLUE}%s{RESET}" % urlsok)
        print(f"Número de urls a analizar: {GREEN}%s{RESET}" % urlsok2)
        print(f"Número de urls invalidas: {RED}%s{RESET}" % urlsko)

        return True

    def process_urls(self, keys):
        from includes.webs import Webs

        path_work = self.path_dataset + "/pre/"

        print(f"\n{BLUE}Procesando...{RESET}\n")

        numpages = 1

        for key in keys:

            if not os.path.exists(path_work + key + '/tmp/'):
                os.mkdir(path_work + key + '/tmp/')

            if not os.path.exists(path_work + key + '/images/'):
                os.mkdir(path_work + key + '/images/')

            with open(path_work + key + '/urls-ok', "r") as tf:
                lines = tf.read().split('\n')
                tf.close()

            for url in lines:
                if url != "":
                    try:
                        title, result = Webs().connect(url)

                        if result is not None:
                            if result == "timeout":
                                print(f"   - %s -> {RED}TIME OUT{RESET}" % title)
                                continue

                            # Comprobar si ya existe el archivo a crear
                            num = Tools().findIDfiles(path_work + key + '/tmp/', key, numpages)

                            with open(path_work + key + '/tmp/' + key + '-' + str(num), 'w') as f:
                                for i in result:
                                    f.write(i)
                                f.close()

                            num += 1

                            Tools().writeFilesOK(path_work, key, url)
                            print(f"   - %s -> {GREEN}OK{RESET}" % title)

                        else:
                            Tools().writeFilesKO(path_work, key, url)
                            print(f"\n !!!! %s: {RED}KO{RESET} !!!! \n" % url)

                    except:
                        print(f"Error al procesar: %s" % url)
                        pass


parser = argparse.ArgumentParser(add_help=True, formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description="""
                                 Extractor de datos.
                                """,
                                 epilog="Enjoy the program! :)", )

parser.add_argument('-k', '--keywords', help='Palabras clave a buscar.', nargs='+', required=True)
parser.add_argument('-s', '--subfix', help="Añadir prefijos a las palabras clave.", nargs='+', required=True)
parser.add_argument('-p', '--prefix', help="Añadir subfijos a las palabras clave.", nargs='+', required=True)
parser.add_argument('-n', '--numsearch', help="Numero de busquedas a realizar.", type=int, default=2)

args = parser.parse_args()

status = GMM().get_urls(args.keywords, args.subfix, args.prefix, args.numsearch)

if status is True:
    GMM().process_urls(args.keywords)
