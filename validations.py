import xml.etree.ElementTree as ET

debug = False

def set_debug(value):
    global debug
    debug = value

def is_well_formed_xml(xml_content):
    if debug: print("Verificando se o XML é bem formado...")
    try:
        ET.fromstring(xml_content)
        if debug: print("XML é bem formado.")
        return True
    except ET.ParseError as e:
        if debug: print(f"Erro ao verificar XML: {e}")
        return False

def is_well_formed_xsd(xsd_content):
    if debug: print("Verificando se o XSD é bem formado...")
    try:
        ET.fromstring(xsd_content)
        if debug: print("XSD é bem formado.")
        return True
    except ET.ParseError as e:
        if debug: print(f"Erro ao verificar XSD: {e}")
        return False

def count_occurrences(element, child_name):
    return sum(1 for child in element if child.tag == child_name)

def validate_data_type(value, data_type):
    if data_type == "xs:string":
        return True 
    elif data_type == "xs:int":
        try:
            int(value)
            return True
        except ValueError:
            return False
    elif data_type == "xs:float":
        try:
            float(value)
            return True
        except ValueError:
            return False
    return False

def validate_element(element, rules):
    name = element.tag
    if debug: print(f"Verificando elemento '{name}'...")
    if name not in rules:
        if debug: print(f"Elemento '{name}' não está definido no XSD")
        return False, f"Elemento '{name}' não está definido no XSD"
    
    rule = rules[name]
    data_type = rule['type']
    

    if data_type and element.text is not None and not validate_data_type(element.text, data_type):
        if debug: print(f"Elemento '{name}' não é do tipo {data_type}")
        return False, f"Elemento '{name}' não é do tipo {data_type}"
    
    children = list(element)
    children_count = {child.tag: count_occurrences(element, child.tag) for child in children}
    
    for child_name, sub_rule in rule.get('restrictions', {}).items():
        occurrences = children_count.get(child_name, 0)
        if debug: print(f"Verificando ocorrências do elemento filho '{child_name}' em '{name}'...")
        if occurrences < sub_rule['minOccurs']:
            if debug: print(f"Elemento '{child_name}' ocorre menos vezes que o permitido ({occurrences} < {sub_rule['minOccurs']})")
            return False, f"Elemento '{child_name}' ocorre menos vezes que o permitido ({occurrences} < {sub_rule['minOccurs']})"
        if sub_rule['maxOccurs'] is not None and occurrences > sub_rule['maxOccurs']:
            if debug: print(f"Elemento '{child_name}' ocorre mais vezes que o permitido ({occurrences} > {sub_rule['maxOccurs']})")
            return False, f"Elemento '{child_name}' ocorre mais vezes que o permitido ({occurrences} > {sub_rule['maxOccurs']})"
        
        for child in element.findall(child_name):
            valid, msg = validate_element(child, rule['restrictions'])
            if not valid:
                return valid, msg
    
    if debug: print(f"Elemento '{name}' é válido de acordo com as regras do XSD")
    return True, "XML é válido de acordo com as regras do XSD"

def validate_xml_against_rules(xml_content, rules):
    root = ET.fromstring(xml_content)
    return validate_element(root, rules)
