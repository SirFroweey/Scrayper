import mechanize
from lxml import etree


HTMLParser = etree.HTMLParser()


class Element(object):
    """
    Base Element used to define what HTML element to find.
    """
    def __init__(self, element_type, attribute, value):
        self.element_type = element_type
        self.attribute = attribute
        self.value = value


class Generator:
    """
    Generates Python, Mechanize and lxml code that scrapes the target information from the specified website.
    """
    def __init__(self, host, element):
        self.host, self.element = self._check_requirements(host, element)
        self.build_browser()

    def _check_requirements(self, host, element):
        if host[:-4] != "http://":
            host = "http://" + host
        if not isinstance(element, Element):
            raise TypeError, "element must be a valid Scrayper.gen.Element() object!"
        return (host, element)

    def build_browser(self):
        """
        Build our default mechanize.Browser() instance.
        :return: None.
        """
        self.browser = mechanize.Browser()
        self.browser.set_handle_redirect(True)
        self.browser.set_handle_robots(False)
        self.browser.set_handle_gzip(False)

    def run(self):
        self.visit()

    def visit(self):
        """
        Visits the specified URL.
        :return: None.
        """
        self.parse(
            response=self.browser.open(self.host)
        )

    def parse(self, response):
        """
        Parse the HTML response and look for the target Scrayper.gen.Element().
        :param response: mechanize.open() instance.
        :return: None.
        """
        tree = etree.parse(response, HTMLParser)
        root = tree.getroot()
        branches = []
        branches += self.read_children(root)
        print branches

    def read_children(self, parent, child=False):
        """
        Traverse the parent node and its children whilst
        looking for the target Scrayper.gen.Element() object.
        :param parent: (etree.Element) parent node.
        :param child: (boolean) is this node a child, or the root node?
        :return: elements traversed.
        """
        elements = []
        if not child:
            iterator = parent.iter()
        else:
            iterator = parent.iterchildren()
        for element in iterator:
            if element.tag == self.element.element_type:
                attribute = element.attrib.get(self.element.attribute)
                if attribute and attribute == self.element.value:
                    print element
                    print dir(element)
                    print element.attrib
                    break
            else:
                elements.append(element)
        return elements


if __name__ == "__main__":
    element = Element("div", "class", "name")
    example = Generator("google.com", element)
    example.run()
