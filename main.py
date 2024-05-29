from validations import is_well_formed_xml, is_well_formed_xsd, validate_xml_against_rules, set_debug as set_debug_validations
from extraction import extract_rules_from_xsd, set_debug as set_debug_extraction

def validate_xml_against_xsd(xml_content, xsd_content, debug=False):
    set_debug_validations(debug)
    set_debug_extraction(debug)
    if debug: print("Iniciando validação do XML contra o XSD...")
    

    if not is_well_formed_xml(xml_content):
        return False, "XML mal formado"
    if not is_well_formed_xsd(xsd_content):
        return False, "XSD mal formado"


    rules = extract_rules_from_xsd(xsd_content)


    is_valid, message = validate_xml_against_rules(xml_content, rules)
    if debug: print(message)
    return is_valid, message

if __name__ == "__main__":
    xml_content = '''<root><child>data</child></root>'''
    xsd_content = '''<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
                        <xs:element name="root">
                            <xs:complexType>
                                <xs:sequence>
                                    <xs:element name="child" type="xs:string" minOccurs="1" maxOccurs="1"/>
                                </xs:sequence>
                            </xs:complexType>
                        </xs:element>
                    </xs:schema>'''
    is_valid, message = validate_xml_against_xsd(xml_content, xsd_content, debug=True)
    print(is_valid, message)
