import unittest
from validations import is_well_formed_xml, is_well_formed_xsd, validate_xml_against_rules
from extraction import extract_rules_from_xsd

class TestXMLValidator(unittest.TestCase):
    
    def setUp(self):
        self.valid_xml = '''<root><child>data</child></root>'''  # XML válido
        self.invalid_xml = '''<root><child>data</child>'''  # XML inválido (mal formado)
        
        self.valid_xsd = '''<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
                                <xs:element name="root">
                                    <xs:complexType>
                                        <xs:sequence>
                                            <xs:element name="child" type="xs:string" minOccurs="1" maxOccurs="1"/>
                                        </xs:sequence>
                                    </xs:complexType>
                                </xs:element>
                            </xs:schema>'''  # XSD válido

        self.invalid_xsd = '''<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
                                <xs:element name="root">
                                    <xs:complexType>
                                        <xs:sequence>
                                            <xs:element name="child" type="xs:string" minOccurs="1" maxOccurs="1"/>
                                        </xs:sequence>
                                    </xs:complexType>
                                </element>
                            </xs:schema>'''  # XSD inválido (mal formado)

        self.missing_child_xml = '''<root></root>'''  # XML faltando elemento obrigatório

        self.valid_xml_multiple = '''<root><child>data1</child><child>data2</child></root>'''  # XML válido com múltiplos elementos

        self.valid_xsd_multiple = '''<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
                                        <xs:element name="root">
                                            <xs:complexType>
                                                <xs:sequence>
                                                    <xs:element name="child" type="xs:string" minOccurs="1" maxOccurs="unbounded"/>
                                                </xs:sequence>
                                            </xs:complexType>
                                        </xs:element>
                                    </xs:schema>'''  # XSD válido permitindo múltiplos elementos

        self.valid_xsd_int = '''<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
                                    <xs:element name="root">
                                        <xs:complexType>
                                            <xs:sequence>
                                                <xs:element name="child" type="xs:int" minOccurs="1" maxOccurs="1"/>
                                            </xs:sequence>
                                        </xs:complexType>
                                    </xs:element>
                                </xs:schema>'''  # XSD válido para elementos de tipo inteiro

        self.valid_xml_int = '''<root><child>123</child></root>'''  # XML válido com elemento inteiro
        self.invalid_xml_int = '''<root><child>abc</child></root>'''  # XML inválido com elemento não inteiro

    def test_is_well_formed_xml(self):
        self.assertTrue(is_well_formed_xml(self.valid_xml))
        self.assertFalse(is_well_formed_xml(self.invalid_xml))
    

    def test_is_well_formed_xsd(self):
        self.assertTrue(is_well_formed_xsd(self.valid_xsd))
        self.assertFalse(is_well_formed_xsd(self.invalid_xsd))
    

    def test_validate_xml_against_rules(self):
        rules = extract_rules_from_xsd(self.valid_xsd)
        self.assertTrue(validate_xml_against_rules(self.valid_xml, rules)[0])
        self.assertFalse(validate_xml_against_rules(self.missing_child_xml, rules)[0])
    

    def test_validate_xml_against_xsd(self):
        from main import validate_xml_against_xsd
        
        test_cases = [
            # Caso de teste 1: XML válido contra XSD válido
            (self.valid_xml, self.valid_xsd, True, "XML é válido de acordo com as regras do XSD"),
            # Caso de teste 2: XML mal formado
            (self.invalid_xml, self.valid_xsd, False, "XML mal formado"),
            # Caso de teste 3: XSD mal formado
            (self.valid_xml, self.invalid_xsd, False, "XSD mal formado"),
            # Caso de teste 4: XML faltando elemento obrigatório
            (self.missing_child_xml, self.valid_xsd, False, "Elemento 'child' ocorre menos vezes que o permitido (0 < 1)")
        ]
        
        for xml, xsd, expected_valid, expected_message in test_cases:
            with self.subTest(xml=xml, xsd=xsd):
                is_valid, message = validate_xml_against_xsd(xml, xsd)
                self.assertEqual(is_valid, expected_valid)
                self.assertEqual(message, expected_message)
    

    def test_validate_xml_against_xsd_multiple(self):
        from main import validate_xml_against_xsd
        
        is_valid, message = validate_xml_against_xsd(self.valid_xml_multiple, self.valid_xsd_multiple)
        self.assertTrue(is_valid)
        self.assertEqual(message, "XML é válido de acordo com as regras do XSD")


    def test_validate_xml_against_xsd_int(self):
        from main import validate_xml_against_xsd
        
        test_cases = [
            # Caso de teste 1: XML com elemento de tipo inteiro válido
            (self.valid_xml_int, self.valid_xsd_int, True, "XML é válido de acordo com as regras do XSD"),
            # Caso de teste 2: XML com elemento de tipo inteiro inválido
            (self.invalid_xml_int, self.valid_xsd_int, False, "Elemento 'child' não é do tipo xs:int")
        ]
        
        for xml, xsd, expected_valid, expected_message in test_cases:
            with self.subTest(xml=xml, xsd=xsd):
                is_valid, message = validate_xml_against_xsd(xml, xsd)
                self.assertEqual(is_valid, expected_valid)
                self.assertEqual(message, expected_message)


    def test_validate_xml_against_xsd_data_types(self):
        from main import validate_xml_against_xsd

        valid_xsd_date = '''<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
                                <xs:element name="root">
                                    <xs:complexType>
                                        <xs:sequence>
                                            <xs:element name="child" type="xs:date" minOccurs="1" maxOccurs="1"/>
                                        </xs:sequence>
                                    </xs:complexType>
                                </xs:element>
                            </xs:schema>'''  # XSD válido para elementos de tipo data

        valid_xml_date = '''<root><child>2023-05-28</child></root>'''  # XML válido com elemento de data
        invalid_xml_date = '''<root><child>invalid-date</child></root>'''  # XML inválido com elemento de data

        test_cases = [
            # Caso de teste 1: XML com data válida
            (valid_xml_date, valid_xsd_date, True, "XML é válido de acordo com as regras do XSD"),
            # Caso de teste 2: XML com data inválida
            (invalid_xml_date, valid_xsd_date, False, "Elemento 'child' não é do tipo xs:date")
        ]

        for xml, xsd, expected_valid, expected_message in test_cases:
            with self.subTest(xml=xml, xsd=xsd):
                is_valid, message = validate_xml_against_xsd(xml, xsd)
                self.assertEqual(is_valid, expected_valid)
                self.assertEqual(message, expected_message)


    def test_validate_xml_against_xsd_attributes(self):
        from main import validate_xml_against_xsd

        valid_xsd_attr = '''<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
                                <xs:element name="root">
                                    <xs:complexType>
                                        <xs:attribute name="attr" type="xs:string" use="required"/>
                                    </xs:complexType>
                                </xs:element>
                            </xs:schema>'''  # XSD válido com atributo obrigatório

        valid_xml_attr = '''<root attr="value"/>'''  # XML válido com atributo presente
        invalid_xml_attr = '''<root/>'''  # XML inválido com atributo ausente

        test_cases = [
            # Caso de teste 1: XML com atributo obrigatório presente
            (valid_xml_attr, valid_xsd_attr, True, "XML é válido de acordo com as regras do XSD"),
            # Caso de teste 2: XML com atributo obrigatório ausente
            (invalid_xml_attr, valid_xsd_attr, False, "Atributo 'attr' é obrigatório e está faltando")
        ]

        for xml, xsd, expected_valid, expected_message in test_cases:
            with self.subTest(xml=xml, xsd=xsd):
                is_valid, message = validate_xml_against_xsd(xml, xsd)
                self.assertEqual(is_valid, expected_valid)
                self.assertEqual(message, expected_message)

if __name__ == '__main__':
    unittest.main()
