__author__ = 'bala'

import os, shutil
from robot.api import SuiteVisitor
from robot.api import logger
from ParseRobotOutput import RobotOutputParser

RESERVED_VARIABLES = ['${EXECDIR}','${LOG_FILE}','${LOG_LEVEL}','${OUTPUT_DIR}','${OUTPUT_FILE}',
                      '${PREV_TEST_MESSAGE}','${PREV_TEST_NAME}','${PREV_TEST_STATUS}','${REPORT_FILE}',
                      '${SPACE}', '${SUITE_DOCUMENTATION}', '&{SUITE_METADATA}', '${SUITE_NAME}', '${SUITE_SOURCE}',
                      '${TEMPDIR}','${TEST_DOCUMENTATION}', '${TEST_MESSAGE}','${TEST_NAME}', '${TEST_STATUS}',
                      '@{TEST_TAGS}', '${DEBUG_FILE}', '${True}', '${False}', '${null}', '${None}', '${\\n}','${:}','${/}']

with open(os.path.join("async_keywords.txt")) as kfile:
    ASYNC_KEYWORDS = kfile.readline().split(",")

class PrerunUtility(SuiteVisitor):

    def __init__(self, recent_output):
        if os.path.exists(recent_output):
            self.recent_output="past_output.xml"
            shutil.copy(recent_output,self.recent_output)

    def start_suite(self, suite):
        tests_in_suite = []
        for _ in suite.tests:
            try:
                test_info = RobotOutputParser(self.recent_output).get_kwinfo(str(_))
            except IOError:
                test_info = {}

            if test_info is None or len(test_info) == len(_.keywords):
                test_info = {}
            logger.console("Keyword in the test before Parsing >>>>>>>>>>>>>>>>>>>>>>"+str(_.keywords))
            new_keywords = []
            async_kw_flag = False
            for keyword in _.keywords:
                if test_info:
                    if test_info.get("log variables"):
                        for variables in test_info.get("log variables")["msg"]["text"]:
                            variable, value = variables.split("=", 1)
                            if str(variable.replace(" ","")) not in RESERVED_VARIABLES:
                                try:
                                    if variable[0] == "@":
                                        variable = variable.replace("@","$")
                                        value = value.replace("[","").replace("]","",value,1).replace("|",",").replace(" ","")
                                    elif variable[0] == "&":
                                        value = value.replace("{","",1)[::-1].replace("}","",1).replace(" ","")[::-1]
                                        value = str(value).split("|")

                                    if type(value) is list:
                                        new_keywords.insert(0, _.keywords.create("Set Test Variable", args=[variable.replace(" ","")]+value))
                                    else:
                                        new_keywords.insert(0, _.keywords.create("Set Test Variable", args=[variable.replace(" ",""),str(value).lstrip()]))
                                except:
                                    continue

                if str(keyword) in ASYNC_KEYWORDS and \
                        [kw for kw in new_keywords if str(kw).lower() not in BUILTIN_KEYWORDS]:
                    logger.console("Sybot:BatchExecutorPrerunUtility:INFO ==> Pausing the test at "+str(keyword))
                    break
                else:
                    if test_info:
                        if str(keyword).lower() in test_info and not async_kw_flag:
                            if str(test_info[str(keyword).lower()]["status"]["attrib"]["status"]) == "PASS":
                                logger.console("Skybot:BatchExecutorPrerunUtility:INFO ==> Skipping the "
                                               "Keyword "+str(keyword)+" as it already passed in previous execution")
                            else:
                                new_keywords.append(keyword)
                        else:
                            if str(keyword) in ASYNC_KEYWORDS:
                                async_kw_flag = True
                            new_keywords.append(keyword)
                    else:
                        new_keywords.append(keyword)

            if new_keywords:
                new_keywords.append(_.keywords.create("Log Variables"))
                _.keywords = new_keywords

            logger.console("After Parsing >>>>>>>>>>>>>>>>>>>>>>"+str([kw for kw in _.keywords if "Set Test Variable" not in str(kw)]))

            if len(_.keywords) != 0:
                tests_in_suite.append(_)

        suite.tests = tests_in_suite

    def end_suite(self, suite):
        pass

    def start_test(self, test):
        pass

    def end_test(self, test):
        pass

    def visit_test(self, test):
        """Avoid visiting tests and their keywords to save a little time."""
        pass
