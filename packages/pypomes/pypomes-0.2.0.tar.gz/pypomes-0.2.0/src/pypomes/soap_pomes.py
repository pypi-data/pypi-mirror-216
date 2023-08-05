from lxml import etree
from zeep import Client
import ast
import json
import requests


def soap_build_envelope(zeep_client: Client, service: str, payload: dict, file_path: str = None) -> bytes:
    """
    Constrói e retorna o envelope SOAP para um dado serviço. Esse envelope não contem os *headers*.

    :param zeep_client: o cliente zeep
    :param payload: os dados a serem enviados
    :param service: o nome do serviço
    :param file_path: Path to store the soap envelope.
    :return: o envelope para a requisição SOAP, sem os headers
    """
    # obtem o envelope XML
    root = zeep_client.create_message(zeep_client.service, service, **payload)
    result: bytes = etree.tostring(element_or_tree=root,
                                   pretty_print=True)

    # salva o envelope em arquivo ?
    if file_path is not None:
        # sim
        with open(file_path, "wb") as f:
            f.write(result)

    return result


def soap_post(ws_url: str, soap_envelope: bytes, extra_headers: dict = None, file_path: str = None) -> bytes:
    """
    Encaminha a solicitação SOAP, e retorna a resposta recebida.

    :param ws_url: a URL da solicitação
    :param soap_envelope: o envelope SOAP
    :param extra_headers: cabeçalho adicional
    :param file_path: Path to store the response to the request.
    :return: a resposta à solicitação
    """
    # constrói o cabeçalho do envelope SOAP
    headers: dict = {"SOAPAction": '""',
                     "content-type": "application/soap+xml; charset=utf-8"}

    # um cabeçalho adicional foi definido ?
    if extra_headers is not None:
        # sim, contabilize-o
        headers.update(extra_headers)

    # envia o request
    response: requests.Response = requests.post(url=ws_url,
                                                data=soap_envelope,
                                                headers=headers)
    result: bytes = response.content

    # salva o response em arquivo ?
    if file_path is not None:
        # sim
        with open(file_path, "wb") as f:
            f.write(result)

    return result


def soap_post_zeep(zeep_service: callable, payload: dict, file_path: str = None) -> dict:
    """
    Encaminha a solicitação SOAP utilizando o pacote *zeep*, e retorna a resposta recebida.

    :param zeep_service: o serviço de referência
    :param payload: os dados a serem enviados
    :param file_path: Path to store the JSON corresponding to the returned response.
    :return: a resposta à solicitação
    """
    # import the needed function
    from .json_pomes import jsonify_dict

    # invoca o servico
    # ('response' é uma subclasse de dict - definida como retorno do 'zeep_service' no wsdl)
    response: any = zeep_service(**payload)

    # converte o conteúdo retornado em dict e o prepara para descarga em JSON
    result: dict = ast.literal_eval(str(response))
    jsonify_dict(result)

    # salva o retorno em arquivo ?
    if file_path is not None:
        # sim
        with open(file_path, "w") as f:
            f.write(json.dumps(result, ensure_ascii=False))

    return result


def soap_get_dict(soap_response: bytes, xml_path: str = None, json_path: str = None) -> dict:
    """
    Recupera o objeto *dict* contendo os dados retornados pela solicitação SOAP.
    Esse objeto é retornado em condições de ser descarregado em formato JSON.

    :param soap_response: o conteúdo retornado pela solicitação SOAP
    :param xml_path: Path to store the XML correspondinge to the returned response.
    :param json_path: Path to store the JSON correspondinge to the returned response.
    :return: o objeto com os dados de resposta à solicitação
    """
    # import the needed functions
    from .json_pomes import jsonify_dict
    from .xml_pomes import xml_to_dict

    # restringe o conteúdo retornado ao conteúdo da tag soap:Body
    pos_1: int = soap_response.find(b"<soap:Body>") + 11
    pos_2: int = soap_response.find(b"</soap:Body>", pos_1)
    content: bytes = soap_response[pos_1:pos_2]

    # salva o conteúdo XML retornado em arquivo ?
    if xml_path is not None:
        # sim
        with open(xml_path, "wb") as f:
            f.write(content)

    # converte o conteúdo XML em dict e o prepara para descarga em JSON
    result: dict = xml_to_dict(content)
    jsonify_dict(result)

    # salva o retorno em arquivo ?
    if json_path is not None:
        # sim
        with open(json_path, "w") as f:
            f.write(json.dumps(result, ensure_ascii=False))

    return result


def soap_get_cids(soap_response: bytes) -> list[bytes]:
    """
    Obtem os *cids* (*Content-IDs*), em *soap_response*, indicativos de anexos retornados no padrão *MTOM*.

    O padrão *Message Transmission Optimization Mechanism* define *cids* em *tags* do tipo

    - <xop:Include xmlns:xop="http://www.w3.org/2004/08/xop/include" href="cid:<uuid4>-<NN>@<web-address>"/>

    onde as variáveis tem o significado:
   - *<uuid4*>: uma *UUID* versão 4
   - *<NN*>: um inteiro de dois dígitos
   - *<web-address*>: o endereço web associado

   Os *cids* retornados têm a forma *<uuid4>-<NN>@<web-address*.

    :param soap_response: o conteúdo retornado pela solicitação SOAP
    :return: a lista de 'content ids' encontrados, podendo ser vazia
    """
    # inicializa a variável de retorno
    result: list[bytes] = []

    prefix: bytes = b'href="cid:'
    pos_1: int = soap_response.find(prefix)
    while pos_1 > 0:
        pos_1 += len(prefix)
        pos_2: int = soap_response.find(b'"', pos_1)
        result.append(soap_response[pos_1:pos_2])
        pos_1 = soap_response.find(prefix, pos_1)

    return result


def soap_get_attachment(soap_response: bytes, cid: bytes, file_path: str = None) -> bytes:
    """
    Obtem e retorna o anexo contido no *response* da solicitação *SOAP*, no padrão *MTOM*
    (*Message Transmission Optimization Mechanism*), e identificado pelo *cid* (Content-ID).

    :param soap_response: o conteúdo retornado pela solicitação SOAP
    :param cid: a identificação do anexo
    :param file_path: Path to store the JSON corresponding to the returned attachment.
    :return: o anexo em referência, ou None se não for encontrado
    """
    # inicializa a variável de retorno
    result: bytes | None = None

    # localiza o início do anexo
    mark: bytes = b"Content-ID: <" + cid + b">"
    pos_1 = soap_response.find(mark)

    # o início do anexo foi localizado ?
    if pos_1 > 0:
        # sim, prossiga
        pos_1 += len(mark)
        # salta caracteres de controle (CR, LF, e outros)
        blank: int = b" "[0]
        while soap_response[pos_1] < blank:
            pos_1 += 1

        # obtem o separador
        pos_2: int = soap_response.find(b"--uuid:")

        separator: bytes = soap_response[pos_2:pos_2+45]  # 45 = 2 + length of uuid4 + 7

        # localiza o final do anexo
        pos_2 = soap_response.find(separator, pos_1)

        # obtem o anexo
        result: bytes = soap_response[pos_1:pos_2]

        # salva o attachment em arquivo ?
        if file_path is not None:
            # sim
            with open(file_path, "wb") as f:
                f.write(result)

    return result
