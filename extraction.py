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
        min_occurs = int(element.get('minOccurs', '1'))
        max_occurs = element.get('maxOccurs', '1')
        max_occurs = int(max_occurs) if max_occurs != 'unbounded' else None
        
        restrictions = {}
        attributes = {}
        
        complex_type = element.find("xs:complexType", namespaces=namespace)
        if complex_type is not None:
            sequence = complex_type.find("xs:sequence", namespaces=namespace)
            if sequence is not None:
                for sub_element in sequence.findall("xs:element", namespaces=namespace):
                    sub_element_name, sub_rules = extract_rules(sub_element, is_top_level=False)
                    restrictions[sub_element_name] = sub_rules
            for attr in complex_type.findall("xs:attribute", namespaces=namespace):
                attr_name = attr.get('name')
                attr_type = attr.get('type')
                attributes[attr_name] = {'type': attr_type, 'minOccurs': 1, 'maxOccurs': 1}
        
        element_rules = {
            'type': data_type,
            'minOccurs': min_occurs,
            'maxOccurs': max_occurs,
            'restrictions': restrictions,
            'attributes': attributes
        }

        if is_top_level:
            rules[element_name] = element_rules
        if debug: print(f"Regras extraídas para o elemento '{element_name}': {element_rules}")
        return element_name, element_rules
    
    for element in root.findall("xs:element", namespaces=namespace):
        extract_rules(element)

    if debug: print("Regras extraídas do XSD:", rules)
    return rules
