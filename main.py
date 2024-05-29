from verificacoes import verificar_xml_bem_formado, verificar_xsd_bem_formado, verificar_xml_contra_regras
from extracao import extrair_regras_do_xsd

def validar_xml_contra_xsd(xml_content, xsd_content):
    # Verifique se o XML e o XSD são bem formados
    if not verificar_xml_bem_formado(xml_content):
        return False, "XML mal formado"
    if not verificar_xsd_bem_formado(xsd_content):
        return False, "XSD mal formado"

    # Extrair regras do XSD
    regras = extrair_regras_do_xsd(xsd_content)

    # Verificar o XML contra as regras extraídas do XSD
    return verificar_xml_contra_regras(xml_content, regras)

# Exemplo de uso
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
    is_valid, message = validar_xml_contra_xsd(xml_content, xsd_content)
    print(is_valid, message)  # True se válido, False caso contrário
