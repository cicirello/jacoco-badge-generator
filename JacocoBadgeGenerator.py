#!/usr/bin/env python3
#
# jacoco-badge-generator: Coverage badges, and pull request coverage checks,
# from JaCoCo reports in GitHub Actions.
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

import csv
import sys
import math
import pathlib
import os
import os.path
import json
from pybadges import badge


defaultColors = [ "#4c1", "#97ca00", "#a4a61d", "#dfb317", "#fe7d37", "#e05d44" ]

def generateBadge(covStr, color, badgeType) :
    """Generates the badge as a string.

    Keyword arguments:
    covStr - The coverage as a string.
    color - The color for the badge.
    badgeType - The text string for a label on the badge.
    """
    return badge(left_text=badgeType, right_text=covStr, right_color=color)

def generateDictionaryForEndpoint(covStr, color, badgeType) :
    """Generated a Python dictionary containing all of the required
    fields for a Shields.io JSON endpoint.

    Keyword arguments:
    covStr - The coverage as a string.
    color - The color for the badge.
    badgeType - The text string for a label on the badge.
    """
    return {
        "schemaVersion" : 1,
        "label" : badgeType,
        "message" : covStr,
        "color" : color
        }

def computeCoverage(fileList) :
    """Parses one or more jacoco.csv files and computes code coverage
    percentages. Returns: coverage, branchCoverage.  The coverage
    is instruction coverage.

    Keyword arguments:
    fileList - A list (or any iterable) of the filenames, including path, of the jacoco.csv files.
    """
    missed = 0
    covered = 0
    missedBranches = 0
    coveredBranches = 0
    for filename in fileList :
        with open(filename, newline='') as csvfile :
            jacocoReader = csv.reader(csvfile)
            for i, row in enumerate(jacocoReader) :
                if i > 0 :
                    missed += int(row[3])
                    covered += int(row[4])
                    missedBranches += int(row[5])
                    coveredBranches += int(row[6])
    return (calculatePercentage(covered, missed),
            calculatePercentage(coveredBranches, missedBranches))

def calculatePercentage(covered, missed) :
    """Calculates the coverage percentage from number of
    covered and number of missed. Returns 1 if both are 0
    to handle the special case of running on an empty class
    (no instructions) or a case with no if, switch, loops (no
    branches).

    Keyword arguments:
    covered - The number of X covered (where X is the metric).
    missed - The number of X missed (where X is the metric).
    """
    if missed == 0 :
        return 1
    return covered / (covered + missed)

def coverageTruncatedToString(coverage) :
    """Converts the coverage percentage to a formatted string.
    Returns: coveragePercentageAsString, coverageTruncatedToOneDecimalPlace

    Keyword arguments:
    coverage - The coverage percentage.
    """
    # Truncate the 2nd decimal place, rather than rounding
    # to avoid considering a non-passing percentage as
    # passing (e.g., if user considers 70% as passing threshold,
    # then 69.99999...% is technically not passing).
    coverage = int(1000 * coverage) / 10
    if coverage - int(coverage) == 0 :
        covStr = "{0:d}%".format(int(coverage))
    else :
        covStr = "{0:.1f}%".format(coverage)
    return covStr, coverage

def badgeCoverageStringColorPair(coverage, cutoffs=[100, 90, 80, 70, 60], colors=[]) :
    """Converts the coverage percentage to a formatted string,
    and determines the badge color.
    Returns: coveragePercentageAsString, colorAsString

    Keyword arguments:
    coverage - The coverage percentage.
    cutoffs - List of percentages that begin begin each color interval.
    colors - List of badge colors in decreasing order of coverage percentages.
    """
    if len(colors) == 0 :
        colors = defaultColors
    cov, coverage = coverageTruncatedToString(coverage)
    c = computeColorIndex(coverage, cutoffs, len(colors))
    return cov, colors[c]

