import unittest
from verificacoes import verificar_xml_bem_formado, verificar_xsd_bem_formado, verificar_xml_contra_regras
from extracao import extrair_regras_do_xsd

class TestXMLValidator(unittest.TestCase):
    
    def setUp(self):
        self.valid_xml = '''<root><child>data</child></root>'''
        self.invalid_xml = '''<root><child>data</child>'''
        self.valid_xsd = '''<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
                                <xs:element name="root">
                                    <xs:complexType>
                                        <xs:sequence>
                                            <xs:element name="child" type="xs:string" minOccurs="1" maxOccurs="1"/>
                                        </xs:sequence>
                                    </xs:complexType>
                                </xs:element>
                            </xs:schema>'''
        self.invalid_xsd = '''<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
                                <xs:element name="root">
                                    <xs:complexType>
                                        <xs:sequence>
                                            <xs:element name="child" type="xs:string" minOccurs="1" maxOccurs="1"/>
                                        </xs:sequence>
                                    </xs:complexType>
                                </element>
                            </xs:schema>'''
    
    def test_verificar_xml_bem_formado(self):
        self.assertTrue(verificar_xml_bem_formado(self.valid_xml))
        self.assertFalse(verificar_xml_bem_formado(self.invalid_xml))
    
    def test_verificar_xsd_bem_formado(self):
        self.assertTrue(verificar_xsd_bem_formado(self.valid_xsd))
        self.assertFalse(verificar_xsd_bem_formado(self.invalid_xsd))
    
    def test_extrair_regras_do_xsd(self):
        regras = extrair_regras_do_xsd(self.valid_xsd)
        esperado = {
            'root': {
                'tipo': None,
                'minOccurs': 1,
                'maxOccurs': 1,
                'restricoes': {
                    'child': {
                        'tipo': 'xs:string',
                        'minOccurs': 1,
                        'maxOccurs': 1
                    }
                }
            }
        }
        self.assertEqual(regras, esperado)
    
    def test_verificar_xml_contra_regras(self):
        regras = extrair_regras_do_xsd(self.valid_xsd)
        self.assertTrue(verificar_xml_contra_regras(self.valid_xml, regras)[0])
        invalid_xml = '''<root></root>'''
        self.assertFalse(verificar_xml_contra_regras(invalid_xml, regras)[0])
    
    def test_validar_xml_contra_xsd(self):
        from main import validar_xml_contra_xsd
        
        is_valid, message = validar_xml_contra_xsd(self.valid_xml, self.valid_xsd)
        self.assertTrue(is_valid)
        self.assertEqual(message, "XML é válido de acordo com as regras do XSD")
        
        is_valid, message = validar_xml_contra_xsd(self.invalid_xml, self.valid_xsd)
        self.assertFalse(is_valid)
        self.assertEqual(message, "XML mal formado")
        
        is_valid, message = validar_xml_contra_xsd(self.valid_xml, self.invalid_xsd)
        self.assertFalse(is_valid)
        self.assertEqual(message, "XSD mal formado")

if __name__ == '__main__':
    unittest.main()
