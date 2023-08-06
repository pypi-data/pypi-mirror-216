import requests
from pandas import Series, DataFrame
import pandas as pd

url = "https://apisinda.dev.coene.inpe.br/api/"
fields = ['latitude', 'longitude', 'altitude', 'estado', 'fabricante', 'modelo', 'codigoWMOFLU', 'intervaloTempoColeta', 'estacao', 'canais']
states = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AP': 'Amapá',
    'AM': 'Amazonas',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PR': 'Paraná',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'SC': 'Santa Catarina',
    'SP': 'São Paulo',
    'SE': 'Sergipe',
    'TO': 'Tocantins'
}

def createHeader(token):
    accessToken = 'Bearer ' + token
    return {'Authorization' : accessToken}

class PCD:
    def __init__(self, numero, token):
        if type(numero) == int and type(token) == str:
            self.numero = numero
            self.token = token
        else:
            print("Numero must be integer and token must be string")

    def get_metadata(self):
        try:
            metadados = requests.get(url + 'buscar/' + str(self.numero), headers=createHeader(self.token))
            if metadados.ok:
                return metadados.json()
            else:
                return metadados.text
        except:
            return("Error fetching metadata")

    def get_metadata_serie(self):
        metadados = self.get_metadata()
        try:
            return pd.Series(metadados)
        except:
            return metadados

    def get_metadata_resumed(self):
        metadados = self.get_metadata()
        try:
            extra_field = ['latitude', 'longitude', 'estado', 'cidade']
            metadados_filtered = {'id': metadados['id'], 'numero': metadados['numero'],
                'ativo': metadados['ativo'], 'proprietario': metadados['proprietario']['nome']}
            for field in extra_field:
                if field in metadados:
                    metadados_filtered[field] = metadados[field]
            return metadados_filtered
        except:
            return("Error fetching resumed metadata")

    def get_owner(self):
        try:
            metadados = requests.get(url + 'buscar/' + str(self.numero), headers=createHeader(self.token))
            if metadados.ok:
                return metadados.json()['proprietario']
            else:
                return metadados.text
        except:
            return("Error fetching owner")
    
    def get_owner_name(self):
        proprietario = self.get_owner()
        try:
            return proprietario['nome']
        except:
            return proprietario

    def get_pcd_family(self):
        try:
            metadados = requests.get(url + 'buscar/' + str(self.numero), headers=createHeader(self.token))
            if metadados.ok:
                return metadados.json()['familiaPCD']
            else:
                return metadados.text
        except:
            return("Error fetching pcd family")

    def get_sensors(self):
        try:
            sensores = requests.get(url + 'buscar/sensores/' + str(self.numero), headers=createHeader(self.token))
            if sensores.ok:
                return sensores.json()
            else:
                return sensores.text
        except:
            return("Error fetching sensors")

    def get_sensors_df(self):
        sensores = self.get_sensors()
        try:
            return pd.DataFrame(sensores)
        except:
            return sensores

    def get_available_period(self):
        try:
            periodo = requests.get(url + 'buscar/periodo-disponivel/' + str(self.numero), headers=createHeader(self.token))
            if periodo.ok:
                return periodo.json()
            else:
                return periodo.text
        except:
            return("Error fetching available period")

    def get_data(self, dataInicial="", dataFinal=""):
        try:
            if dataInicial == "" or dataFinal ==  "":
                periodo = self.get_available_period()
                dataInicial = periodo['dataInicial']
                dataFinal = periodo['dataFinal']
            analisePCD = {'pcd': {'numero': self.numero}, 'dataInicial': dataInicial, 'dataFinal': dataFinal}
            dados = requests.post(url + 'buscar/dados', json=analisePCD, headers=createHeader(self.token))
            return dados.json()
        except:
            return("Error fetching data")

    def get_data_df(self):
        dados = self.get_data()
        try:
            dados_df = pd.DataFrame(dados['dados'], columns=dados['cabecalho'])
            dados_df = dados_df.replace('', None)
            dados_df['Tempo'] = pd.to_datetime(dados_df['Tempo'])
            dados_df = dados_df.set_index(dados_df.columns[0])
            dados_df = dados_df.astype(float)
            return dados_df
        except:
            return dados

    def get_small_data_df(self):
        dados_df = self.get_data_df()
        try:
            dataFinal = dados_df.index[-1]
            dataInicial1 = dataFinal - pd.DateOffset(months=2)
            dados_df1 = dados_df[dados_df.index>dataInicial1]
            return dados_df1
        except:
            return("Error fetching small data")

    def is_private(self):
        try:
            metadados = requests.get(url + 'buscar/' + str(self.numero), headers=createHeader(self.token))
            if metadados.ok:
                return metadados.json()['privado']
            else:
                return metadados.text
        except:
            return("Error checking if pcd is private")

