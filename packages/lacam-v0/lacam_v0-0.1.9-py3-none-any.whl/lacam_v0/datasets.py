import requests
'''
class Dados:
    
    def __init__(self, name: list):
        self.arquivos_disponiveis = self._criarDict()
        
        for i in range(len(name)):
            self._baixarDados(name[i])

    def _criarDict(self):
        try:
            dicio = {}
            path = "data/dict_dados_disp.txt"
            with open(path, "r") as file:
                for line in file:
                    key, value = line.split(";")
                    dicio[key] = value       
            return dicio
        except Exception as e:
            print(f"Error: {str(e)}")

    def _baixarDados(self, name: str):

        if name in self.arquivos_disponiveis.keys():

            filename = self.arquivos_disponiveis.get(name)
            url = self.arquivos_disponiveis[filename]
            filename = filename + '.csv'

            with requests.get(url) as req:
                with open(filename, 'wb') as f:
                    for chunk in req.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            print(f'O arquivo {name} foi criado')

        else:
            print(f'O arquivo {name} não foi criado.')
            '''

class Dados:

    def __init__(self, name: list):
        self.dados_disp = self._create_dict()
        print(dados_disp)

        for i in range(len(name)):
            self._download_data(name[i])

    @staticmethod
    def _create_dict():
        try:
            dicio = {}
            path = "dados_disp.txt"
            with open(path, "r") as file:
                for line in file:
                    key, value = line.split(";")
                    dicio[key] = value
            return dicio
        except Exception as e:
            print(f"Error: {str(e)}")

    def _download_data(self, name: str):

        if name in self.dados_disp.keys():
            print(f'name >> {name}')
            filename = name
            print(f'filename >> {filename}')
            url = self.dados_disp[filename.replace('\n', '')]
            print(f'url >> {url}')
            filename = filename + '.csv'

            with requests.get(url) as req:
                with open(filename, 'wb') as f:
                    for chunk in req.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            print(f'O arquivo {name} foi criado')

        else:
            print(f'O arquivo {name} existe.')