def computeColorIndex(coverage, cutoffs, numColors) :
    """Computes index into color list from coverage.

    Keyword arguments:
    coverage - The coverage percentage.
    cutoffs - The thresholds for each color.
    """
    numIntervals = min(numColors, len(cutoffs)+1)
    for c in range(numIntervals-1) :
        if coverage >= cutoffs[c] :
            return c
    return numIntervals-1

def createOutputDirectories(badgesDirectory) :
    """Creates the output directory if it doesn't already exist.

    Keyword arguments:
    badgesDirectory - The badges directory
    """
    if not os.path.exists(badgesDirectory) :
        p = pathlib.Path(badgesDirectory)
        os.umask(0)
        p.mkdir(mode=0o777, parents=True, exist_ok=True)

def splitPath(filenameWithPath) :
    """Breaks a filename including path into containing directory and filename.

    Keyword arguments:
    filenameWithPath - The filename including path.
    """
    if filenameWithPath.startswith("./") :
        filenameWithPath = filenameWithPath[2:]
    if filenameWithPath[0] == "/" :
        filenameWithPath = filenameWithPath[1:]
    i = filenameWithPath.rfind("/")
    if i >= 0 :
        return filenameWithPath[:i], filenameWithPath[i+1:]
    else :
        return ".", filenameWithPath

def formFullPathToFile(directory, filename) :
    """Generates path string.

    Keyword arguments:
    directory - The directory for the badges
    filename - The filename for the badge.
    """
    if len(filename) > 1 and filename[0:2] == "./" :
        filename = filename[2:]
    if filename[0] == "/" :
        filename = filename[1:]
    if len(directory) > 1 and directory[0:2] == "./" :
        directory = directory[2:]
    if len(directory) > 0 and directory[0] == "/" :
        directory = directory[1:]
    if directory == "" or directory == "." :
        return filename
    elif directory[-1] == "/" :
        return directory + filename
    else :
        return directory + "/" + filename

def filterMissingReports(jacocoFileList, failIfMissing=False) :
    """Validates report file existence, and returns a list
    containing a subset of the report files that exist. Logs
    files that don't exist to the console as warnings.

    Keyword arguments:
    jacocoFileList - A list of jacoco.csv files.
    failIfMissing - If true and if any of the jacoco.csv files
    don't exist, then it will exit with a non-zero exit code causing
    workflow to fail.
    """
    goodReports = []
    for f in jacocoFileList :
        if os.path.exists(f) :
            goodReports.append(f)
        else :
            print("WARNING: Report file", f, "does not exist.")
    if len(goodReports) == 0 :
        print("WARNING: No JaCoCo csv reports found.")
        if failIfMissing :
            sys.exit(1)
    if failIfMissing and len(goodReports) != len(jacocoFileList) :
        sys.exit(1)
    return goodReports

def stringToPercentage(s) :
    """Converts a string describing a percentage to
    a float. The string s can be of any of the following
    forms: 60.2%, 60.2, or 0.602. All three of these will
    be treated the same. Without the percent sign, it is
    treated the same as with the percent sign if the value
    is greater than 1. This is to gracefully handle
    user misinterpretation of action input specification. In all cases,
    this function will return a float in the interval [0.0, 1.0].

    Keyword arguments:
    s - the string to convert.
    """
    if len(s)==0 :
        return 0
    doDivide = False
    if s[-1]=="%" :
        s = s[:-1].strip()
        if len(s)==0 :
            return 0
        doDivide = True
    try :
        p = float(s)
    except ValueError :
        return 0
    if p > 1 :
        doDivide = True
    return p / 100 if doDivide else p

