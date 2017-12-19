__author__ = 'bala'


import xml.etree.ElementTree as ET
from robot.api import ResultVisitor
from robot.api import logger
from robot import rebot
from ParseRobotOutput import RobotOutputParser

class RebotPostrunUtility(ResultVisitor):

    def start_suite(self, suite):
        logger.console("Post run Start suite")

    def end_suite(self, suite):
        logger.console("Running rebot to consolidate output")
        rebot("output.xml")

    def start_test(self, test):
        pass

    def end_test(self, test):
        logger.console("Test is complete....")

    def visit_test(self, test):
        """Avoid visiting tests and their keywords to save a little time."""
        try:
            test_info = RobotOutputParser("past_output.xml").get_kwinfo(str(test))
        except IOError:
            test_info = {}

        if test_info:
            tree = ET.parse("output.xml")
            root = tree.getroot()
            logger.console("Post Processing the output....")
            for testcase in root.iter("test"):
                if str(testcase.attrib["name"]) == str(test):
                    logger.console("Starting the Test "+str(test))
                    i = 0
                    for kw, props_set in test_info.iteritems():
                        if not props_set:
                            continue
                        for props in props_set:
                            item = ET.Element('kw')
                            item.attrib["name"] = str(kw).title()
                            if props.get("msg"):
                                for msg in props["msg"].get("text"):
                                    msgitem = ET.SubElement(item,"msg")
                                    msgitem.text = msg
                                    for attr in props["msg"].get("attrib"):
                                        msgitem.attrib[attr] = props["msg"]["attrib"][attr]
                            statusitem = ET.SubElement(item,"status")
                            for status in props["status"]["attrib"]:
                                statusitem.attrib[status] = props["status"]["attrib"][status]
                            testcase.insert(i, item)
                            i+=1
            tree.write("output.xml")
