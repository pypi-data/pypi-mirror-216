from cosmo_wallet_friends.wallets import lista_carteiras
from cosmo_wallet_friends.controller import get_objekts_trocaveis, search_all_grid_in_lista_trocaveis

def buscar_objecks(busca_input):
    for carteira in lista_carteiras:        
        get_objekts_trocaveis(carteira)

    search_all_grid_in_lista_trocaveis(busca_input)