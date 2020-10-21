#!/usr/bin/env python3
#
# jacoco-badge-generator: Github action for generating a jacoco coverage
# percentage badge.
# 
# Copyright (c) 2020 Vincent A Cicirello
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

    def testFullCoverage(self) :
        self.assertAlmostEqual(1, jbg.computeCoverage("tests/jacoco100.csv"))

    def testCoverage90(self) :
        self.assertAlmostEqual(0.9, jbg.computeCoverage("tests/jacoco90.csv"))

    def testCoverage901(self) :
        self.assertAlmostEqual(0.901, jbg.computeCoverage("tests/jacoco901.csv"))
    
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
                          
