from dataclasses import dataclass
from typing import Optional


@dataclass
class Prestador:
    cnpj: str
    inscricao_municipal: Optional[str]
    codigo_municipio: Optional[str] = None


@dataclass
class Endereco:
    logradouro: str
    numero: str
    complemento: Optional[str]
    cidade: str
    bairro: str
    uf: str
    cep: str


@dataclass
class Tomador:
    cpf_cnpj: str
    razao_social: Optional[str] = None
    email: Optional[str] = None
    codigo_municipio: Optional[int] = None
    endereco: Optional[Endereco] = None


@dataclass
class Servico:
    valor_servicos: str
    base_calculo: str
    cnae: str
    discriminacao: str
    municipio_incidencia: str
    

@dataclass
class RecepcionarLoteParams:
    id_client_control: str
    data_emissao: str
    prestador: Prestador
    tomador: Tomador
    servico: Servico


@dataclass
class ConsultaLoteParams:
    protocolo: str
    cnpj: str
    inscricao_municipal: str
    codigo_municipio: str


@dataclass
class ConsultaRpsParams:
    numero: int
    serie: int
    tipo: int
    cnpj: int
    inscricao_municipal: int
    codigo_municipio: int


@dataclass
class ConsultaNfseParams:
    numero: int
    codigo_municipio: int
    data_inicial: str
    data_final: str
    prestador: Prestador
    tomador: Tomador


@dataclass
class CancelaNfseParams:
    numero: int
    cnpj: int
    inscricao_municipal: int
    codigo_municipio: int
    codigo_cancelamento: int


@dataclass
class ConsultaUrlVisualizacaoNfseParams:
    numero: int
    cnpj: int
    inscricao_municipal: int
    codigo_municipio: int
    codigo_tributacao_municipio: int
