import requests
from cosmo_wallet_friends.models import Objekt
from cosmo_wallet_friends.wallets import lista_carteiras

lista_objekts_trocaveis = []

def buscar_carteira(carteira_id):
    resposta = requests.get(
    f'https://polygon-mainnet.g.alchemy.com/nft/v2/OFnXkAWjmJ-emPdPy1fBsh-YVJgCo4MA/getNFTs?contractAddresses[]=0xA4B37bE40F7b231Ee9574c4b16b7DDb7EAcDC99B&owner={carteira_id}&withMetadata=true')

    return resposta.json()

def get_objekt_simplificado(obj, owner):
    novo_objekt = Objekt(obj['collectionId'].lower(),
                        obj['season'].lower(),
                        obj['member'].lower(),
                        obj['collectionNo'].lower(),
                        obj['class'].lower(), 
                        obj['transferable'], 
                        owner)

    return novo_objekt

def search_objekts_in_lista_trocaveis(busca_input):
    achou = False

    for objeck in lista_objekts_trocaveis:
        if f'{objeck.member} {objeck.collectionNo}' == busca_input:
            achou = True
            print(f'{objeck.collectionId}: {objeck.owner}')

    if achou == False:
        print(f'{busca_input} ninguem tem')

def search_all_grid_in_lista_trocaveis(member):
    inicio = 101

    for i in range(1, 9):
        search_objekts_in_lista_trocaveis(f'{member} {inicio}z')
        inicio = inicio + 1

def get_objekts_trocaveis(carteira):
    resp_carteira = buscar_carteira(lista_carteiras[carteira])

    for objeck in resp_carteira['ownedNfts']:
        is_transferable = objeck['metadata']['objekt']['transferable']

        if is_transferable:
            novo_objekt = get_objekt_simplificado(objeck['metadata']['objekt'], carteira)
            lista_objekts_trocaveis.append(novo_objekt)

    return lista_objekts_trocaveis