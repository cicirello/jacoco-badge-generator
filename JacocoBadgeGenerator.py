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

import csv
import sys
import math
import pathlib
import os

badgeTemplate = '<svg xmlns="http://www.w3.org/2000/svg" width="104" \
height="20" role="img" aria-label="coverage: {0}">\
<linearGradient id="s" x2="0" y2="100%">\
<stop offset="0" stop-color="#bbb" stop-opacity=".1"/>\
<stop offset="1" stop-opacity=".1"/></linearGradient><clipPath id="r">\
<rect width="104" height="20" rx="3" fill="#fff"/></clipPath>\
<g clip-path="url(#r)"><rect width="61" height="20" fill="#555"/>\
<rect x="61" width="43" height="20" fill="{1}"/>\
<rect width="104" height="20" fill="url(#s)"/></g>\
<g fill="#fff" text-anchor="middle" \
font-family="Verdana,Geneva,DejaVu Sans,sans-serif" \
text-rendering="geometricPrecision" font-size="110">\
<text aria-hidden="true" x="315" y="150" fill="#010101" \
fill-opacity=".3" transform="scale(.1)" textLength="510">coverage</text>\
<text x="315" y="140" transform="scale(.1)" fill="#fff" \
textLength="510">coverage</text>\
<text aria-hidden="true" x="815" y="150" \
fill="#010101" fill-opacity=".3" transform="scale(.1)" \
textLength="{2}">{0}</text><text x="815" y="140" \
transform="scale(.1)" fill="#fff" textLength="{2}">{0}</text>\
</g></svg>'

colors = [ "#4c1", "#97ca00", "#a4a61d", "#dfb317", "#fe7d37", "#e05d44" ]

def generateBadge(covStr, color) :
    """Generates the badge as a string.

    Keyword arguments:
    covStr - The coverage as a string.
    color - The color for the badge.
    """
    if len(covStr) >= 4 :
        textLength = "330"
    elif len(covStr) >= 3 :
        textLength = "250" 
    else :
        textLength = "170"
    return badgeTemplate.format(covStr, color, textLength)

def computeCoverage(filename) :
    """Parses a jacoco.csv file and computes code coverage
    percentage.

    Keyword arguments:
    filename - The name, including path, of the jacoco.csv
    """
    missed = 0
    covered = 0
    with open(filename, newline='') as csvfile :
        jacocoReader = csv.reader(csvfile)
        for i, row in enumerate(jacocoReader) :
            if i > 0 :
                missed += int(row[3])
                covered += int(row[4])
    return covered / (covered + missed)

def badgeCoverageStringColorPair(coverage) :
    """Converts the coverage percentage to a formatted string,
    and determines the badge color.
    Returns: coveragePercentageAsString, colorAsString

    Keyword arguments:
    coverage - The coverage percentage.
    """
    # Truncate the 2nd decimal place, rather than rounding
    # to avoid considering a non-passing percentage as
    # passing (e.g., if user considers 70% as passing threshold,
    # then 69.99999...% is technically not passing).
    coverage = int(1000 * coverage) / 10
    c = math.ceil((100 - coverage) / 10)
    if c >= len(colors) :
        c = len(colors) - 1
    if coverage - int(coverage) == 0 :
        cov = "{0:d}%".format(int(coverage))
    else :
        cov = "{0:.1f}%".format(coverage)
    return cov, colors[c]

def createOutputDirectories(jacocoBadgeFile) :
    """Creates the output directory if it doesn't already exist.

    Keyword arguments:
    jacocoBadgeFile - The path, including filename, to the output badge file.
    """
    if not os.path.exists(jacocoBadgeFile) :
        p = pathlib.Path(os.path.dirname(jacocoBadgeFile))
        p.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__" :
    jacocoCsvFile = sys.argv[1]
    jacocoBadgeFile = sys.argv[2]

    cov = computeCoverage(jacocoCsvFile)
    covStr, color = badgeCoverageStringColorPair(cov)
    createOutputDirectories(jacocoBadgeFile)
    with open(jacocoBadgeFile, "w") as badge :
        badge.write(generateBadge(covStr, color))

    print("::set-output name=coverage::" + str(cov))
    
    


                
            
