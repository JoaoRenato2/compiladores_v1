import xml.etree.ElementTree as ET

def verificar_xml_bem_formado(xml_content):
    try:
        ET.fromstring(xml_content)
        return True
    except ET.ParseError:
        return False

def verificar_xsd_bem_formado(xsd_content):
    try:
        ET.fromstring(xsd_content)
        return True
    except ET.ParseError:
        return False

def contar_ocorrencias(elemento, nome_filho):
    return sum(1 for filho in elemento if filho.tag == nome_filho)

def verificar_elemento(elemento, regras):
    nome = elemento.tag
    if nome not in regras:
        return False, f"Elemento '{nome}' não está definido no XSD"
    
    regra = regras[nome]
    tipo = regra['tipo']
    
    # Verificar tipo de dados (exemplo para string)
    if tipo == "xs:string":
        if elemento.text is not None and not isinstance(elemento.text, str):
            return False, f"Elemento '{nome}' não é do tipo xs:string"
    
    # Verificar restrições nos filhos
    restricoes = regra.get('restricoes', {})
    for nome_filho, sub_regra in restricoes.items():
        ocorrencias = contar_ocorrencias(elemento, nome_filho)
        if ocorrencias < sub_regra['minOccurs']:
            return False, f"Elemento '{nome_filho}' ocorre menos vezes que o permitido ({ocorrencias} < {sub_regra['minOccurs']})"
        if sub_regra['maxOccurs'] is not None and ocorrencias > sub_regra['maxOccurs']:
            return False, f"Elemento '{nome_filho}' ocorre mais vezes que o permitido ({ocorrencias} > {sub_regra['maxOccurs']})"
        
        for filho in elemento.findall(nome_filho):
            valid, msg = verificar_elemento(filho, restricoes)
            if not valid:
                return valid, msg
    
    return True, "XML é válido de acordo com as regras do XSD"

def verificar_xml_contra_regras(xml_content, regras):
    root = ET.fromstring(xml_content)
    return verificar_elemento(root, regras)
