import os
from pathlib import Path

class IdentificaDiretorio:
    def localizaDir(pastaBusca):
        lista = ['c','a','b','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x']
        for i in lista:
            if os.path.isdir( i +':'):
                local =  i +':/'

        diretorio = Path(local)
        arquivos = diretorio.glob('**/{}'.format(pastaBusca))

        for i in arquivos:
            if 'Business Intelligence' in str(i):
                output = str(i)
            elif 'Schedules Products' in str(i):
                script = str(i)

        return output, script