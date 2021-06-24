#!/usr/bin/env python3
#
# jacoco-badge-generator: Github action for generating a jacoco coverage
# percentage badge.
# 
# Copyright (c) 2020-2021 Vincent A Cicirello
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
import JacocoBadgeGenerator as jbg

class TestJacocoBadgeGenerator(unittest.TestCase) :

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
        self.assertEqual(jbg.colors[0], jbg.badgeCoverageStringColorPair(1)[1])
        self.assertEqual(jbg.colors[0], jbg.badgeCoverageStringColorPair(1.0)[1])
        self.assertEqual(jbg.colors[1], jbg.badgeCoverageStringColorPair(0.99999)[1])
        self.assertEqual(jbg.colors[1], jbg.badgeCoverageStringColorPair(0.9)[1])
        self.assertEqual(jbg.colors[2], jbg.badgeCoverageStringColorPair(0.89999)[1])
        self.assertEqual(jbg.colors[2], jbg.badgeCoverageStringColorPair(0.8)[1])
        self.assertEqual(jbg.colors[3], jbg.badgeCoverageStringColorPair(0.79999)[1])
        self.assertEqual(jbg.colors[3], jbg.badgeCoverageStringColorPair(0.7)[1])
        self.assertEqual(jbg.colors[4], jbg.badgeCoverageStringColorPair(0.69999)[1])
        self.assertEqual(jbg.colors[4], jbg.badgeCoverageStringColorPair(0.6)[1])
        self.assertEqual(jbg.colors[5], jbg.badgeCoverageStringColorPair(0.59999)[1])
        self.assertEqual(jbg.colors[5], jbg.badgeCoverageStringColorPair(0.0)[1])
        self.assertEqual(jbg.colors[5], jbg.badgeCoverageStringColorPair(0)[1])

    def testColorIndex(self):
        self.assertEquals(0, jbg.computeColorIndex(100, [100, 90, 80, 70, 60]));
        self.assertEquals(0, jbg.computeColorIndex(100.0, [100, 90, 80, 70, 60]));
        self.assertEquals(1, jbg.computeColorIndex(99.999, [100, 90, 80, 70, 60]));
        self.assertEquals(1, jbg.computeColorIndex(90, [100, 90, 80, 70, 60]));
        self.assertEquals(2, jbg.computeColorIndex(89.999, [100, 90, 80, 70, 60]));
        self.assertEquals(2, jbg.computeColorIndex(80, [100, 90, 80, 70, 60]));
        self.assertEquals(3, jbg.computeColorIndex(79.999, [100, 90, 80, 70, 60]));
        self.assertEquals(3, jbg.computeColorIndex(70, [100, 90, 80, 70, 60]));
        self.assertEquals(4, jbg.computeColorIndex(69.999, [100, 90, 80, 70, 60]));
        self.assertEquals(4, jbg.computeColorIndex(60, [100, 90, 80, 70, 60]));
        self.assertEquals(5, jbg.computeColorIndex(59.999, [100, 90, 80, 70, 60]));
        self.assertEquals(5, jbg.computeColorIndex(50, [100, 90, 80, 70, 60]));
        # more cutoffs than necessary
        self.assertEquals(0, jbg.computeColorIndex(100, [100, 90, 80, 70, 60, 50]));
        self.assertEquals(0, jbg.computeColorIndex(100.0, [100, 90, 80, 70, 60, 50]));
        self.assertEquals(1, jbg.computeColorIndex(99.999, [100, 90, 80, 70, 60, 50]));
        self.assertEquals(1, jbg.computeColorIndex(90, [100, 90, 80, 70, 60, 50]));
        self.assertEquals(2, jbg.computeColorIndex(89.999, [100, 90, 80, 70, 60, 50]));
        self.assertEquals(2, jbg.computeColorIndex(80, [100, 90, 80, 70, 60, 50]));
        self.assertEquals(3, jbg.computeColorIndex(79.999, [100, 90, 80, 70, 60, 50]));
        self.assertEquals(3, jbg.computeColorIndex(70, [100, 90, 80, 70, 60, 50]));
        self.assertEquals(4, jbg.computeColorIndex(69.999, [100, 90, 80, 70, 60, 50]));
        self.assertEquals(4, jbg.computeColorIndex(60, [100, 90, 80, 70, 60, 50]));
        self.assertEquals(5, jbg.computeColorIndex(59.999, [100, 90, 80, 70, 60, 50]));
        self.assertEquals(5, jbg.computeColorIndex(50, [100, 90, 80, 70, 60, 50]));
        # even more cutoffs than necessary
        self.assertEquals(0, jbg.computeColorIndex(100, [100, 90, 80, 70, 60, 50, 0]));
        self.assertEquals(0, jbg.computeColorIndex(100.0, [100, 90, 80, 70, 60, 50, 0]));
        self.assertEquals(1, jbg.computeColorIndex(99.999, [100, 90, 80, 70, 60, 50, 0]));
        self.assertEquals(1, jbg.computeColorIndex(90, [100, 90, 80, 70, 60, 50, 0]));
        self.assertEquals(2, jbg.computeColorIndex(89.999, [100, 90, 80, 70, 60, 50, 0]));
        self.assertEquals(2, jbg.computeColorIndex(80, [100, 90, 80, 70, 60, 50, 0]));
        self.assertEquals(3, jbg.computeColorIndex(79.999, [100, 90, 80, 70, 60, 50, 0]));
        self.assertEquals(3, jbg.computeColorIndex(70, [100, 90, 80, 70, 60, 50, 0]));
        self.assertEquals(4, jbg.computeColorIndex(69.999, [100, 90, 80, 70, 60, 50, 0]));
        self.assertEquals(4, jbg.computeColorIndex(60, [100, 90, 80, 70, 60, 50, 0]));
        self.assertEquals(5, jbg.computeColorIndex(59.999, [100, 90, 80, 70, 60, 50, 0]));
        self.assertEquals(5, jbg.computeColorIndex(50, [100, 90, 80, 70, 60, 50, 0]));
        # too few cutoffs
        self.assertEquals(0, jbg.computeColorIndex(100, [100, 90, 80, 70]));
        self.assertEquals(0, jbg.computeColorIndex(100.0, [100, 90, 80, 70]));
        self.assertEquals(1, jbg.computeColorIndex(99.999, [100, 90, 80, 70]));
        self.assertEquals(1, jbg.computeColorIndex(90, [100, 90, 80, 70]));
        self.assertEquals(2, jbg.computeColorIndex(89.999, [100, 90, 80, 70]));
        self.assertEquals(2, jbg.computeColorIndex(80, [100, 90, 80, 70]));
        self.assertEquals(3, jbg.computeColorIndex(79.999, [100, 90, 80, 70]));
        self.assertEquals(3, jbg.computeColorIndex(70, [100, 90, 80, 70]));
        self.assertEquals(4, jbg.computeColorIndex(69.999, [100, 90, 80, 70]));
        self.assertEquals(4, jbg.computeColorIndex(60, [100, 90, 80, 70]));
        self.assertEquals(4, jbg.computeColorIndex(59.999, [100, 90, 80, 70]));
        self.assertEquals(4, jbg.computeColorIndex(50, [100, 90, 80, 70]));
        # only 1 cutoff
        self.assertEquals(0, jbg.computeColorIndex(100, [100]));
        self.assertEquals(0, jbg.computeColorIndex(100.0, [100]));
        self.assertEquals(1, jbg.computeColorIndex(99.999, [100]));
        self.assertEquals(1, jbg.computeColorIndex(90, [100]));
        self.assertEquals(1, jbg.computeColorIndex(89.999, [100]));
        self.assertEquals(1, jbg.computeColorIndex(80, [100]));
        self.assertEquals(1, jbg.computeColorIndex(79.999, [100]));
        self.assertEquals(1, jbg.computeColorIndex(70, [100]));
        self.assertEquals(1, jbg.computeColorIndex(69.999, [100]));
        self.assertEquals(1, jbg.computeColorIndex(60, [100]));
        self.assertEquals(1, jbg.computeColorIndex(59.999, [100]));
        self.assertEquals(1, jbg.computeColorIndex(50, [100]));
        # no cutoffs
        self.assertEquals(0, jbg.computeColorIndex(100, []));
        self.assertEquals(0, jbg.computeColorIndex(100.0, []));
        self.assertEquals(0, jbg.computeColorIndex(99.999, []));
        self.assertEquals(0, jbg.computeColorIndex(90, []));
        self.assertEquals(0, jbg.computeColorIndex(89.999, []));
        self.assertEquals(0, jbg.computeColorIndex(80, []));
        self.assertEquals(0, jbg.computeColorIndex(79.999, []));
        self.assertEquals(0, jbg.computeColorIndex(70, []));
        self.assertEquals(0, jbg.computeColorIndex(69.999, []));
        self.assertEquals(0, jbg.computeColorIndex(60, []));
        self.assertEquals(0, jbg.computeColorIndex(59.999, []));
        self.assertEquals(0, jbg.computeColorIndex(50, []));
        
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
                self.assertEqual(f.read(), badge)
        covStr, color = jbg.badgeCoverageStringColorPair(0.999)
        badge = jbg.generateBadge(covStr, color, "branches")
        with open("tests/999b.svg","r") as f :
            self.assertEqual(f.read(), badge)

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
            
                  
                          
