import xml.etree.ElementTree as ET

debug = False

def set_debug(value):
    global debug
    debug = value

def verificar_xml_bem_formado(xml_content):
    if debug: print("Verificando se o XML é bem formado...")
    try:
        ET.fromstring(xml_content)
        if debug: print("XML é bem formado.")
        return True
    except ET.ParseError as e:
        if debug: print(f"Erro ao verificar XML: {e}")
        return False

def verificar_xsd_bem_formado(xsd_content):
    if debug: print("Verificando se o XSD é bem formado...")
    try:
        ET.fromstring(xsd_content)
        if debug: print("XSD é bem formado.")
        return True
    except ET.ParseError as e:
        if debug: print(f"Erro ao verificar XSD: {e}")
        return False

def contar_ocorrencias(elemento, nome_filho):
    return sum(1 for filho in elemento if filho.tag == nome_filho)

def verificar_elemento(elemento, regras):
    nome = elemento.tag
    if debug: print(f"Verificando elemento '{nome}'...")
    if nome not in regras:
        if debug: print(f"Elemento '{nome}' não está definido no XSD")
        return False, f"Elemento '{nome}' não está definido no XSD"
    
    regra = regras[nome]
    tipo = regra['tipo']
    
    # Verificar tipo de dados (exemplo para string)
    if tipo == "xs:string":
        if elemento.text is not None and not isinstance(elemento.text, str):
            if debug: print(f"Elemento '{nome}' não é do tipo xs:string")
            return False, f"Elemento '{nome}' não é do tipo xs:string"
    
    # Verificar restrições nos filhos
    restricoes = regra.get('restricoes', {})
    for nome_filho, sub_regra in restricoes.items():
        ocorrencias = contar_ocorrencias(elemento, nome_filho)
        if debug: print(f"Verificando ocorrências do elemento filho '{nome_filho}' em '{nome}'...")
        if ocorrencias < sub_regra['minOccurs']:
            if debug: print(f"Elemento '{nome_filho}' ocorre menos vezes que o permitido ({ocorrencias} < {sub_regra['minOccurs']})")
            return False, f"Elemento '{nome_filho}' ocorre menos vezes que o permitido ({ocorrencias} < {sub_regra['minOccurs']})"
        if sub_regra['maxOccurs'] is not None and ocorrencias > sub_regra['maxOccurs']:
            if debug: print(f"Elemento '{nome_filho}' ocorre mais vezes que o permitido ({ocorrencias} > {sub_regra['maxOccurs']})")
            return False, f"Elemento '{nome_filho}' ocorre mais vezes que o permitido ({ocorrencias} > {sub_regra['maxOccurs']})"
        
        for filho in elemento.findall(nome_filho):
            valid, msg = verificar_elemento(filho, restricoes)
            if not valid:
                return valid, msg
    
    if debug: print(f"Elemento '{nome}' é válido de acordo com as regras do XSD")
    return True, "XML é válido de acordo com as regras do XSD"

def verificar_xml_contra_regras(xml_content, regras):
    root = ET.fromstring(xml_content)
    return verificar_elemento(root, regras)