def coverageIsFailing(coverage, branches, minCoverage, minBranches) :
    """Checks if coverage or branchs coverage or both are
    below minimum to pass workflow run. Logs messages if it is.
    Actual failing behavior should be handled by caller.

    Keyword arguments:
    coverage - instructions coverage in interval 0.0 to 1.0.
    branches - branches coverage in interval 0.0 to 1.0.
    minCoverage - minimum instructions coverage to pass in interval 0.0 to 1.0.
    minBranches - minimum branches coverage to pass in interval 0.0 to 1.0.
    """
    shouldFail = False
    if coverage < minCoverage :
        shouldFail = True
        print("Coverage of", coverage, "is below passing threshold of", minCoverage)
    if branches < minBranches :
        shouldFail = True
        print("Branches of", branches, "is below passing threshold of", minBranches)
    return shouldFail

def getPriorCoverage(badgeFilename, whichBadge) :
    """Parses an existing badge (if one exists) returning
    the coverage percentage stored there. Returns -1 if
    badge file doesn't exist or if it isn't of the expected format.

    Keyword arguments:
    badgeFilename - the filename with path
    whichBadge - this input should be one of 'coverage' or 'branches'
    """
    if not os.path.isfile(badgeFilename) :
        return -1
    with open(badgeFilename, "r") as f :
        priorBadge = f.read()
    i = priorBadge.find(whichBadge)
    if i < 0 :
        return -1
    i += len(whichBadge) + 1
    j = priorBadge.find("%", i)
    if j < 0 :
        return -1
    return stringToPercentage(priorBadge[i:j+1].strip())

def getPriorCoverageFromEndpoint(jsonFilename, whichBadge) :
    """Parses an existing JSON endpoint (if one exists) returning
    the coverage percentage stored there. Returns -1 if
    file doesn't exist or if it isn't of the expected format.

    Keyword arguments:
    jsonFilename - the filename with path
    whichBadge - this input should be one of 'coverage' or 'branches'
    """
    if not os.path.isfile(jsonFilename) :
        return -1
    try :
        with open(jsonFilename, "r") as f :
            priorEndpoint = json.load(f)
    except :
        return -1
    if "message" not in priorEndpoint :
        return -1
    if "label" not in priorEndpoint :
        return -1
    if priorEndpoint["label"] != whichBadge :
        return -1
    return stringToPercentage(priorEndpoint["message"].strip())

def coverageDecreased(coverage, badgeFilename, whichBadge) :
    """Checks if coverage decreased relative to previous run, and logs
    a message if it did.

    Keyword arguments:
    coverage - The coverage in interval 0.0 to 1.0
    badgeFilename - the filename with path
    whichBadge - this input should be one of 'coverage' or 'branches'
    """
    previous = getPriorCoverage(badgeFilename, whichBadge)
    # Badge only records 1 decimal place, and thus need
    # to take care to avoid floating-point rounding error
    # when old is converted to [0.0 to 1.0] range with div by
    # 100 in getPriorCoverage.  e.g., 99.9 / 100 = 0.9990000000000001
    # due to rounding error.
    old = round(previous * 1000)
    # Don't need to round with new since this is still as computed
    # from coverage data at this point.
    new = coverage * 1000
    if new < old :
        s = "Branches coverage" if whichBadge == "branches" else "Coverage"
        print(s, "decreased from", coverageTruncatedToString(previous)[0], "to", coverageTruncatedToString(coverage)[0])
        return True
    return False

def coverageDecreasedEndpoint(coverage, jsonFilename, whichBadge) :
    """Checks if coverage decreased relative to previous run, and logs
    a message if it did.

    Keyword arguments:
    coverage - The coverage in interval 0.0 to 1.0
    jsonFilename - the filename with path
    whichBadge - this input should be one of 'coverage' or 'branches'
    """
    previous = getPriorCoverageFromEndpoint(jsonFilename, whichBadge)
    # Badge only records 1 decimal place, and thus need
    # to take care to avoid floating-point rounding error
    # when old is converted to [0.0 to 1.0] range with div by
    # 100 in getPriorCoverage.  e.g., 99.9 / 100 = 0.9990000000000001
    # due to rounding error.
    old = round(previous * 1000)
    # Don't need to round with new since this is still as computed
    # from coverage data at this point.
    new = coverage * 1000
    if new < old :
        s = "Branches coverage" if whichBadge == "branches" else "Coverage"
        print(s, "decreased from", coverageTruncatedToString(previous)[0], "to", coverageTruncatedToString(coverage)[0])
        return True
    return False

