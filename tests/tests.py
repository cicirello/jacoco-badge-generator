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
import jacoco_badge_generator.text_length as textLength 

class TestJacocoBadgeGenerator(unittest.TestCase) :

    def testTextLength(self) :
        self.assertEqual(510, textLength.calculateTextLength110("coverage"))
        self.assertEqual(507, textLength.calculateTextLength110("branches"))
        self.assertAlmostEqual(51.0, textLength.calculateTextLength("coverage", 11, False, 400))
        self.assertAlmostEqual(50.7, textLength.calculateTextLength("branches", 11, False, 400))
        self.assertAlmostEqual(510, textLength.calculateTextLength("coverage", 146 + 2/3, True, 400))
        self.assertAlmostEqual(507, textLength.calculateTextLength("branches", 146 + 2/3, True, 400))
        self.assertAlmostEqual(51.0, textLength.calculateTextLength("coverage", 14 + 2/3, True, 400))
        self.assertAlmostEqual(50.7, textLength.calculateTextLength("branches", 14 + 2/3, True, 400))
        self.assertAlmostEqual(76.5, textLength.calculateTextLength("coverage", 11, False, 600))
        self.assertAlmostEqual(76.05, textLength.calculateTextLength("branches", 11, False, 600))
        self.assertAlmostEqual(765, textLength.calculateTextLength("coverage", 146 + 2/3, True, 600))
        self.assertAlmostEqual(760.5, textLength.calculateTextLength("branches", 146 + 2/3, True, 600))
        self.assertAlmostEqual(76.5, textLength.calculateTextLength("coverage", 14 + 2/3, True, 600))
        self.assertAlmostEqual(76.05, textLength.calculateTextLength("branches", 14 + 2/3, True, 600))

    def testCoverageDecreasedSummary(self) :
        # Same coverages
        self.assertFalse(
            jbg.coverageDecreasedSummary(
                True,
                True,
                "tests/reportTest.json",
                0.7272727272727272,
                0.7777777777777777
            )
        )
        self.assertFalse(
            jbg.coverageDecreasedSummary(
                False,
                True,
                "tests/reportTest.json",
                0.7272727272727272,
                0.7777777777777777
            )
        )
        self.assertFalse(
            jbg.coverageDecreasedSummary(
                True,
                False,
                "tests/reportTest.json",
                0.7272727272727272,
                0.7777777777777777
            )
        )
        self.assertFalse(
            jbg.coverageDecreasedSummary(
                False,
                False,
                "tests/reportTest.json",
                0.7272727272727272,
                0.7777777777777777
            )
        )
        # Decreased coverage
        self.assertTrue(
            jbg.coverageDecreasedSummary(
                True,
                True,
                "tests/reportTest.json",
                0.7272727172727272,
                0.7777777777777777
            )
        )
        self.assertTrue(
            jbg.coverageDecreasedSummary(
                True,
                False,
                "tests/reportTest.json",
                0.7272727172727272,
                0.7777777777777777
            )
        )
        self.assertFalse(
            jbg.coverageDecreasedSummary(
                False,
                True,
                "tests/reportTest.json",
                0.7272727172727272,
                0.7777777777777777
            )
        )
        self.assertFalse(
            jbg.coverageDecreasedSummary(
                False,
                False,
                "tests/reportTest.json",
                0.7272727172727272,
                0.7777777777777777
            )
        )
        # Decreased branches
        self.assertTrue(
            jbg.coverageDecreasedSummary(
                True,
                True,
                "tests/reportTest.json",
                0.7272727272727272,
                0.7777777677777777
            )
        )
        self.assertTrue(
            jbg.coverageDecreasedSummary(
                False,
                True,
                "tests/reportTest.json",
                0.7272727272727272,
                0.7777777677777777
            )
        )
        self.assertFalse(
            jbg.coverageDecreasedSummary(
                True,
                False,
                "tests/reportTest.json",
                0.7272727272727272,
                0.7777777677777777
            )
        )
        self.assertFalse(
            jbg.coverageDecreasedSummary(
                False,
                False,
                "tests/reportTest.json",
                0.7272727272727272,
                0.7777777677777777
            )
        )
        # Both decreased
        self.assertTrue(
            jbg.coverageDecreasedSummary(
                True,
                True,
                "tests/reportTest.json",
                0.7272727172727272,
                0.7777777677777777
            )
        )
        self.assertTrue(
            jbg.coverageDecreasedSummary(
                True,
                False,
                "tests/reportTest.json",
                0.7272727172727272,
                0.7777777677777777
            )
        )
        self.assertTrue(
            jbg.coverageDecreasedSummary(
                False,
                True,
                "tests/reportTest.json",
                0.7272727172727272,
                0.7777777677777777
            )
        )
        self.assertFalse(
            jbg.coverageDecreasedSummary(
                False,
                False,
                "tests/reportTest.json",
                0.7272727172727272,
                0.7777777677777777
            )
        )

    def testCoverageDictionary(self) :
        cov = 8 / 9
        branches = 8 / 11
        d = jbg.coverageDictionary(cov, branches)
        expected = { "coverage" : 800 / 9, "branches" : 800 / 11 }
        self.assertAlmostEqual(expected["coverage"], d["coverage"])
        self.assertAlmostEqual(expected["branches"], d["branches"])
        d = jbg.coverageDictionary(0, 1)
        self.assertAlmostEqual(0.0, d["coverage"])
        self.assertAlmostEqual(100.0, d["branches"])
        d = jbg.coverageDictionary(1, 0)
        self.assertAlmostEqual(100.0, d["coverage"])
        self.assertAlmostEqual(0.0, d["branches"])
        
    def testCoverageDecreased(self) :
        badgeFiles = [ "tests/0.svg",
                          "tests/599.svg",
                          "tests/60.svg",
                          "tests/70.svg",
                          "tests/80.svg",
                          "tests/899.svg",
                          "tests/90.svg",
                          "tests/99.svg",
                          "tests/999.svg",
                          "tests/100.svg"
                          ]
        prior = [0, 0.599, 0.6, 0.7, 0.8, 0.899, 0.9, 0.99, 0.999, 1.0 ]
        for i, f in enumerate(badgeFiles) :
            self.assertFalse(jbg.coverageDecreased(prior[i], f, "coverage"))
            self.assertFalse(jbg.coverageDecreased(prior[i]+0.1, f, "coverage"))
            self.assertTrue(jbg.coverageDecreased(prior[i]-0.1, f, "coverage"))
            self.assertFalse(jbg.coverageDecreased(prior[i]+0.0001, f, "coverage"))
            self.assertTrue(jbg.coverageDecreased(prior[i]-0.0001, f, "coverage"))

        branchesBadgeFiles = [ "tests/87b.svg", "tests/90b.svg", "tests/999b.svg" ]
        prior = [0.87, 0.9, 0.999]
        for i, f in enumerate(branchesBadgeFiles) :
            self.assertFalse(jbg.coverageDecreased(prior[i], f, "branches"))
            self.assertFalse(jbg.coverageDecreased(prior[i]+0.1, f, "branches"))
            self.assertTrue(jbg.coverageDecreased(prior[i]-0.1, f, "branches"))
            self.assertFalse(jbg.coverageDecreased(prior[i]+0.0001, f, "branches"))
            self.assertTrue(jbg.coverageDecreased(prior[i]-0.0001, f, "branches"))

        for i in range(0, 101, 5) :
            cov = i / 100
            self.assertFalse(jbg.coverageDecreased(cov, "tests/idontexist.svg", "coverage"))
            self.assertFalse(jbg.coverageDecreased(cov, "tests/idontexist.svg", "branches"))

    def testCoverageDecreasedCustomLabelCase(self) :
        self.assertFalse(jbg.coverageDecreased(1.0, "tests/custom1.svg", "custom coverage label one"))
        self.assertFalse(jbg.coverageDecreased(1.0001, "tests/custom1.svg", "custom coverage label one"))
        self.assertTrue(jbg.coverageDecreased(0.9999, "tests/custom1.svg", "custom coverage label one"))
        self.assertFalse(jbg.coverageDecreased(0.9, "tests/custom2.svg", "custom coverage label two"))
        self.assertFalse(jbg.coverageDecreased(0.9001, "tests/custom2.svg", "custom coverage label two"))
        self.assertTrue(jbg.coverageDecreased(0.8999, "tests/custom2.svg", "custom coverage label two"))

        self.assertFalse(jbg.coverageDecreasedEndpoint(1.0, "tests/custom1.json", "custom coverage label one"))
        self.assertFalse(jbg.coverageDecreasedEndpoint(1.0001, "tests/custom1.json", "custom coverage label one"))
        self.assertTrue(jbg.coverageDecreasedEndpoint(0.9999, "tests/custom1.json", "custom coverage label one"))
        self.assertFalse(jbg.coverageDecreasedEndpoint(0.9, "tests/custom2.json", "custom coverage label two"))
        self.assertFalse(jbg.coverageDecreasedEndpoint(0.9001, "tests/custom2.json", "custom coverage label two"))
        self.assertTrue(jbg.coverageDecreasedEndpoint(0.8999, "tests/custom2.json", "custom coverage label two"))

    def testCoverageDecreasedEndpoint(self) :
        jsonFiles = [ "tests/0.json",
                          "tests/599.json",
                          "tests/60.json",
                          "tests/70.json",
                          "tests/80.json",
                          "tests/899.json",
                          "tests/90.json",
                          "tests/99.json",
                          "tests/999.json",
                          "tests/100.json"
                          ]
        prior = [0, 0.599, 0.6, 0.7, 0.8, 0.899, 0.9, 0.99, 0.999, 1.0 ]
        for i, f in enumerate(jsonFiles) :
            self.assertFalse(jbg.coverageDecreasedEndpoint(prior[i], f, "coverage"))
            self.assertFalse(jbg.coverageDecreasedEndpoint(prior[i]+0.1, f, "coverage"))
            self.assertTrue(jbg.coverageDecreasedEndpoint(prior[i]-0.1, f, "coverage"))
            self.assertFalse(jbg.coverageDecreasedEndpoint(prior[i]+0.0001, f, "coverage"))
            self.assertTrue(jbg.coverageDecreasedEndpoint(prior[i]-0.0001, f, "coverage"))

        branchesJsonFiles = [ "tests/0b.json",
                          "tests/599b.json",
                          "tests/60b.json",
                          "tests/70b.json",
                          "tests/80b.json",
                          "tests/899b.json",
                          "tests/90b.json",
                          "tests/99b.json",
                          "tests/999b.json",
                          "tests/100b.json"
                          ]
        for i, f in enumerate(branchesJsonFiles) :
            self.assertFalse(jbg.coverageDecreasedEndpoint(prior[i], f, "branches"))
            self.assertFalse(jbg.coverageDecreasedEndpoint(prior[i]+0.1, f, "branches"))
            self.assertTrue(jbg.coverageDecreasedEndpoint(prior[i]-0.1, f, "branches"))
            self.assertFalse(jbg.coverageDecreasedEndpoint(prior[i]+0.0001, f, "branches"))
            self.assertTrue(jbg.coverageDecreasedEndpoint(prior[i]-0.0001, f, "branches"))

        for i in range(0, 101, 5) :
            cov = i / 100
            self.assertFalse(jbg.coverageDecreasedEndpoint(cov, "tests/idontexist.svg", "coverage"))
            self.assertFalse(jbg.coverageDecreasedEndpoint(cov, "tests/idontexist.svg", "branches"))

    def testGetPriorCoverage(self):
        badgeFiles = [ "tests/0.svg",
                          "tests/599.svg",
                          "tests/60.svg",
                          "tests/70.svg",
                          "tests/80.svg",
                          "tests/899.svg",
                          "tests/90.svg",
                          "tests/99.svg",
                          "tests/999.svg",
                          "tests/100.svg"
                          ]
        expected = [0, 0.599, 0.6, 0.7, 0.8, 0.899, 0.9, 0.99, 0.999, 1.0 ]
        for i, f in enumerate(badgeFiles) :
            self.assertAlmostEqual(expected[i], jbg.getPriorCoverage(f, "coverage"))
        self.assertEqual(-1, jbg.getPriorCoverage("tests/idontexist.svg", "coverage"))
        self.assertEqual(-1, jbg.getPriorCoverage("tests/999b.svg", "coverage"))

        branchesBadgeFiles = [ "tests/87b.svg", "tests/90b.svg", "tests/999b.svg" ]
        expected = [0.87, 0.9, 0.999]
        for i, f in enumerate(branchesBadgeFiles) :
            self.assertAlmostEqual(expected[i], jbg.getPriorCoverage(f, "branches"))
        self.assertEqual(-1, jbg.getPriorCoverage("tests/idontexist.svg", "branches"))
        self.assertEqual(-1, jbg.getPriorCoverage("tests/999.svg", "branches"))

    def testGetPriorCoverageCustomBadgeLabelCase(self):
        self.assertAlmostEqual(1.0, jbg.getPriorCoverage("tests/custom1.svg", "custom coverage label one"))
        self.assertAlmostEqual(0.9, jbg.getPriorCoverage("tests/custom2.svg", "custom coverage label two"))
        self.assertAlmostEqual(1.0, jbg.getPriorCoverageFromEndpoint("tests/custom1.json", "custom coverage label one"))
        self.assertAlmostEqual(0.9, jbg.getPriorCoverageFromEndpoint("tests/custom2.json", "custom coverage label two"))

    def testGetPriorCoverageFromEndpoint(self):
        jsonFiles = [
            "tests/0.json",
            "tests/599.json",
            "tests/60.json",
            "tests/70.json",
            "tests/78.json",
            "tests/80.json",
            "tests/87.json",
            "tests/899.json",
            "tests/90.json",
            "tests/99.json",
            "tests/999.json",
            "tests/100.json",
            "tests/idontexist.json"
            ]
        jsonFilesB = [
            "tests/0b.json",
            "tests/599b.json",
            "tests/60b.json",
            "tests/70b.json",
            "tests/78b.json",
            "tests/80b.json",
            "tests/87b.json",
            "tests/899b.json",
            "tests/90b.json",
            "tests/99b.json",
            "tests/999b.json",
            "tests/100b.json",
            "tests/idontexist.json"
            ]
        expected = [0, 0.599, 0.6, 0.7, 0.78, 0.8, 0.87, 0.899, 0.9, 0.99, 0.999, 1.0, -1 ]
        for i, f in enumerate(jsonFiles) :
            self.assertAlmostEqual(expected[i], jbg.getPriorCoverageFromEndpoint(f, "coverage"), msg="file:"+f)
        for i, f in enumerate(jsonFilesB) :
            self.assertAlmostEqual(expected[i], jbg.getPriorCoverageFromEndpoint(f, "branches"), msg="file:"+f)

    def testCoverageIsFailing(self) :
        self.assertFalse(jbg.coverageIsFailing(0, 0, 0, 0))
        self.assertFalse(jbg.coverageIsFailing(0.5, 0.5, 0.5, 0.5))
        self.assertFalse(jbg.coverageIsFailing(0.51, 0.51, 0.5, 0.5))
        self.assertTrue(jbg.coverageIsFailing(0.49, 0.5, 0.5, 0.5))
        self.assertTrue(jbg.coverageIsFailing(0.5, 0.49, 0.5, 0.5))
        self.assertTrue(jbg.coverageIsFailing(0.49, 0.49, 0.5, 0.5))

    def testStringToPercentage(self) :
        for i in range(0, 101, 10) :
            expected = i/100
            s1 = str(i)
            s2 = s1 + "%"
            s3 = s1 + " %"
            s4 = str(expected)
            self.assertAlmostEqual(expected, jbg.stringToPercentage(s1))
            self.assertAlmostEqual(expected, jbg.stringToPercentage(s2))
            self.assertAlmostEqual(expected, jbg.stringToPercentage(s3))
            self.assertAlmostEqual(expected, jbg.stringToPercentage(s4))
        for j in range(10, 101, 10) :
            i = j - 0.5
            expected = i/100
            s1 = str(i)
            s2 = s1 + "%"
            s3 = s1 + " %"
            s4 = str(expected)
            self.assertAlmostEqual(expected, jbg.stringToPercentage(s1))
            self.assertAlmostEqual(expected, jbg.stringToPercentage(s2))
            self.assertAlmostEqual(expected, jbg.stringToPercentage(s3))
            self.assertAlmostEqual(expected, jbg.stringToPercentage(s4))
        i = 0.0
        while i <= 1.0 :
            s1 = str(i)
            self.assertAlmostEqual(i, jbg.stringToPercentage(s1))
            s2 = s1 + "%"
            s3 = s1 + " %"
            self.assertAlmostEqual(i/100, jbg.stringToPercentage(s2))
            self.assertAlmostEqual(i/100, jbg.stringToPercentage(s3))
            i += 0.05
        self.assertAlmostEqual(0, jbg.stringToPercentage(""))
        self.assertAlmostEqual(0, jbg.stringToPercentage("%"))
        self.assertAlmostEqual(0, jbg.stringToPercentage(" %"))
        self.assertAlmostEqual(0, jbg.stringToPercentage(" "))
        self.assertAlmostEqual(0, jbg.stringToPercentage("hello"))

    def testFilterMissingReports_empty(self) :
        self.assertEqual([], jbg.filterMissingReports([]))

    def testFilterMissingReports(self) :
        expected = ["tests/jacoco100.csv", "tests/jacoco90.csv"]
        case = ["tests/idontexist1.csv",
                "tests/jacoco100.csv",
                "tests/idontexist2.csv",
                "tests/idontexist3.csv",
                "tests/jacoco90.csv",
                "tests/idontexist4.csv"]
        self.assertEqual(expected, jbg.filterMissingReports(case))
        
    def testFullCoverage(self) :
        self.assertAlmostEqual(1, jbg.computeCoverage(["tests/jacoco100.csv"])[0])

    def testCoverage90(self) :
        self.assertAlmostEqual(0.9, jbg.computeCoverage(["tests/jacoco90.csv"])[0])

    def testCoverage901(self) :
        self.assertAlmostEqual(0.901, jbg.computeCoverage(["tests/jacoco901.csv"])[0])

    def testCoverageNoInstructions(self) :
        self.assertAlmostEqual(1, jbg.computeCoverage(["tests/jacocoDivZero.csv"])[0])

    def testFullCoverageBranches(self) :
        self.assertAlmostEqual(1, jbg.computeCoverage(["tests/branches100.csv"])[1])

    def testCoverage90Branches(self) :
        self.assertAlmostEqual(0.9, jbg.computeCoverage(["tests/branches90.csv"])[1])

    def testCoverage901Branches(self) :
        self.assertAlmostEqual(0.901, jbg.computeCoverage(["tests/branches901.csv"])[1])

    def testCoverageNoBranches(self) :
        self.assertAlmostEqual(1, jbg.computeCoverage(["tests/branchesDivZero.csv"])[1])

    def testComputeCoverageMultiJacocoReports(self) :
        coverage, branches = jbg.computeCoverage(["tests/multi1.csv", "tests/multi2.csv"])
        self.assertAlmostEqual(0.78, coverage)
        self.assertAlmostEqual(0.87, branches)

    def testCoverageTruncatedToString_str(self) :
        self.assertEqual("100%", jbg.coverageTruncatedToString(1)[0])
        self.assertEqual("100%", jbg.coverageTruncatedToString(1.0)[0])
        self.assertEqual("99.9%", jbg.coverageTruncatedToString(0.99999)[0])
        self.assertEqual("99.8%", jbg.coverageTruncatedToString(0.9989)[0])
        self.assertEqual("99%", jbg.coverageTruncatedToString(0.99000001)[0])
        self.assertEqual("99%", jbg.coverageTruncatedToString(0.9904)[0])
        self.assertEqual("99%", jbg.coverageTruncatedToString(0.99009)[0])
        self.assertEqual("99.1%", jbg.coverageTruncatedToString(0.991000001)[0])

    def testCoverageTruncatedToString_float(self) :
        self.assertAlmostEqual(100.0, jbg.coverageTruncatedToString(1)[1])
        self.assertAlmostEqual(100.0, jbg.coverageTruncatedToString(1.0)[1])
        self.assertAlmostEqual(99.9, jbg.coverageTruncatedToString(0.99999)[1])
        self.assertAlmostEqual(99.8, jbg.coverageTruncatedToString(0.9989)[1])
        self.assertAlmostEqual(99.0, jbg.coverageTruncatedToString(0.99000001)[1])
        self.assertAlmostEqual(99.0, jbg.coverageTruncatedToString(0.9904)[1])
        self.assertAlmostEqual(99.0, jbg.coverageTruncatedToString(0.99009)[1])
        self.assertAlmostEqual(99.1, jbg.coverageTruncatedToString(0.991000001)[1])

    def testFormatPercentage(self) :
        self.assertEqual("100%", jbg.badgeCoverageStringColorPair(1)[0])
        self.assertEqual("100%", jbg.badgeCoverageStringColorPair(1.0)[0])
        self.assertEqual("99.9%", jbg.badgeCoverageStringColorPair(0.99999)[0])
        self.assertEqual("99.8%", jbg.badgeCoverageStringColorPair(0.9989)[0])
        self.assertEqual("99%", jbg.badgeCoverageStringColorPair(0.99000001)[0])
        self.assertEqual("99%", jbg.badgeCoverageStringColorPair(0.9904)[0])
        self.assertEqual("99%", jbg.badgeCoverageStringColorPair(0.99009)[0])
        self.assertEqual("99.1%", jbg.badgeCoverageStringColorPair(0.991000001)[0])

    def testColor(self) :
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(1)[1])
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(1.0)[1])
        self.assertEqual(jbg.defaultColors[1], jbg.badgeCoverageStringColorPair(0.99999)[1])
        self.assertEqual(jbg.defaultColors[1], jbg.badgeCoverageStringColorPair(0.9)[1])
        self.assertEqual(jbg.defaultColors[2], jbg.badgeCoverageStringColorPair(0.89999)[1])
        self.assertEqual(jbg.defaultColors[2], jbg.badgeCoverageStringColorPair(0.8)[1])
        self.assertEqual(jbg.defaultColors[3], jbg.badgeCoverageStringColorPair(0.79999)[1])
        self.assertEqual(jbg.defaultColors[3], jbg.badgeCoverageStringColorPair(0.7)[1])
        self.assertEqual(jbg.defaultColors[4], jbg.badgeCoverageStringColorPair(0.69999)[1])
        self.assertEqual(jbg.defaultColors[4], jbg.badgeCoverageStringColorPair(0.6)[1])
        self.assertEqual(jbg.defaultColors[5], jbg.badgeCoverageStringColorPair(0.59999)[1])
        self.assertEqual(jbg.defaultColors[5], jbg.badgeCoverageStringColorPair(0.0)[1])
        self.assertEqual(jbg.defaultColors[5], jbg.badgeCoverageStringColorPair(0)[1])
        # extra colors
        colors = jbg.defaultColors[:]
        colors.append("#000000")
        colors.append("#ffffff")
        cutoffs=[100, 90, 80, 70, 60]
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(1, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(1.0, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[1], jbg.badgeCoverageStringColorPair(0.99999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[1], jbg.badgeCoverageStringColorPair(0.9, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[2], jbg.badgeCoverageStringColorPair(0.89999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[2], jbg.badgeCoverageStringColorPair(0.8, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[3], jbg.badgeCoverageStringColorPair(0.79999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[3], jbg.badgeCoverageStringColorPair(0.7, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[4], jbg.badgeCoverageStringColorPair(0.69999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[4], jbg.badgeCoverageStringColorPair(0.6, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[5], jbg.badgeCoverageStringColorPair(0.59999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[5], jbg.badgeCoverageStringColorPair(0.0, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[5], jbg.badgeCoverageStringColorPair(0, cutoffs, colors)[1])
        # fewer colors
        colors = jbg.defaultColors[:3]
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(1, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(1.0, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[1], jbg.badgeCoverageStringColorPair(0.99999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[1], jbg.badgeCoverageStringColorPair(0.9, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[2], jbg.badgeCoverageStringColorPair(0.89999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[2], jbg.badgeCoverageStringColorPair(0.8, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[2], jbg.badgeCoverageStringColorPair(0.79999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[2], jbg.badgeCoverageStringColorPair(0.7, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[2], jbg.badgeCoverageStringColorPair(0.69999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[2], jbg.badgeCoverageStringColorPair(0.6, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[2], jbg.badgeCoverageStringColorPair(0.59999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[2], jbg.badgeCoverageStringColorPair(0.0, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[2], jbg.badgeCoverageStringColorPair(0, cutoffs, colors)[1])
        # only 1 color
        colors = jbg.defaultColors[:1]
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(1, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(1.0, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(0.99999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(0.9, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(0.89999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(0.8, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(0.79999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(0.7, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(0.69999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(0.6, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(0.59999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(0.0, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(0, cutoffs, colors)[1])
        # empty color list should use default.
        colors = []
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(1, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[0], jbg.badgeCoverageStringColorPair(1.0, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[1], jbg.badgeCoverageStringColorPair(0.99999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[1], jbg.badgeCoverageStringColorPair(0.9, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[2], jbg.badgeCoverageStringColorPair(0.89999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[2], jbg.badgeCoverageStringColorPair(0.8, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[3], jbg.badgeCoverageStringColorPair(0.79999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[3], jbg.badgeCoverageStringColorPair(0.7, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[4], jbg.badgeCoverageStringColorPair(0.69999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[4], jbg.badgeCoverageStringColorPair(0.6, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[5], jbg.badgeCoverageStringColorPair(0.59999, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[5], jbg.badgeCoverageStringColorPair(0.0, cutoffs, colors)[1])
        self.assertEqual(jbg.defaultColors[5], jbg.badgeCoverageStringColorPair(0, cutoffs, colors)[1])
        

    def testColorIndex(self):
        self.assertEqual(0, jbg.computeColorIndex(100, [100, 90, 80, 70, 60], 6));
        self.assertEqual(0, jbg.computeColorIndex(100.0, [100, 90, 80, 70, 60], 6));
        self.assertEqual(1, jbg.computeColorIndex(99.999, [100, 90, 80, 70, 60], 6));
        self.assertEqual(1, jbg.computeColorIndex(90, [100, 90, 80, 70, 60], 6));
        self.assertEqual(2, jbg.computeColorIndex(89.999, [100, 90, 80, 70, 60], 6));
        self.assertEqual(2, jbg.computeColorIndex(80, [100, 90, 80, 70, 60], 6));
        self.assertEqual(3, jbg.computeColorIndex(79.999, [100, 90, 80, 70, 60], 6));
        self.assertEqual(3, jbg.computeColorIndex(70, [100, 90, 80, 70, 60], 6));
        self.assertEqual(4, jbg.computeColorIndex(69.999, [100, 90, 80, 70, 60], 6));
        self.assertEqual(4, jbg.computeColorIndex(60, [100, 90, 80, 70, 60], 6));
        self.assertEqual(5, jbg.computeColorIndex(59.999, [100, 90, 80, 70, 60], 6));
        self.assertEqual(5, jbg.computeColorIndex(50, [100, 90, 80, 70, 60], 6));
        # more cutoffs than necessary
        self.assertEqual(0, jbg.computeColorIndex(100, [100, 90, 80, 70, 60, 50], 6));
        self.assertEqual(0, jbg.computeColorIndex(100.0, [100, 90, 80, 70, 60, 50], 6));
        self.assertEqual(1, jbg.computeColorIndex(99.999, [100, 90, 80, 70, 60, 50], 6));
        self.assertEqual(1, jbg.computeColorIndex(90, [100, 90, 80, 70, 60, 50], 6));
        self.assertEqual(2, jbg.computeColorIndex(89.999, [100, 90, 80, 70, 60, 50], 6));
        self.assertEqual(2, jbg.computeColorIndex(80, [100, 90, 80, 70, 60, 50], 6));
        self.assertEqual(3, jbg.computeColorIndex(79.999, [100, 90, 80, 70, 60, 50], 6));
        self.assertEqual(3, jbg.computeColorIndex(70, [100, 90, 80, 70, 60, 50], 6));
        self.assertEqual(4, jbg.computeColorIndex(69.999, [100, 90, 80, 70, 60, 50], 6));
        self.assertEqual(4, jbg.computeColorIndex(60, [100, 90, 80, 70, 60, 50], 6));
        self.assertEqual(5, jbg.computeColorIndex(59.999, [100, 90, 80, 70, 60, 50], 6));
        self.assertEqual(5, jbg.computeColorIndex(50, [100, 90, 80, 70, 60, 50], 6));
        # even more cutoffs than necessary
        self.assertEqual(0, jbg.computeColorIndex(100, [100, 90, 80, 70, 60, 50, 0], 6));
        self.assertEqual(0, jbg.computeColorIndex(100.0, [100, 90, 80, 70, 60, 50, 0], 6));
        self.assertEqual(1, jbg.computeColorIndex(99.999, [100, 90, 80, 70, 60, 50, 0], 6));
        self.assertEqual(1, jbg.computeColorIndex(90, [100, 90, 80, 70, 60, 50, 0], 6));
        self.assertEqual(2, jbg.computeColorIndex(89.999, [100, 90, 80, 70, 60, 50, 0], 6));
        self.assertEqual(2, jbg.computeColorIndex(80, [100, 90, 80, 70, 60, 50, 0], 6));
        self.assertEqual(3, jbg.computeColorIndex(79.999, [100, 90, 80, 70, 60, 50, 0], 6));
        self.assertEqual(3, jbg.computeColorIndex(70, [100, 90, 80, 70, 60, 50, 0], 6));
        self.assertEqual(4, jbg.computeColorIndex(69.999, [100, 90, 80, 70, 60, 50, 0], 6));
        self.assertEqual(4, jbg.computeColorIndex(60, [100, 90, 80, 70, 60, 50, 0], 6));
        self.assertEqual(5, jbg.computeColorIndex(59.999, [100, 90, 80, 70, 60, 50, 0], 6));
        self.assertEqual(5, jbg.computeColorIndex(50, [100, 90, 80, 70, 60, 50, 0], 6));
        # too few cutoffs
        self.assertEqual(0, jbg.computeColorIndex(100, [100, 90, 80, 70], 6));
        self.assertEqual(0, jbg.computeColorIndex(100.0, [100, 90, 80, 70], 6));
        self.assertEqual(1, jbg.computeColorIndex(99.999, [100, 90, 80, 70], 6));
        self.assertEqual(1, jbg.computeColorIndex(90, [100, 90, 80, 70], 6));
        self.assertEqual(2, jbg.computeColorIndex(89.999, [100, 90, 80, 70], 6));
        self.assertEqual(2, jbg.computeColorIndex(80, [100, 90, 80, 70], 6));
        self.assertEqual(3, jbg.computeColorIndex(79.999, [100, 90, 80, 70], 6));
        self.assertEqual(3, jbg.computeColorIndex(70, [100, 90, 80, 70], 6));
        self.assertEqual(4, jbg.computeColorIndex(69.999, [100, 90, 80, 70], 6));
        self.assertEqual(4, jbg.computeColorIndex(60, [100, 90, 80, 70], 6));
        self.assertEqual(4, jbg.computeColorIndex(59.999, [100, 90, 80, 70], 6));
        self.assertEqual(4, jbg.computeColorIndex(50, [100, 90, 80, 70], 6));
        # only 1 cutoff
        self.assertEqual(0, jbg.computeColorIndex(100, [100], 6));
        self.assertEqual(0, jbg.computeColorIndex(100.0, [100], 6));
        self.assertEqual(1, jbg.computeColorIndex(99.999, [100], 6));
        self.assertEqual(1, jbg.computeColorIndex(90, [100], 6));
        self.assertEqual(1, jbg.computeColorIndex(89.999, [100], 6));
        self.assertEqual(1, jbg.computeColorIndex(80, [100], 6));
        self.assertEqual(1, jbg.computeColorIndex(79.999, [100], 6));
        self.assertEqual(1, jbg.computeColorIndex(70, [100], 6));
        self.assertEqual(1, jbg.computeColorIndex(69.999, [100], 6));
        self.assertEqual(1, jbg.computeColorIndex(60, [100], 6));
        self.assertEqual(1, jbg.computeColorIndex(59.999, [100], 6));
        self.assertEqual(1, jbg.computeColorIndex(50, [100], 6));
        # no cutoffs
        self.assertEqual(0, jbg.computeColorIndex(100, [], 6));
        self.assertEqual(0, jbg.computeColorIndex(100.0, [], 6));
        self.assertEqual(0, jbg.computeColorIndex(99.999, [], 6));
        self.assertEqual(0, jbg.computeColorIndex(90, [], 6));
        self.assertEqual(0, jbg.computeColorIndex(89.999, [], 6));
        self.assertEqual(0, jbg.computeColorIndex(80, [], 6));
        self.assertEqual(0, jbg.computeColorIndex(79.999, [], 6));
        self.assertEqual(0, jbg.computeColorIndex(70, [], 6));
        self.assertEqual(0, jbg.computeColorIndex(69.999, [], 6));
        self.assertEqual(0, jbg.computeColorIndex(60, [], 6));
        self.assertEqual(0, jbg.computeColorIndex(59.999, [], 6));
        self.assertEqual(0, jbg.computeColorIndex(50, [], 6));
        
    def testBadgeGeneration(self) :
        testPercentages = [0, 0.599, 0.6, 0.7, 0.8, 0.899, 0.9, 0.99, 0.999, 1]
        expectedFiles = [ "tests/0.svg",
                          "tests/599.svg",
                          "tests/60.svg",
                          "tests/70.svg",
                          "tests/80.svg",
                          "tests/899.svg",
                          "tests/90.svg",
                          "tests/99.svg",
                          "tests/999.svg",
                          "tests/100.svg"
                          ]
        for i, cov in enumerate(testPercentages) :
            covStr, color = jbg.badgeCoverageStringColorPair(cov)
            badge = jbg.generateBadge(covStr, color)
            with open(expectedFiles[i],"r") as f :
                self.assertEqual(f.read(), badge, msg=expectedFiles[i])
        covStr, color = jbg.badgeCoverageStringColorPair(0.999)
        badge = jbg.generateBadge(covStr, color, "branches")
        with open("tests/999b.svg","r") as f :
            self.assertEqual(f.read(), badge)

    def testCustomBadgeLabels(self) :
        covStr, color = jbg.badgeCoverageStringColorPair(1.0)
        badge = jbg.generateBadge(covStr, color, "custom coverage label one")
        with open("tests/custom1.svg","r") as f :
            self.assertEqual(f.read(), badge)
        covStr, color = jbg.badgeCoverageStringColorPair(0.9)
        badge = jbg.generateBadge(covStr, color, "custom coverage label two")
        with open("tests/custom2.svg","r") as f :
            self.assertEqual(f.read(), badge)

    def testGenerateDictionaryForEndpoint(self) :
        testPercentages = [0, 0.599, 0.6, 0.7, 0.8, 0.899, 0.9, 0.99, 0.999, 1]
        expectedMsg = ["0%", "59.9%", "60%", "70%", "80%", "89.9%", "90%", "99%", "99.9%", "100%"]
        expectedColor = [
            jbg.defaultColors[5],
            jbg.defaultColors[5],
            jbg.defaultColors[4],
            jbg.defaultColors[3],
            jbg.defaultColors[2],
            jbg.defaultColors[2],
            jbg.defaultColors[1],
            jbg.defaultColors[1],
            jbg.defaultColors[1],
            jbg.defaultColors[0]
            ]
        for i, cov in enumerate(testPercentages) :
            covStr, color = jbg.badgeCoverageStringColorPair(cov)
            d = jbg.generateDictionaryForEndpoint(covStr, color, "coverage")
            self.assertEqual(1, d["schemaVersion"])
            self.assertEqual("coverage", d["label"])
            self.assertEqual(expectedMsg[i], d["message"])
            self.assertEqual(expectedColor[i], d["color"])
            d = jbg.generateDictionaryForEndpoint(covStr, color, "branches")
            self.assertEqual(1, d["schemaVersion"])
            self.assertEqual("branches", d["label"])
            self.assertEqual(expectedMsg[i], d["message"])
            self.assertEqual(expectedColor[i], d["color"])

    def testSplitPath(self) :
        cases = [ ( "./jacoco.svg", ".", "jacoco.svg" ),
                  ( "/jacoco.svg", ".", "jacoco.svg" ),
                  ( "jacoco.svg", ".", "jacoco.svg" ),
                  ( "./a/jacoco.svg", "a", "jacoco.svg" ),
                  ( "/a/jacoco.svg", "a", "jacoco.svg" ),
                  ( "a/jacoco.svg", "a", "jacoco.svg" ),
                  ( "./a/b/jacoco.svg", "a/b", "jacoco.svg" ),
                  ( "/a/b/jacoco.svg", "a/b", "jacoco.svg" ),
                  ( "a/b/jacoco.svg", "a/b", "jacoco.svg" )
                  ]
        for testcase, directoryExpected, filenameExpected in cases :
            directory, filename = jbg.splitPath(testcase)
            self.assertEqual(directoryExpected, directory)
            self.assertEqual(filenameExpected, filename)

    def testFormPath(self) :
        cases = [ ( ".", "jacoco.svg", "jacoco.svg" ),
                  ( "./", "jacoco.svg", "jacoco.svg" ),
                  ( "/", "jacoco.svg", "jacoco.svg" ),
                  ( "", "jacoco.svg", "jacoco.svg" ),
                  ( ".", "/jacoco.svg", "jacoco.svg" ),
                  ( "./", "/jacoco.svg", "jacoco.svg" ),
                  ( "/", "/jacoco.svg", "jacoco.svg" ),
                  ( "", "/jacoco.svg", "jacoco.svg" ),
                  ( "./a", "jacoco.svg", "a/jacoco.svg" ),
                  ( "./a/", "jacoco.svg", "a/jacoco.svg" ),
                  ( "/a", "jacoco.svg", "a/jacoco.svg" ),
                  ( "/a/", "jacoco.svg", "a/jacoco.svg" ),
                  ( "a", "jacoco.svg", "a/jacoco.svg" ),
                  ( "a/", "jacoco.svg", "a/jacoco.svg" ),
                  ( "./a", "/jacoco.svg", "a/jacoco.svg" ),
                  ( "./a/", "/jacoco.svg", "a/jacoco.svg" ),
                  ( "/a", "/jacoco.svg", "a/jacoco.svg" ),
                  ( "/a/", "/jacoco.svg", "a/jacoco.svg" ),
                  ( "a", "/jacoco.svg", "a/jacoco.svg" ),
                  ( "a/", "/jacoco.svg", "a/jacoco.svg" ),
                  ( "./a/b", "jacoco.svg", "a/b/jacoco.svg" ),
                  ( "./a/b/", "jacoco.svg", "a/b/jacoco.svg" ),
                  ( "/a/b", "jacoco.svg", "a/b/jacoco.svg" ),
                  ( "/a/b/", "jacoco.svg", "a/b/jacoco.svg" ),
                  ( "a/b", "jacoco.svg", "a/b/jacoco.svg" ),
                  ( "a/b/", "jacoco.svg", "a/b/jacoco.svg" ),
                  ( "./a/b", "/jacoco.svg", "a/b/jacoco.svg" ),
                  ( "./a/b/", "/jacoco.svg", "a/b/jacoco.svg" ),
                  ( "/a/b", "/jacoco.svg", "a/b/jacoco.svg" ),
                  ( "/a/b/", "/jacoco.svg", "a/b/jacoco.svg" ),
                  ( "a/b", "/jacoco.svg", "a/b/jacoco.svg" ),
                  ( "a/b/", "/jacoco.svg", "a/b/jacoco.svg" )
                  ]
        for directory, filename, expected in cases :
            self.assertEqual(expected, jbg.formFullPathToFile(directory, filename))
            
    def testStringToFloatCutoffs(self) :
        self.assertEqual([100, 90, 80, 70, 60, 0], jbg.colorCutoffsStringToNumberList('100, 90, 80, 70, 60, 0'))
        self.assertEqual([100, 90, 80, 70, 60, 0], jbg.colorCutoffsStringToNumberList('100 90 80 70 60 0'))
        self.assertEqual([100, 90, 80, 70, 60, 0], jbg.colorCutoffsStringToNumberList('100,90,80,70,60,0'))
        self.assertEqual([], jbg.colorCutoffsStringToNumberList(''))
        self.assertEqual([], jbg.colorCutoffsStringToNumberList(','))
        self.assertEqual([], jbg.colorCutoffsStringToNumberList('   '))
        self.assertEqual([99.9], jbg.colorCutoffsStringToNumberList('99.9'))
        self.assertEqual([99.9], jbg.colorCutoffsStringToNumberList('99.9,'))
