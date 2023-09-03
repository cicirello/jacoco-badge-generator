# jacoco-badge-generator: Coverage badges, and pull request coverage checks,
# from JaCoCo reports in GitHub Actions.
# 
# Copyright (c) 2020-2023 Vincent A Cicirello
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

import argparse
from .coverage_badges import stringToPercentage
from .coverage_badges import main

if __name__ == "__main__" :
    # IMPORTANT: This is the entrypoint for the use-case of
    # running as a command-line utility only.
    #
    # This is the entry point when using the
    # jacoco-badge-generator as a command-line tool,
    # such as via a build script, locally (and not via
    # GitHub Actions). The source code for the entry
    # point for GitHub Actions is found at src/entrypoint.py,
    # although please see the project README.md for detailed
    # usage within an GitHub Actions workflow.

    print("jacoco-badge-generator: Generate coverage badges from JaCoCo coverage reports")
    print("Copyright (C) 2022-2023 Vincent A. Cicirello (https://www.cicirello.org/)")
    print("MIT License: https://github.com/cicirello/jacoco-badge-generator/blob/main/LICENSE")
    print()

    parser = argparse.ArgumentParser(
        prog="jacoco-badge-generator",
        description="Generate coverage badges from JaCoCo coverage reports. All parameters are optional, provided that the defaults meet your use-case."
    )
    parser.add_argument(
        "-j", "--jacoco-csv-file",
        nargs='+',
        default=["target/site/jacoco/jacoco.csv"],
        help="Filename(s) with full path(s) relative to current working directory of one or more JaCoCo csv reports (default is target/site/jacoco/jacoco.csv).",
        dest="csvReports",
        metavar="report_files"
    )
    parser.add_argument(
        "-d", "--badges-directory",
        default="badges",
        help="Directory for storing the badges relative to current working directory (default: badges), which will be created if it doesn't exist.",
        dest="badgesDirectory",
        metavar="badges-directory"
    )
    parser.add_argument(
        "--generate-coverage-badge",
        default="true",
        help="Controls whether to generate the coverage badge (default: true).",
        dest="generateCoverageBadge",
        choices=['true', 'false']
    )
    parser.add_argument(
        "--coverage-badge-filename",
        default="jacoco.svg",
        help="Filename for the coverage badge (Instructions or C0 Coverage) (default: jacoco.svg), which will be created in the badges directory.",
        dest="coverageFilename",
        metavar="coverage-badge-filename"
    )
    parser.add_argument(
        "--generate-branches-badge",
        default="false",
        help="Controls whether to generate the branches coverage badge (default: false).",
        dest="generateBranchesBadge",
        choices=['true', 'false']
    )
    parser.add_argument(
        "--branches-badge-filename",
        default="branches.svg",
        help="Filename for the branches coverage badge (C1 Coverage) (default: branches.svg), which will be created in the badges directory.",
        dest="branchesFilename",
        metavar="branches-badge-filename"
    )
    parser.add_argument(
        "--generate-coverage-endpoint",
        default="false",
        help="Controls whether to generate a Shields JSON endpoint for coverage (default: false).",
        dest="generateCoverageJSON",
        choices=['true', 'false']
    )
    parser.add_argument(
        "--coverage-endpoint-filename",
        default="jacoco.json",
        help="Filename for the coverage Shields JSON endpoint (Instructions or C0 Coverage) (default: jacoco.json), which will be created in the badges directory.",
        dest="coverageJSON",
        metavar="coverage-endpoint-filename"
    )
    parser.add_argument(
        "--generate-branches-endpoint",
        default="false",
        help="Controls whether to generate a Shields JSON endpoint for branches coverage (default: false).",
        dest="generateBranchesJSON",
        choices=['true', 'false']
    )
    parser.add_argument(
        "--branches-endpoint-filename",
        default="branches.json",
        help="Filename for the branches coverage Shields JSON endpoint (C1 Coverage) (default: branches.json), which will be created in the badges directory.",
        dest="branchesJSON",
        metavar="branches-endpoint-filename"
    )
    parser.add_argument(
        "--generate-summary",
        default="false",
        help="Controls whether or not to generate a simple JSON summary report of the following form: {\"branches\": 77.77777777777779, \"coverage\": 72.72727272727273}. Default: false.",
        dest="generateSummary",
        choices=['true', 'false']
    )
    parser.add_argument(
        "--summary-filename",
        default="coverage-summary.json",
        help="Filename for the summary report (see above). Default: coverage-summary.json, and will be created within the badges directory.",
        dest="summaryFilename",
        metavar="summary-filename"
    )
    parser.add_argument(
        "--coverage-label",
        default="coverage",
        help="Text for the label on the left side of the coverage badge. Default: coverage.",
        dest="coverageLabel",
        metavar="coverage-label"
    )
    parser.add_argument(
        "--branches-label",
        default="branches",
        help="Text for the label on the left side of the branches coverage badge. Default: branches.",
        dest="branchesLabel",
        metavar="branches-label"
    )
    parser.add_argument(
        "--colors",
        nargs="+",
        default=["#4c1", "#97ca00", "#a4a61d", "#dfb317", "#fe7d37", "#e05d44"],
        help="Badge colors in order corresponding to the order of the coverage percentages specified in the --intervals input. Colors can be specified with 6-digit hex, such as #97ca00, or 3-digit hex, such as #4c1, or as SVG named colors, such as green. Default: #4c1 #97ca00 #a4a61d #dfb317 #fe7d37 #e05d44. Depending upon your shell, you may need to escape the # characters or quote each color.",
        dest="colors",
        metavar="color"
    )
    parser.add_argument(
        "--intervals",
        nargs="+",
        default=[100, 90, 80, 70, 60, 0],
        help="Percentages in decreasing order that serve as minimum needed for each color. Order corresponds to that of --colors input. Default: 100 90 80 70 60 0, which means coverage of 100 gets first color, at least 90 gets second color, etc.",
        dest="colorCutoffs",
        metavar="min-coverage-for-color",
        type=float
    )
    parser.add_argument(
        "--on-missing-report",
        default="fail",
        help="Controls what happens if one or more jacoco.csv files do not exist (fail = output error and return non-zero exit code, quiet = exit silently without generating badges and exit code of 0, badges = generate badges from the csv files present (not recommended)). Default: fail.",
        dest="onMissingReport",
        choices=['fail', 'quiet', 'badges']
    )
    parser.add_argument(
        "--fail-if-coverage-less-than",
        default=0,
        help="Don't generate badges and return a non-zero exit code if coverage less than a minimum percentage, specified as value between 0.0 and 1.0, or as a percent (with or without the %% sign). E.g., 0.6, 60, and 60%% are all equivalent. Default: 0.",
        dest="minCoverage",
        metavar="min-coverage",
        type=lambda s : stringToPercentage(s)
    )
    parser.add_argument(
        "--fail-if-branches-less-than",
        default=0,
        help="Don't generate badges and return a non-zero exit code if branches coverage less than a minimum percentage, specified as value between 0.0 and 1.0, or as a percent (with or without the %% sign). E.g., 0.6, 60, and 60%% are all equivalent. Default: 0.",
        dest="minBranches",
        metavar="min-branches",
        type=lambda s : stringToPercentage(s)
    )
    parser.add_argument(
        "--fail-on-coverage-decrease",
        default="false",
        help="If true, will exit with non-zero error code if coverage is less than prior run as recorded in either the existing badge, the existing Shields endpoint, or the JSON summary report (default: false).",
        dest="failOnCoverageDecrease",
        choices=['true', 'false']
    )
    parser.add_argument(
        "--fail-on-branches-decrease",
        default="false",
        help="If true, will exit with non-zero error code if branches coverage is less than prior run as recorded in either the existing badge, the existing Shields endpoint, or the JSON summary report (default: false).",
        dest="failOnBranchesDecrease",
        choices=['true', 'false']
    )
    args = parser.parse_args()

    main(
        jacocoCsvFile = " ".join(args.csvReports),
        badgesDirectory = args.badgesDirectory,
        coverageFilename = args.coverageFilename,
        branchesFilename = args.branchesFilename,
        generateCoverageBadge = args.generateCoverageBadge == "true",
        generateBranchesBadge = args.generateBranchesBadge == "true",
        onMissingReport = args.onMissingReport,
        minCoverage = args.minCoverage,
        minBranches = args.minBranches,
        failOnCoverageDecrease = args.failOnCoverageDecrease == "true",
        failOnBranchesDecrease = args.failOnBranchesDecrease == "true",
        colorCutoffs = args.colorCutoffs,
        colors = args.colors,
        generateCoverageJSON = args.generateCoverageJSON == "true",
        generateBranchesJSON = args.generateBranchesJSON == "true",
        coverageJSON = args.coverageJSON,
        branchesJSON = args.branchesJSON,
        generateSummary = args.generateSummary == "true",
        summaryFilename = args.summaryFilename,
        appendWorkflowSummary = False,
        coverageLabel = args.coverageLabel,
        branchesLabel = args.branchesLabel,
        ghActionsMode = False
    )
