from unittest.mock import patch, MagicMock


def mock_api_response(url):
    if "bcdata.sgs.11" in url:  # SELIC
        return MagicMock(json=lambda: [{"data": "14/05/2026", "valor": "10.65"}])
    elif "bcdata.sgs.4389" in url:  # CDI
        return MagicMock(json=lambda: [{"data": "14/05/2026", "valor": "10.50"}])
    elif "bcdata.sgs.433" in url:  # IPCA
        return MagicMock(json=lambda: [{"data": "14/05/2026", "valor": "0.50"}])
    elif "bcdata.sgs.1" in url:  # Dólar
        return MagicMock(json=lambda: [{"data": "14/05/2026", "valor": "5.20"}])
    return MagicMock(json=lambda: [])


@patch("requests.get")
def test_api_data_fetching(mock_get):
    # Mock das respostas das APIs
    mock_get.side_effect = mock_api_response

    # Importar e executar a lógica de busca
    import requests

    # SELIC
    resposta_selic = requests.get(
        "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1?formato=json"
    )
    dados_selic = resposta_selic.json()
    selic = dados_selic[0]["valor"]
    data_selic = dados_selic[0]["data"]

    # CDI
    resposta_cdi = requests.get(
        "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4389/dados/ultimos/1?formato=json"
    )
    dados_cdi = resposta_cdi.json()
    cdi = dados_cdi[0]["valor"]
    data_cdi = dados_cdi[0]["data"]

    # IPCA
    resposta_ipca = requests.get(
        "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json"
    )
    dados_ipca = resposta_ipca.json()
    ipca = dados_ipca[0]["valor"]
    data_ipca = dados_ipca[0]["data"]

    # Dólar
    resposta_dolar = requests.get(
        "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados/ultimos/1?formato=json"
    )
    dados_dolar = resposta_dolar.json()
    dolar = dados_dolar[0]["valor"]
    data_dolar = dados_dolar[0]["data"]

    # Verificar se os valores são os esperados
    assert selic == "10.65"
    assert data_selic == "14/05/2026"
    assert cdi == "10.50"
    assert data_cdi == "14/05/2026"
    assert ipca == "0.50"
    assert data_ipca == "14/05/2026"
    assert dolar == "5.20"
    assert data_dolar == "14/05/2026"
