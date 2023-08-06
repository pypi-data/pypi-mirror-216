from dataclasses import dataclass
from typing import Optional


@dataclass
class Prestador:
    cnpj: str
    inscricao_municipal: str
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
    inscricao_municipal: Optional[str] = None


@dataclass
class Servico:
    valor_servicos: str
    base_calculo: str
    valor_deducoes: str
    valor_pis: str
    valor_cofins: str
    valor_inss: str
    valor_ir: str
    valor_csll: str
    outras_retencoes: str
    valor_iss: str
    aliquota: str
    desconto_inc: str
    desconto_con: str
    iss_retido: str
    item_lista_servico: str
    cnae: str
    codigo_tributario_municipio: str
    discriminacao: str
    codigo_pais: str
    exigibilidade_iss: str
    municipio_incidencia: str
    

@dataclass
class RecepcionarLoteParams:
    id_client_control: str
    serie: str
    tipo: str
    data_emissao: str
    status: str
    prestador: Prestador
    tomador: Tomador
    servico: Servico
    regime_especial_tributacao: str
    natureza_operacao: str
    simples_nacional: str
    incentivador_cultural: str


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
