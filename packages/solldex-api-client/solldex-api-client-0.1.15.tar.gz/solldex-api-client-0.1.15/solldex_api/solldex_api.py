import json
import logging
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from typing import Dict, Union
from dataclasses import asdict
from .solldex_models import (
    RecepcionarLoteParams,
    ConsultaLoteParams,
    ConsultaRpsParams,
    ConsultaNfseParams,
    CancelaNfseParams,
    ConsultaUrlVisualizacaoNfseParams,
)


class SolldexAPI:
    """
    A Python interface to interact with the Solldex API.
    """

    def __init__(self, token: str):
        """
        Initializes a new instance of the SolldexAPI class.

        Args:
            token: The authorization token for the Solldex API.
        """
        self.base_url = "https://api.solldex.com.br/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        }                                         

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def recepcionar_lote(self, data: RecepcionarLoteParams) -> Dict:
        """
        Makes a POST request to the 'recepcionar-lote-rps' endpoint of the Solldex API.

        Args:
            data: The request body data.

        Returns:
            The response from the Solldex API.
        """
        url = f"{self.base_url}/recepciona-lote-rps"
        params = asdict(data)
        try:
            response = requests.post(url, headers=self.headers, json=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Request to {url} failed: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def consultar_lote(self, data: ConsultaLoteParams) -> Dict:
        """
        Makes a GET request to the 'consulta-lote' endpoint of the Solldex API.

        Args:
            data: The request parameters.

        Returns:
            The response from the Solldex API.
        """
        url = f"{self.base_url}/consulta-lote"
        params = asdict(data)
        try:
            response = requests.get(url, headers=self.headers, json=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Request to {url} failed: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def consultar_rps(self, data: ConsultaRpsParams) -> Dict:
        """
        Makes a GET request to the 'consulta-rps' endpoint of the Solldex API.

        Args:
            data: The request parameters.

        Returns:
            The response from the Solldex API.
        """
        url = f"{self.base_url}/consulta-rps"
        params = asdict(data)
        try:
            response = requests.get(url, headers=self.headers, json=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Request to {url} failed: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def consultar_nfse(self, data: ConsultaNfseParams) -> Dict:
        """
        Makes a GET request to the 'consulta-nfse' endpoint of the Solldex API.

        Args:
            data: The request parameters.

        Returns:
            The response from the Solldex API.
        """
        url = f"{self.base_url}/consulta-nfse"
        params = asdict(data)
        try:
            response = requests.get(url, headers=self.headers, json=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Request to {url} failed: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def cancela_nfse(self, data: CancelaNfseParams) -> Dict:
        """
        Makes a PUT request to the 'cancela-nfse' endpoint of the Solldex API.

        Args:
            data: The request parameters.

        Returns:
            The response from the Solldex API.
        """
        url = f"{self.base_url}/cancela-nfse"
        params = asdict(data)
        try:
            response = requests.put(url, headers=self.headers, json=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Request to {url} failed: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def consulta_url_nfse(self, data: ConsultaUrlVisualizacaoNfseParams) -> Dict:
        """
        Makes a GET request to the 'consulta-url-visualizacao-nfse' endpoint of the Solldex API.

        Args:
            data: The request parameters.

        Returns:
            The response from the Solldex API.
        """
        url = f"{self.base_url}/consulta-url-visualizacao-nfse"
        params = asdict(data)
        try:
            response = requests.get(url, headers=self.headers, json=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Request to {url} failed: {e}")
            raise