class Groups:
    def __init__(self, token):
        if type(token) == str:
            self.token = token
        else:
            print("Token must be string")

    def get_all(self):
        try:
            pcds = requests.get(url + 'buscar/todas', headers=createHeader(self.token))
            if pcds.ok:
                return pcds.json()
            else:
                return pcds.text
        except:
            return("Error fetching all PCDs")

    def get_all_df(self):
        pcds = self.get_all()
        try:
            return pd.DataFrame(pcds)
        except:
            return pcds

    def get_all_resumed(self):
        pcds = self.get_all()
        try:
            pcds_simple = []
            extra_field = ['latitude', 'longitude', 'estado', 'cidade']
            for idx, obj in enumerate(pcds):
                pcd = {'id': obj['id'], 'numero': obj['numero'], 'ativo': obj['ativo'],
                        'proprietario': obj['proprietario']['nome']}
                for field in extra_field:
                    if field in obj:
                        pcd[field] = obj[field]
                pcds_simple.append(pcd)
            return pcds_simple
        except:
            return("Error fetching all resumed PCDs")

    def get_public(self):
        try:
            pcds = requests.get(url + 'buscar/publicas', headers=createHeader(self.token))
            if pcds.ok:
                return pcds.json()
            else:
                return pcds.text
        except:
            return("Error fetching public PCDs")

    def get_private(self):
        try:
            pcds = requests.get(url + 'buscar/privadas', headers=createHeader(self.token))
            if pcds.ok:    
                return pcds.json()
            else:
                return pcds.text
        except:
            return("Error fetching private PCDs")

    def get_complete_pcds(self):
        try:
            pcds = requests.get(url + 'buscar/todas', headers=createHeader(self.token))
            if pcds.ok:
                pcds_json = pcds.json()
                pcds_completas = []
                for idx, obj in enumerate(pcds_json):
                    completa = True
                    for field in fields:
                        if field not in obj:
                            completa = False
                    if completa:
                        pcds_completas.append(obj)
                return pcds_completas
            else:
                return pcds.text
        except:
            return("Error fetching complete PCDs")

    def get_complete_pcds_df(self):
        pcds = self.get_complete_pcds()
        try:
            return pd.DataFrame(pcds)
        except:
            return pcds

    def get_incomplete_pcds(self):
        try:
            pcds = requests.get(url + 'buscar/todas', headers=createHeader(self.token))
            if pcds.ok:
                pcds_json = pcds.json()
                pcds_incompletas = []
                for idx, obj in enumerate(pcds_json):
                    for field in fields:
                        if field not in obj:
                            pcds_incompletas.append(obj)
                            break
                return pcds_incompletas
            else:
                return pcds.text
        except:
            return("Error fetching incomplete PCDs")

    def get_incomplete_pcds_df(self):
        pcds = self.get_incomplete_pcds()
        try:
            return pd.DataFrame(pcds)
        except:
            return pcds

    def get_incomplete_pcds_detailed(self):
        incompletas = self.get_incomplete_pcds()
        try:
            resposta = {}
            resposta['cabecalho'] = fields
            resposta['incompletas'] = []
            for field in fields:
                sublista = []
                resposta['incompletas'].append(sublista)
            for idx, elem in enumerate(incompletas):
                for i, field in enumerate(fields):
                    if field not in elem:
                        resposta['incompletas'][i].append(elem)
            return resposta
        except:
            return("Error getting incomplete PCDs detailed")

    def get_amount_incomplete_pcds_serie(self):
        incompletas = self.get_incomplete_pcds_detailed()
        try:
            cabecalho = incompletas['cabecalho']
            quantidades = []
            for i in range(len(cabecalho)):
                quantidades.append(len(incompletas['incompletas'][i]))
            return pd.Series(data = quantidades, index = cabecalho)
        except:
            return incompletas

    def get_pcds_by_state(self, state):
        try:
            if type(state) == str:
                if state in states:
                    nome_estado = states[state]
                else:
                    return("Entered state does not exist")
                pcds = requests.get(url + 'buscar/todas', headers=createHeader(self.token))
                if pcds.ok:
                    pcds_json = pcds.json()
                    pcds_filtered = []
                    for idx, obj in enumerate(pcds_json):
                        if 'estado' in obj:
                            if obj['estado'] == state or obj['estado'] == nome_estado:
                                pcds_filtered.append(obj)
                    return pcds_filtered
                else:
                    return pcds.text
            else:
                print("State must be string")
        except:
            return("Error filtering PCDs by state")

    def get_amount_pcds_state(self):
        todas_df = self.get_all_df()
        try:
            estados_serie = pd.Series(todas_df['estado'].value_counts())
            for i in estados_serie.index:
                if i not in states.keys():
                    estados_serie = estados_serie.drop(i)
            return estados_serie
        except:
            return("Error getting the amount of PCDs by state")

    def get_pcds_by_owner(self, owner):
        try:
            if type(owner) == str:
                pcds = requests.get(url + 'buscar/todas', headers=createHeader(self.token))
                if pcds.ok:
                    pcds_json = pcds.json()
                    pcds_filtered = []
                    for idx, elem in enumerate(pcds_json):
                        if elem['proprietario']['nome'] == owner:
                            pcds_filtered.append(elem)
                    return pcds_filtered
                else:
                    return pcds.text
            else:
                print("Owner must be string")
        except:
            return("Error filtering PCDs by owner")

    def get_amount_pcds_owner(self):
        todas_df = self.get_all_df()
        try:
            proprietarios_serie = pd.Series(todas_df['proprietario'].value_counts())
            new_index = []
            for idx, obj in enumerate(proprietarios_serie.index):
                new_index.append(obj['nome'])
            proprietarios_serie.index = new_index
            return proprietarios_serie
        except:
            return("Error getting the amount of PCDs by owner")