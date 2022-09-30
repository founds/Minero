#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "altsys"
__license__ = "GNU General Public License v3.0"
__version__ = "0.0.02"
__email__ = "info@altsys.es"

import configparser
import sys
import os


class Tools():
    def __init__(self):
        pass

    def create_config(self, path_config, path_dataset):
        print("Creando el archivo de configuración por defecto.")
        config = configparser.ConfigParser()
        config.add_section('CONFIG')
        config.set('CONFIG', 'path_dataset', path_dataset)

        with open(path_config, 'w') as configfile:
            config.write(configfile)

    def create_structure(self, path, key):
        if not os.path.exists(path + key + '/images/'):
            os.mkdir(path + key + '/images/')

        if not os.path.exists(path + key + '/urls'):
            with open(path + key + '/urls', 'w') as f:
                f.write("")
                f.close()

            with open(path + key + '/urls-ko', "w") as f:
                f.write("")
                f.close()

            with open(path + key + '/urls-ok', "w") as f:
                f.write("")
                f.close()

            with open(path + key + '/urls-end', "w") as f:
                f.write("")
                f.close()

    def findIDfiles(self, path, key, num):
        with os.scandir(path) as ficheros:
            files = [fichero.name for fichero in ficheros if fichero.is_file()]
        IDFILE = key + '-' + str(num)
        status = False
        while status is False:
            if IDFILE in files:
                num += 1
                IDFILE = key + '-' + str(num)
            else:
                status = True

        else:
            return num

    def writeFilesOK(self, path_work, key, data):
        with open(path_work + key + '/urls-end', 'a') as fend:
            fend.write(data + os.linesep)
            fend.close()

        with open(path_work + key + '/urls-ok', 'r+') as fok:
            lines = fok.readlines()
            fok.seek(0)
            fok.truncate()

            if data not in lines:
                fok.write(data + os.linesep)
                fok.close()

        with open(path_work + key + '/urls', 'r+') as flst:
            lines = flst.readlines()
            flst.seek(0)
            flst.truncate()

            if data not in lines:
                flst.write(data + os.linesep)
                flst.close()

    def writeFilesKO(self, path_work, key, data):
        with open(path_work + key + '/urls-ko', 'a') as fko:
            fko.write(data + os.linesep)
            fko.close()

        with open(path_work + key + '/urls', 'r+') as flst:
            lines = flst.readlines()
            flst.seek(0)
            flst.truncate()

            if data not in lines:
                flst.write(data + os.linesep)
                flst.close()

        with open(path_work + key + '/urls-ok', 'r+') as fok:
            lines = fok.readlines()
            fok.seek(0)
            fok.truncate()

            if data not in lines:
                fok.write(data + os.linesep)
                fok.close()