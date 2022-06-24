#!/usr/bin/env -S python3 -B
#
# jacoco-badge-generator: Coverage badges, and pull request coverage checks,
# from JaCoCo reports in GitHub Actions.
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

from jacoco_badge_generator import main
import sys

if __name__ == "__main__" :
    main(
        jacocoCsvFile = sys.argv[1],
        badgesDirectory = sys.argv[2],
        coverageFilename = sys.argv[3],
        branchesFilename = sys.argv[4],
        generateCoverageBadge = sys.argv[5].lower() == "true",
        generateBranchesBadge = sys.argv[6].lower() == "true",
        onMissingReport = sys.argv[7].lower(),
        minCoverage = stringToPercentage(sys.argv[8]),
        minBranches = stringToPercentage(sys.argv[9]),
        failOnCoverageDecrease = sys.argv[10].lower() == "true",
        failOnBranchesDecrease = sys.argv[11].lower() == "true",
        colorCutoffs = colorCutoffsStringToNumberList(sys.argv[12]),
        colors = sys.argv[13].replace(',', ' ').split(),
        generateCoverageJSON = sys.argv[14].lower() == "true",
        generateBranchesJSON = sys.argv[15].lower() == "true",
        coverageJSON = sys.argv[16],
        branchesJSON = sys.argv[17],
        generateSummary = sys.argv[18].lower() == "true",
        summaryFilename = sys.argv[19],
        coverageLabel = sys.argv[20],
        branchesLabel = sys.argv[21]
    )
