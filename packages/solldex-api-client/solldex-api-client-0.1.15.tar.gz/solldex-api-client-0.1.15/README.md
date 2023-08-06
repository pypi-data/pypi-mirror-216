# SolldexAPI Python Client

This repository contains a Python client for interacting with the Solldex API. The client supports making requests to the following endpoints:

- Recepcionar Lote RPS
- Consultar Lote
- Consultar RPS
- Consultar NFSe
- Cancelar NFSe
- URL Visualização

## Features

- Simple and intuitive interface for making requests to the Solldex API.
- Built-in retry logic using the Tenacity library, with up to 3 retry attempts and a 2 second wait between each attempt.
- Error logging for better debugging and maintenance.

## Installation

You can install the SolldexAPI Python Client via pip:

```bash
pip install solldex-api-client
```


## Usage

To use the SolldexAPI client, you'll need to import the SolldexAPI class and initialize it with your API token. 

```python
from solldex_api import SolldexAPI
from solldex_api.solldex_models import RecepcionarLoteParams, ConsultaLoteParams, ConsultaRpsParams

api = SolldexAPI('your-token-here')
```

Once you've done that, you can make requests to the Solldex API using the `recepcionar_lote`, `consultar_lote`, and `consultar_rps` and more methods:

```python
from solldex_api.solldex_models import Prestador, Tomador, Servico, Endereco

# Define data for Recepcionar Lote RPS endpoint
prestador_data = Prestador(cnpj='string', inscricao_municipal='number', codigo_municipio='number')
endereco_data = Endereco(logradouro='string', numero='number', bairro='string', uf='string', cep='number')
tomador_data = Tomador(cpf_cnpj='number', endereco=endereco_data)
servico_data = Servico(aliquota='number', discriminacao='string', iss_retido=True, item_lista_servico='number', codigo_tributario_municipio='number', valor_servicos='number')

request_data = RecepcionarLoteParams(data_emissao='date', prestador=prestador_data, tomador=tomador_data, servico=servico_data)
# Make a request to the Recepcionar Lote RPS endpoint
response = api.recepcionar_lote(request_data)

# Define data for Consultar Lote endpoint
request_data = ConsultaLoteParams(protocolo='number', cnpj='number', inscricao_municipal='number', codigo_municipio='number')
# Make a request to the Consultar Lote endpoint
response = api.consultar_lote(request_data)

# Define data for Consultar RPS endpoint
request_data = ConsultaRpsParams(numero='number', serie='number', tipo='number', cnpj='number', inscricao_municipal='number', codigo_municipio='number')
# Make a request to the Consultar RPS endpoint
response = api.consultar_rps(request_data)
```

Continue in a similar fashion for the rest of the available methods, such as `consultar_nfse`, `cancela_nfse`, and `consulta_url_nfse`, providing the correct data structure to the method.

```python
from solldex_api.solldex_models import ConsultaNfseParams, Prestador, Tomador, Endereco

# Define data for Consultar NFS-e endpoint
prestador_data = Prestador(cnpj='string', inscricao_municipal='number', codigo_municipio='number')
endereco_data = Endereco(logradouro='string', numero='number', bairro='string', uf='string', cep='number')
tomador_data = Tomador(cpf_cnpj='number', endereco=endereco_data)

request_data = ConsultaNfseParams(numero='number', codigo_municipio='number', data_inicial='date', data_final='date', prestador=prestador_data, tomador=tomador_data)
# Make a request to the Consultar NFS-e endpoint
response = api.consultar_nfse(request_data)
```

Remember to replace `'number'`, `'string'`, and `'date'` with actual values before executing the requests.

Errors during the request will be logged, and the methods will automatically retry the request up to

## Error Handling

The SolldexAPI client uses the Tenacity library to provide built-in retry logic for requests. If a request fails, the client will automatically retry it up to 3 times, with a 2 second wait between each attempt.

If a request continues to fail after 3 attempts, the client will log the error and raise a `requests.RequestException` exception.
