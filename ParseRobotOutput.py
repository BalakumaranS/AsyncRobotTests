__author__ = 'bala'

import xml.etree.ElementTree as ET
from collections import OrderedDict

class RobotOutputParser(object):
    def __init__(self, robot_output):
        self.robot_output_file = robot_output
        try:
            self.tree = ET.parse(self.robot_output_file)
            self.root = self.tree.getroot()
        except:
            self.tree, self.root = [None]*2

    def get_kwinfo(self, testcase, keyword=None):

        if not self.tree:
            return None

        keywords_info = OrderedDict()
        for test in self.root.iter("test"):
            if test.attrib["name"] == testcase:
                for kw in test.iter("kw"):
                    if keyword:
                        if kw.attrib["name"] == keyword:
                            return { str(kw.attrib["name"]).lower(): self._get_kwdetails()}

                    keywords_info[str(kw.attrib["name"]).lower()] = self._get_kwdetails(kw)
        return keywords_info

    def _get_kwdetails(self, kw):
        kw_info = {}
        for _ in kw:
            if _.tag not in kw_info:
                kw_info[_.tag] = {
                                    "text" : [_.text],
                                    "attrib": _.attrib
                                 }
            else:
                kw_info[_.tag]["text"].append(_.text),
        return kw_info

    def _write_output(self):
        self.tree.write(self.robot_output_file)

