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

def verificar_tipo_dado(valor, tipo):
    if tipo == "xs:string":
        return True  # Qualquer valor é válido para xs:string
    elif tipo == "xs:int":
        try:
            int(valor)
            return True
        except ValueError:
            return False
    elif tipo == "xs:float":
        try:
            float(valor)
            return True
        except ValueError:
            return False
    # Adicione mais tipos conforme necessário
    return False

def verificar_elemento(elemento, regras):
    nome = elemento.tag
    if debug: print(f"Verificando elemento '{nome}'...")
    if nome not in regras:
        if debug: print(f"Elemento '{nome}' não está definido no XSD")
        return False, f"Elemento '{nome}' não está definido no XSD"
    
    regra = regras[nome]
    tipo = regra['tipo']
    
    # Verificar tipo de dados
    if tipo and elemento.text is not None and not verificar_tipo_dado(elemento.text, tipo):
        if debug: print(f"Elemento '{nome}' não é do tipo {tipo}")
        return False, f"Elemento '{nome}' não é do tipo {tipo}"
    
    filhos = list(elemento)
    filhos_contagem = {filho.tag: contar_ocorrencias(elemento, filho.tag) for filho in filhos}
    
    for nome_filho, sub_regra in regra.get('restricoes', {}).items():
        ocorrencias = filhos_contagem.get(nome_filho, 0)
        if debug: print(f"Verificando ocorrências do elemento filho '{nome_filho}' em '{nome}'...")
        if ocorrencias < sub_regra['minOccurs']:
            if debug: print(f"Elemento '{nome_filho}' ocorre menos vezes que o permitido ({ocorrencias} < {sub_regra['minOccurs']})")
            return False, f"Elemento '{nome_filho}' ocorre menos vezes que o permitido ({ocorrencias} < {sub_regra['minOccurs']})"
        if sub_regra['maxOccurs'] is not None and ocorrencias > sub_regra['maxOccurs']:
            if debug: print(f"Elemento '{nome_filho}' ocorre mais vezes que o permitido ({ocorrencias} > {sub_regra['maxOccurs']})")
            return False, f"Elemento '{nome_filho}' ocorre mais vezes que o permitido ({ocorrencias} > {sub_regra['maxOccurs']})"
        
        for filho in elemento.findall(nome_filho):
            valid, msg = verificar_elemento(filho, regra['restricoes'])
            if not valid:
                return valid, msg
    
    if debug: print(f"Elemento '{nome}' é válido de acordo com as regras do XSD")
    return True, "XML é válido de acordo com as regras do XSD"

def verificar_xml_contra_regras(xml_content, regras):
    root = ET.fromstring(xml_content)
    return verificar_elemento(root, regras)
