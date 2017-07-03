import mechanize
from lxml import etree


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
        self.browser = mechanize.Browser()
        self.browser.set_handle_redirect(True)
        self.browser.set_handle_robots(False)
        self.browser.set_handle_gzip(False)

    def run(self):
        self.visit()

    def visit(self):
        self.parse(
            response=self.browser.open(self.host)
        )

    def parse(self, response):
        print response


if __name__ == "__main__":
    element = Element("div", "class", "name")
    example = Generator("google.com", element)
    example.run()