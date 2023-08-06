from lacam_v0 import DATADIR
import requests
import os

class Dados:

    def __init__(self, name: list):
        self.dados_disp = self._create_dict()

        for i in range(len(name)):
            self._download_data(name[i])

    @staticmethod
    def _create_dict():
        try:
            dicio = {}
            path = os.path.join(DATADIR, 'dados_disp.txt')
            with open(path, "r") as file:
                for line in file:
                    key, value = line.split(";")
                    dicio[key] = value
            return dicio
        except Exception as e:
            print(f"Error: {str(e)}")

    def _download_data(self, name: str):

        if name in self.dados_disp.keys():
            filename = name
            url = self.dados_disp[filename.replace('\n', '')]
            filename = filename + '.csv'

            with requests.get(url) as req:
                with open(filename, 'wb') as f:
                    for chunk in req.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            print(f'O arquivo {name} foi criado')
        else:
            print(f'O arquivo {name} existe.')