def coverageDecreasedSummary(checkCoverage, checkBranches, jsonFile, coverage, branches) :
    """Uses a summary report JSON file for the decreased coverage checks.
    Returns true if workflow should fail, and also logs appropriate message.

    Keyword arguments:
    checkCoverage - If true, check if coverage decreased.
    checkBranches - If true, check if branches coverage decreased.
    jsonFile - The summary report including full path.
    coverage - The instructions coverage in interval [0.0, 1.0].
    branches - The branches coverage in interval [0.0, 1.0].
    """
    if not os.path.isfile(jsonFile) :
        return False
    try :
        with open(jsonFile, "r") as f :
            priorCoverage = json.load(f)
    except :
        return False
    result = False
    if checkCoverage and "coverage" in priorCoverage and 100*coverage < priorCoverage["coverage"] :
        print("Coverage decreased from", priorCoverage["coverage"], "to", 100*coverage)
        result = True
    if checkBranches and "branches" in priorCoverage and 100*branches < priorCoverage["branches"] :
        print("Branches coverage decreased from", priorCoverage["branches"], "to", 100*branches)
        result = True
    return result

def colorCutoffsStringToNumberList(strCutoffs) :
    """Converts a string of space or comma separated percentages
    to a list of floats.

    Keyword arguments:
    strCutoffs - a string of space or comma separated percentages
    """
    return list(map(float, strCutoffs.replace(',', ' ').split()))

def coverageDictionary(cov, branches) :
    """Creates a dictionary with the coverage and branches coverage
    as double-precision floating-point values, specifically the raw
    computed values prior to truncation. Enables more accurate implementation
    of fail on decrease. Coverages are reported in interval [0.0, 100.0].

    Keyword arguments:
    cov - Instruction coverage in interval [0.0, 1.0]
    branches - Branches coverage in interval [0.0, 1.0]
    """
    return { "coverage" : 100 * cov, "branches" : 100 * branches }

