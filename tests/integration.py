# jacoco-badge-generator: Github action for generating a jacoco coverage
# percentage badge.
# 
# Copyright (c) 2020-2022 Vincent A Cicirello
# https://www.cicirello.org/
#
# MIT License
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import unittest
import json

import sys
sys.path.insert(0,'src')
import jacoco_badge_generator.coverage_badges as jbg

class IntegrationTest(unittest.TestCase) :

    def testCLIIntegrationCustomCoverageLabel(self) :
        with open("tests/custom1.svg","r") as expected :
            with open("tests/cli/badges/customCoverage.svg","r") as generated :
                self.assertEqual(expected.read(), generated.read())

    def testCLIIntegrationCustomBranchesLabel(self) :
        with open("tests/custom2.svg","r") as expected :
            with open("tests/cli/badges/customBranches.svg","r") as generated :
                self.assertEqual(expected.read(), generated.read())

    def testCLIIntegrationCustomCoverageLabelJSON(self) :
        with open("tests/custom1.json","r") as expected :
            with open("tests/cli/badges/customCoverage.json","r") as generated :
                self.assertEqual(expected.read(), generated.read())

    def testCLIIntegrationCustomBranchesLabelJSON(self) :
        with open("tests/custom2.json","r") as expected :
            with open("tests/cli/badges/customBranches.json","r") as generated :
                self.assertEqual(expected.read(), generated.read())

    def testIntegrationCustomCoverageLabel(self) :
        with open("tests/custom1.svg","r") as expected :
            with open("tests/badges/customCoverage.svg","r") as generated :
                self.assertEqual(expected.read(), generated.read())

    def testIntegrationCustomBranchesLabel(self) :
        with open("tests/custom2.svg","r") as expected :
            with open("tests/badges/customBranches.svg","r") as generated :
                self.assertEqual(expected.read(), generated.read())

    def testIntegrationCustomCoverageLabelJSON(self) :
        with open("tests/custom1.json","r") as expected :
            with open("tests/badges/customCoverage.json","r") as generated :
                self.assertEqual(expected.read(), generated.read())

    def testIntegrationCustomBranchesLabelJSON(self) :
        with open("tests/custom2.json","r") as expected :
            with open("tests/badges/customBranches.json","r") as generated :
                self.assertEqual(expected.read(), generated.read())

    def testCLIIntegrationInstructionsBadge(self) :
        with open("tests/100.svg","r") as expected :
            with open("tests/cli/badges/jacoco.svg","r") as generated :
                self.assertEqual(expected.read(), generated.read())

    def testCLIIntegrationBranchesBadge(self) :
        with open("tests/90b.svg","r") as expected :
            with open("tests/cli/badges/branches.svg","r") as generated :
                self.assertEqual(expected.read(), generated.read())

    def testCLIIntegrationMultiJacocoReportsCase(self) :
        with open("tests/78.svg","r") as expected :
            with open("tests/cli/badges/coverageMulti.svg","r") as generated :
                self.assertEqual(expected.read(), generated.read())
        with open("tests/87b.svg","r") as expected :
            with open("tests/cli/badges/branchesMulti.svg","r") as generated :
                self.assertEqual(expected.read(), generated.read())
                
    def testIntegrationInstructionsBadge(self) :
        with open("tests/100.svg","r") as expected :
            with open("tests/badges/jacoco.svg","r") as generated :
                self.assertEqual(expected.read(), generated.read())

    def testIntegrationBranchesBadge(self) :
        with open("tests/90b.svg","r") as expected :
            with open("tests/badges/branches.svg","r") as generated :
                self.assertEqual(expected.read(), generated.read())

    def testIntegrationMultiJacocoReportsCase(self) :
        with open("tests/78.svg","r") as expected :
            with open("tests/badges/coverageMulti.svg","r") as generated :
                self.assertEqual(expected.read(), generated.read())
        with open("tests/87b.svg","r") as expected :
            with open("tests/badges/branchesMulti.svg","r") as generated :
                self.assertEqual(expected.read(), generated.read())

    def testIntegrationSummaryReport(self) :
        with open("tests/summary/coverage-summary.json", "r") as f :
            d = json.load(f)
            self.assertAlmostEqual(72.72727272727272, d["coverage"])
            self.assertAlmostEqual(77.77777777777777, d["branches"])
    
    def testCLIIntegrationSummaryReport(self) :
        with open("tests/cli/summary/coverage-summary.json", "r") as f :
            d = json.load(f)
            self.assertAlmostEqual(72.72727272727272, d["coverage"])
            self.assertAlmostEqual(77.77777777777777, d["branches"])

    def testIntegrationInstructionsJSON(self) :
        with open("tests/endpoints/jacoco.json", "r") as f :
            d = json.load(f)
            self.assertEqual(1, d["schemaVersion"])
            self.assertEqual("coverage", d["label"])
            self.assertEqual("100%", d["message"])
            self.assertEqual(jbg.defaultColors[0], d["color"])

    def testIntegrationBranchesJSON(self) :
        with open("tests/endpoints/branches.json", "r") as f :
            d = json.load(f)
            self.assertEqual(1, d["schemaVersion"])
            self.assertEqual("branches", d["label"])
            self.assertEqual("90%", d["message"])
            self.assertEqual(jbg.defaultColors[1], d["color"])

    def testCLIIntegrationInstructionsJSON(self) :
        with open("tests/cli/badgesJSON/jacoco.json", "r") as f :
            d = json.load(f)
            self.assertEqual(1, d["schemaVersion"])
            self.assertEqual("coverage", d["label"])
            self.assertEqual("100%", d["message"])
            self.assertEqual(jbg.defaultColors[0], d["color"])

    def testCLIIntegrationBranchesJSON(self) :
        with open("tests/cli/badgesJSON/branches.json", "r") as f :
            d = json.load(f)
            self.assertEqual(1, d["schemaVersion"])
            self.assertEqual("branches", d["label"])
            self.assertEqual("90%", d["message"])
            self.assertEqual(jbg.defaultColors[1], d["color"])
    
