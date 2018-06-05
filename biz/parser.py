from rest_framework_xml.parsers import XMLParser as BaseXMLParser


class XMLParser(BaseXMLParser):
    media_type = 'text/xml'