if __name__ == "__main__" :
    jacocoCsvFile = sys.argv[1]
    badgesDirectory = sys.argv[2]
    coverageFilename = sys.argv[3]
    branchesFilename = sys.argv[4]
    generateCoverageBadge = sys.argv[5].lower() == "true"
    generateBranchesBadge = sys.argv[6].lower() == "true"
    onMissingReport = sys.argv[7].lower()
    minCoverage = stringToPercentage(sys.argv[8])
    minBranches = stringToPercentage(sys.argv[9])
    failOnCoverageDecrease = sys.argv[10].lower() == "true"
    failOnBranchesDecrease = sys.argv[11].lower() == "true"
    colorCutoffs = colorCutoffsStringToNumberList(sys.argv[12])
    colors = sys.argv[13].replace(',', ' ').split()
    generateCoverageJSON = sys.argv[14].lower() == "true"
    generateBranchesJSON = sys.argv[15].lower() == "true"
    coverageJSON = sys.argv[16]
    branchesJSON = sys.argv[17]
    generateSummary = sys.argv[18].lower() == "true"
    summaryFilename = sys.argv[19]

    if len(sys.argv) > 19:
        badgeText = sys.argv[20]
    else:
        badgeText = "coverage"

    if onMissingReport not in {"fail", "quiet", "badges"} :
        print("ERROR: Invalid value for on-missing-report.")
        sys.exit(1)

    if len(badgesDirectory) > 1 and badgesDirectory[0:2] == "./" :
        badgesDirectory = badgesDirectory[2:]
    if len(badgesDirectory) > 0 and badgesDirectory[0] == "/" :
        badgesDirectory = badgesDirectory[1:]
    if badgesDirectory == "." :
        badgesDirectory = ""

    jacocoFileList = jacocoCsvFile.split()
    filteredFileList = filterMissingReports(jacocoFileList, onMissingReport=="fail")

    noReportsMissing = len(jacocoFileList)==len(filteredFileList)

    if len(filteredFileList) > 0 and (noReportsMissing or onMissingReport!="quiet") :  

        cov, branches = computeCoverage(filteredFileList)

        if coverageIsFailing(cov, branches, minCoverage, minBranches) :
            print("Failing the workflow run.")
            sys.exit(1)

        coverageBadgeWithPath = formFullPathToFile(badgesDirectory, coverageFilename)
        branchesBadgeWithPath = formFullPathToFile(badgesDirectory, branchesFilename)
        coverageJSONWithPath = formFullPathToFile(badgesDirectory, coverageJSON)
        branchesJSONWithPath = formFullPathToFile(badgesDirectory, branchesJSON)
        summaryFilenameWithPath = formFullPathToFile(badgesDirectory, summaryFilename)

        # If using the fail on decrease options, in combination with the summary report, use summary
        # report for the check since it is more accurate.
        if (failOnCoverageDecrease or failOnBranchesDecrease) and generateSummary and os.path.isfile(summaryFilenameWithPath) :
            if coverageDecreasedSummary(failOnCoverageDecrease, failOnBranchesDecrease, summaryFilenameWithPath, cov, branches) :
                print("Failing the workflow run.")
                sys.exit(1)
        else : # Otherwise use the prior coverages as stored in badges / JSON.
            if failOnCoverageDecrease and generateCoverageBadge and coverageDecreased(cov, coverageBadgeWithPath, "coverage") :
                print("Failing the workflow run.")
                sys.exit(1)
            if failOnBranchesDecrease and generateBranchesBadge and coverageDecreased(branches, branchesBadgeWithPath, "branches") :
                print("Failing the workflow run.")
                sys.exit(1)
            if failOnCoverageDecrease and generateCoverageJSON and coverageDecreasedEndpoint(cov, coverageJSONWithPath, "coverage") :
                print("Failing the workflow run.")
                sys.exit(1)
            if failOnBranchesDecrease and generateBranchesJSON and coverageDecreasedEndpoint(branches, branchesJSONWithPath, "branches") :
                print("Failing the workflow run.")
                sys.exit(1)

        if (generateSummary or generateCoverageBadge or generateBranchesBadge or generateCoverageJSON or generateBranchesJSON) and badgesDirectory != "" :
            createOutputDirectories(badgesDirectory)

        if generateCoverageBadge or generateCoverageJSON :
            covStr, color = badgeCoverageStringColorPair(cov, colorCutoffs, colors)
            if generateCoverageBadge :
                with open(coverageBadgeWithPath, "w") as badge :
                    badge.write(generateBadge(covStr, color, badgeText))
            if generateCoverageJSON :
                with open(coverageJSONWithPath, "w") as endpoint :
                    json.dump(generateDictionaryForEndpoint(covStr, color, "coverage"), endpoint, sort_keys=True)

        if generateBranchesBadge or generateBranchesJSON :
            covStr, color = badgeCoverageStringColorPair(branches, colorCutoffs, colors)
            if generateBranchesBadge :
                with open(branchesBadgeWithPath, "w") as badge :
                    badge.write(generateBadge(covStr, color, "branches"))
            if generateBranchesJSON :
                with open(branchesJSONWithPath, "w") as endpoint :
                    json.dump(generateDictionaryForEndpoint(covStr, color, "branches"), endpoint, sort_keys=True)

        if generateSummary :
            with open(summaryFilenameWithPath, "w") as summaryFile :
                json.dump(coverageDictionary(cov, branches), summaryFile, sort_keys=True)

        print("::set-output name=coverage::" + str(cov))
        print("::set-output name=branches::" + str(branches))

