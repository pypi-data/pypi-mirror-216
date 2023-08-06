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
    inscricao_municipal: Optional[str] = None


@dataclass
class Servico:
    valor_servicos: str
    base_calculo: str
    valor_deducoes: Optional[str]
    valor_pis: Optional[str]
    valor_cofins: Optional[str]
    valor_inss: Optional[str]
    valor_ir: Optional[str]
    valor_csll: Optional[str]
    outras_retencoes: Optional[str]
    valor_iss: Optional[str]
    aliquota: Optional[str]
    desconto_inc: Optional[str]
    desconto_con: Optional[str]
    iss_retido: Optional[str]
    item_lista_servico: Optional[str]
    cnae: str
    codigo_tributario_municipio: Optional[str]
    discriminacao: str
    codigo_pais: Optional[str]
    exigibilidade_iss: Optional[str]
    municipio_incidencia: str
    

@dataclass
class RecepcionarLoteParams:
    id_client_control: str
    serie: Optional[str]
    tipo: Optional[str]
    data_emissao: str
    status: Optional[str]
    prestador: Prestador
    tomador: Tomador
    servico: Servico
    regime_especial_tributacao: Optional[str]
    natureza_operacao: Optional[str]
    simples_nacional: Optional[str]
    incentivador_cultural: Optional[str]


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
