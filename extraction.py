import xml.etree.ElementTree as ET

debug = False

def set_debug(value):
    global debug
    debug = value

def extract_rules_from_xsd(xsd_content):
    if debug: print("Extraindo regras do XSD...")
    rules = {}
    root = ET.fromstring(xsd_content)
    
    namespace = {'xs': 'http://www.w3.org/2001/XMLSchema'}
    
    def extract_rules(element, is_top_level=True):
        element_name = element.get('name')
        data_type = element.get('type')
        min_occurs = element.get('minOccurs', '1')
        max_occurs = element.get('maxOccurs', '1')
        
        restrictions = {}
        complex_type = element.find(".//xs:complexType", namespaces=namespace)
        if complex_type is not None:
            sequence = complex_type.find(".//xs:sequence", namespaces=namespace)
            if sequence is not None:
                for sub_element in sequence.findall(".//xs:element", namespaces=namespace):
                    sub_element_name, sub_rules = extract_rules(sub_element, is_top_level=False)
                    restrictions[sub_element_name] = sub_rules

        element_rules = {
            'type': data_type,
            'minOccurs': int(min_occurs),
            'maxOccurs': int(max_occurs) if max_occurs != 'unbounded' else None
        }

        if restrictions:
            element_rules['restrictions'] = restrictions

        if is_top_level:
            rules[element_name] = element_rules
        if debug: print(f"Regras extraídas para o elemento '{element_name}': {element_rules}")
        return element_name, element_rules
    
    for element in root.findall("./xs:element", namespaces=namespace):
        extract_rules(element)

    if debug: print("Regras extraídas do XSD:", rules)
    return rules
