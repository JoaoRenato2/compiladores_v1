import xml.etree.ElementTree as ET

debug = False

def set_debug(value):
    global debug
    debug = value

def extrair_regras_do_xsd(xsd_content):
    if debug: print("Extraindo regras do XSD...")
    regras = {}
    root = ET.fromstring(xsd_content)
    
    namespace = {'xs': 'http://www.w3.org/2001/XMLSchema'}
    
    def extrair_regras(element, is_top_level=True):
        nome_elemento = element.get('name')
        tipo_elemento = element.get('type')
        min_occurs = element.get('minOccurs', '1')
        max_occurs = element.get('maxOccurs', '1')
        
        restricoes = {}
        complex_type = element.find(".//xs:complexType", namespaces=namespace)
        if complex_type is not None:
            sequence = complex_type.find(".//xs:sequence", namespaces=namespace)
            if sequence is not None:
                for sub_element in sequence.findall(".//xs:element", namespaces=namespace):
                    sub_nome_elemento, sub_regras = extrair_regras(sub_element, is_top_level=False)
                    restricoes[sub_nome_elemento] = sub_regras

        regras_elemento = {
            'tipo': tipo_elemento,
            'minOccurs': int(min_occurs),
            'maxOccurs': int(max_occurs) if max_occurs != 'unbounded' else None
        }

        if restricoes:
            regras_elemento['restricoes'] = restricoes

        if is_top_level:
            regras[nome_elemento] = regras_elemento
        if debug: print(f"Regras extraídas para o elemento '{nome_elemento}': {regras_elemento}")
        return nome_elemento, regras_elemento
    
    for element in root.findall("./xs:element", namespaces=namespace):
        extrair_regras(element)

    if debug: print("Regras extraídas do XSD:", regras)
    return regras
