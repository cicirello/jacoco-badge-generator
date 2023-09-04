# jacoco-badge-generator

[![cicirello/jacoco-badge-generator - Coverage badges, and pull request coverage checks, from JaCoCo reports in GitHub Actions](https://actions.cicirello.org/images/jacoco-badge-generator640.png)](#jacoco-badge-generator)

Check out all of our GitHub Actions: https://actions.cicirello.org/

## About

| __GitHub Actions__ | [![GitHub release (latest by date)](https://img.shields.io/github/v/release/cicirello/jacoco-badge-generator?label=Marketplace&logo=GitHub)](https://github.com/marketplace/actions/jacoco-badge-generator) [![Count of Action Users](https://badgen.net/runkit/cicirello/jacoco-badge-generator-dependents?icon=github)](https://github.com/cicirello/jacoco-badge-generator/network/dependents?package_id=UGFja2FnZS0yOTQ0NTMxNTI3) |
| :--- | :--- |
| __Command-Line Utility__ | [![PyPI](https://img.shields.io/pypi/v/jacoco-badge-generator?logo=pypi)](https://pypi.org/project/jacoco-badge-generator/) [![PyPI Downloads/month](https://static.pepy.tech/personalized-badge/jacoco-badge-generator?period=month&units=international_system&left_color=grey&right_color=blue&left_text=pypi%20downloads/month)](https://pepy.tech/project/jacoco-badge-generator) [![PyPI Downloads/week](https://static.pepy.tech/personalized-badge/jacoco-badge-generator?period=week&units=international_system&left_color=grey&right_color=blue&left_text=pypi%20downloads/week)](https://pepy.tech/project/jacoco-badge-generator) |
| __Build Status__ | [![build](https://github.com/cicirello/jacoco-badge-generator/actions/workflows/build.yml/badge.svg)](https://github.com/cicirello/jacoco-badge-generator/actions/workflows/build.yml) [![CodeQL](https://github.com/cicirello/jacoco-badge-generator/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/cicirello/jacoco-badge-generator/actions/workflows/codeql-analysis.yml) |
| __Security__ | [![Snyk security score](https://snyk-widget.herokuapp.com/badge/pip/jacoco-badge-generator/badge.svg)](https://snyk.io/vuln/pip%3Ajacoco-badge-generator) |
| __Source Info__ | [![License](https://img.shields.io/github/license/cicirello/jacoco-badge-generator)](https://github.com/cicirello/jacoco-badge-generator/blob/main/LICENSE) ![GitHub top language](https://img.shields.io/github/languages/top/cicirello/jacoco-badge-generator) |
| __Support__ | [![GitHub Sponsors](https://img.shields.io/badge/sponsor-30363D?logo=GitHub-Sponsors&logoColor=#EA4AAA)](https://github.com/sponsors/cicirello) [![Liberapay](https://img.shields.io/badge/Liberapay-F6C915?logo=liberapay&logoColor=black)](https://liberapay.com/cicirello) [![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?logo=ko-fi&logoColor=white)](https://ko-fi.com/cicirello) | 

The jacoco-badge-generator can be used in one of two ways: as a GitHub Action or as a command-line 
utility (e.g., such as part of a local build script). The jacoco-badge-generator parses a `jacoco.csv` 
from a JaCoCo coverage report, computes coverage percentages 
from [JaCoCo's Instructions and Branches counters](https://www.jacoco.org/jacoco/trunk/doc/counters.html), and 
generates badges for one or both of these (user configurable) to provide an easy 
to read visual summary of the code coverage of your test cases. The default behavior directly
generates the badges internally with no external calls, but the action also provides an option
to instead generate [Shields JSON endpoints](#direct-badge-generation-vs-json-endpoint). It supports
both the basic case of a single `jacoco.csv`, as well as multi-module projects in which
case the action can produce coverage badges from the combination of the JaCoCo reports
from all modules, provided that the individual reports are independent. It can also be configured to 
generate a simple JSON file containing the coverages as double-precision floating-point values, either 
instead of or in addition to generating the badges, which may be useful as input to other tools.

When used as a GitHub Action, the jacoco-badge-generator can also optionally be used as part of a pull-request 
check. Specifically, you can configure it to fail the workflow run if coverage decreased relative to prior run, 
and/or if coverage is below a target threshold. See the [Inputs](#inputs) section for details of how to configure 
it for this purpose. 

_The developers of the jacoco-badge-generator are not affiliated with the developers of JaCoCo, although we are a 
fan and user of their excellent test coverage tool._ 

## Table of Contents

The documentation is organized into the following sections:
* [The Coverage Metrics](#the-coverage-metrics): Explains the JaCoCo 
  metrics that are supported by the badge generator, such as what 
  they measure, and why they were chosen for inclusion for 
  the jacoco-badge-generator.
* [Badge Style and Content](#badge-style-and-content): Provides 
  examples of the appearance of the badges that are generated, 
  including a description of the color scheme used, and the 
  formatting of the percentages.
* [GitHub Action Usage](#github-action-usage): Details on how to use the 
  jacoco-badge-generator GitHub Action (its primary use-case).
  * [Inputs](#inputs): Detailed descriptions of the action inputs.
  * [Outputs](#outputs): Detailed descriptions of the action inputs.
  * [Example Workflows](#example-workflows): Example GitHub workflows 
    demonstrating usage of the jacoco-badge-generator action.
  * [Multi-Module Example Workflows](#multi-module-example-workflows): Example 
    GitHub workflows demonstrating usage of the jacoco-badge-generator 
    action with multi-module projects.
  * [Examples in Other Projects](#examples-in-other-projects): Info and a link
    to a template repository that we have setup to provide live runnable workflows
    to get you started; as well as links to a few repositories that are actively
    using the action, as well as direct links to the relevant workflow files.
* [Command-Line Usage](#command-line-usage): Details on how to install and run
  the jacoco-badge-generator as a command-line utility outside of GitHub Actions.
  * [Installing from PyPI](#installing-from-pypi): How to install command-line
    utility from PyPI.
  * [Running for the First Time](#running-for-the-first-time): Command-line utility's
    help menu.
  * [CLI Examples](#cli-examples): Several examples of using the command-line utlity.
* [Summary of Input Defaults](#summary-of-input-defaults): A table summarizing all
  of the inputs, along with the defaults, for both GitHub Actions usage as well as
  CLI usage.
* [Blog Posts](#blog-posts): A selection of blog posts about the GitHub Action.
* [Support the Project](#support-the-project): Information on various 
  ways that you can support the project.


## The Coverage Metrics

The jacoco-badge-generator currently supports generating badges for 
the two primary coverage metrics generated by JaCoCo: Instructions (C0 Coverage), and 
Branches (C1 Coverage). Here is a summary of what these compute and why they were chosen
for inclusion by this badge generator.

### Instructions Coverage (C0 Coverage)

The default behavior of the badge generator is to generate only the Instructions Coverage
badge, which is labeled on the badge simply as "coverage". JaCoCo 
measures [C0 Coverage](https://www.jacoco.org/jacoco/trunk/doc/counters.html)
from the Java bytecode instructions in the compiled `.class` files. One of the advantages
to counting the bytecode instructions executed or missed, rather than lines of source code, 
is that it is independent of coding style and formatting. As a simple example, consider
the sequence of Java statements to swap the values in two 
variables: `int temp = a; a = b; b = temp;`.  A line counter will count this as 1 line if
written on a single line, or 3 lines if each statement is written on its own line. However,
JaCoCo's instructions counter treats these two cases as equivalent since they compile
to the same bytecode. Consider a more complex example of calling a method while passing a simple
value, such as `foo(5)` versus passing the result of a calculation to the method, such as
`foo(2.0 + bar/11.0)`. Line counting considers both of these as 1 line; while the second case
will factor in more heavily into JaCoCo's instruction counting than will the first case. For
these reasons, although JaCoCo also provides line coverage data, we do not currently support
generating a badge from JaCoCo's line counter data. JaCoCo's use of bytecode instructions
in its definition of C0 Coverage is a more meaningful measure of coverage than is counting
lines of code.

### Branches Coverage (C1 Coverage)

The badge generator also optionally supports generating a badge for Branches Coverage
(or C1 Coverage), with the generated badge labeled as "branches".  See 
the [inputs](#inputs) section for a description of the action
inputs.  JaCoCo 
measures [C1 Coverage or Branches Coverage](https://www.jacoco.org/jacoco/trunk/doc/counters.html)
from the Java bytecode in the compiled `.class` files, so the result may be a bit
different than what you might expect from branch coverage. At first, you may even mistakenly
guess that it is counting conditions (C2 coverage) rather than branches, but it is counting
branches (in bytecode rather than in source code). Consider this example to illustrate
the difference: `if (a && b) foo(); else bar();`. If we count branches in source code,
there are 2 branches, which would require a minimum of two tests for full coverage, one where
both `a` and `b` are `true`, and a second test where at least one of them is `false`.
If we instead count conditions, there are 4 conditions (`a==true`, `a==false`, `b==true`, 
`b==false`), which can be covered with as few as two tests (e.g., `a==true` and `b==false`
as test one, and `b==true` and `a==false` as test two), without actually covering both
branches. JaCoCo's branches counter is neither of these. JaCoCo's branches counter
counts branches in the Java bytecode. What does that mean for this example? Imagine instead
that the if statement above was written as a pair of nested if 
statements: `if (a) { if (b) { foo(); } else { bar(); } } else { bar(); }`. There are
a total of 4 branches in this case (and is essentially what JaCoCo would count as branches).
To cover all 4 branches would require a minimum of 3 test cases: one where `a` and `b` are both
`true`, one in which `a` is `true` and `b` is `false`, and a third where `a` is `false` and `b`'s 
value doesn't matter. In this way, JaCoCo's branches counter leads to a stronger form
of C1 Coverage than is usually implied by branches coverage.


## Badge Style and Content

### Default Color Scheme

Here are a few samples of what the badges look like if you use
the default colors:

| Coverage range | Direct badge generation | Badge generation from endpoint |
| :---  | :--- | :--- | 
| Bright green for 100% coverage  | ![Coverage 100%](https://raw.githubusercontent.com/cicirello/jacoco-badge-generator/main/tests/100.svg) | ![Coverage 100%](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cicirello/jacoco-badge-generator/main/tests/100.json) |
| Green for 90% through 99.9% coverage | ![Coverage 99.9%](https://raw.githubusercontent.com/cicirello/jacoco-badge-generator/main/tests/999.svg) | ![Coverage 99.9%](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cicirello/jacoco-badge-generator/main/tests/999.json) |
| Yellow green for 80% through 89.9% coverage | ![Coverage 80%](https://raw.githubusercontent.com/cicirello/jacoco-badge-generator/main/tests/80.svg) | ![Coverage 80%](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cicirello/jacoco-badge-generator/main/tests/80.json) |
| Yellow for 70% through 79.9% coverage | ![Coverage 70%](https://raw.githubusercontent.com/cicirello/jacoco-badge-generator/main/tests/70.svg) | ![Coverage 70%](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cicirello/jacoco-badge-generator/main/tests/70.json) |
| Orange for 60% through 69.9% coverage | ![Coverage 60%](https://raw.githubusercontent.com/cicirello/jacoco-badge-generator/main/tests/60.svg) | ![Coverage 60%](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cicirello/jacoco-badge-generator/main/tests/60.json) |
| Red for 0% through 59.9% coverage | ![Coverage 59.9%](https://raw.githubusercontent.com/cicirello/jacoco-badge-generator/main/tests/599.svg) | ![Coverage 59.9%](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cicirello/jacoco-badge-generator/main/tests/599.json) |
| Sample of a branch coverage badge | ![Branches Coverage 99.9%](https://raw.githubusercontent.com/cicirello/jacoco-badge-generator/main/tests/999b.svg) | ![Branches Coverage 99.9%](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cicirello/jacoco-badge-generator/main/tests/999b.json) |

### Customizing Colors or Coverage Intervals

The jacoco-badge-generator provides two inputs that can be used to customize 
the colors used for the badges. The `colors` input enables you to pass a list 
of colors to the action. The `intervals` input enables you to pass a list of 
percentages used to determine color choice. If you like the default colors, 
but want to start the colors at different percentages, then you can use the 
`intervals` input to accomplish that. These two inputs can be used either
individually or in combination depending upon what you want to do. See the
[Inputs](#inputs) section for more details.

### Displayed Percentages

The coverage displayed in the badge is the result of truncating to one 
decimal place.  If that decimal place is 0, then it is displayed as an 
integer.  The rationale for truncating to one decimal place, rather than 
rounding is to avoid displaying a just failing coverage as passing. For
example, if the user of the action considers 80% to be a passing level,
then we wish to avoid the case of 79.9999% being rounded to 80% (it will
instead be truncated to 79.9%). 

### Direct Badge Generation vs JSON Endpoint

The default behavior generates badges that are inspired by the style of the badges 
of [Shields.io](https://github.com/badges/shields), and generates the badges entirely
within the jacoco-badge-generator, with no external calls. However, it also supports 
an optional alternative to instead generate [Shields JSON endpoints](https://shields.io/endpoint). 
Most users will likely prefer the default behavior, for a variety of reasons, such as 
simpler insertion of badge into README and probable faster loading. The main reason to 
consider generating a JSON endpoint instead is if you are trying to match the style of 
the coverage badges to other badges in your README that use one of Shields's alternative 
styles. The default internally generated badges match the default Shields style. See 
the [Inputs](#inputs) section for more details on how to generate JSON endpoints instead 
of badges.

### Adding the Badges to your README

#### If you generate the badges (default behavior)....

If you use the default badges directory and default badge filenames, then 
you can add the coverage badge to your repository's readme with the following 
markdown: 
```markdown
![Coverage](.github/badges/jacoco.svg)
```

And likewise for the branch coverage badge: 
```markdown
![Branches](.github/badges/branches.svg)
```

See the [Inputs](#inputs) section for how to change the directory and filenames of
the badges. You can of course also link these to the JaCoCo coverage report if you host it
online, or perhaps to the workflow that generated it, such as with (just replace 
USERNAME and REPOSITORY with yours):
```markdown
[![Coverage](.github/badges/jacoco.svg)](https://github.com/USERNAME/REPOSITORY/actions/workflows/build.yml)
```
The above assumes that the relevant workflow is `build.yml` (replace as needed). This will
link the badge to the runs of that specific workflow.

#### If you generate JSON endpoints instead....

Inserting coverage badges into your README is more complex if you use
the alternate behavior of generating JSON endpoints. It involves
passing the URL of your coverage endpoint to Shields custom badge endpoint.
Assuming that you use the default badge directory, you would then use
the following markdown:
```markdown
![Coverage](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/USERNAME/REPOSITORY/BRANCHNAME/.github/badges/jacoco.json)
```
In the above, replace USERNAME, REPOSITORY, and BRANCHNAME with yours. You can do
something similar for the branches coverage badge, such as:
```markdown
![Branches](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/USERNAME/REPOSITORY/BRANCHNAME/.github/badges/branches.json)
```
And of course, you can also link these to your workflow runs just as before with:
```markdown
[![Coverage](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/USERNAME/REPOSITORY/BRANCHNAME/.github/badges/jacoco.json)](https://github.com/USERNAME/REPOSITORY/actions/workflows/build.yml)
```

If you do have reason to prefer generating endpoints over generating the badges directly,
then you might consider pushing the endpoints to a GitHub Pages site instead, such
as a project site served from a docs directory of your default branch, or from a gh-pages
branch. To do so, in addition to configuring GitHub Pages, you would need to use the
`badges-directory` input to change the directory where the endpoints are stored
(e.g., in "docs" or in a subdirectory of "docs"). Doing so would probably speed up Shields's
access to your JSON endpoint, since you'd gain the benefit of the CDN that backs GitHub
Pages; whereas passing Shields the URL to the JSON file on GitHub's raw server will probably
be slower. Note that the potential benefit is probably small, so if doing so would complicate
your workflow, you can simply pass the URL of the endpoint from GitHub's raw server
(e.g., the examples of generating badges from an endpoint in the rightmost column
of the table in section [Default Color Scheme](#default-color-scheme) were done that way,
without the use of GitHub Pages).

This is not an issue if you use the default behavior of directly generating the badge,
since in that case the image is served directly to the viewer from the repository whose 
README is being viewed.


## GitHub Action Usage

The jacoco-badge-generator's primary use-case is as a GitHub Action. The subsections of this
section documents how to use it as a GitHub Action.

### Inputs

All inputs include default values, and are thus optional provided the
defaults are relevant to your use-case.

#### `jacoco-csv-file`

This input is the full path, relative to the root of the repository, to 
the `jacoco.csv` file, including filename.  It defaults 
to `target/site/jacoco/jacoco.csv`, which is the default location and filename
assuming you are using the JaCoCo Maven plugin and don't change the default
output location. Note that if you are using Gradle to run your build, you will
definitely need to use this input, because the default location and name of the
jacoco csv report is different than it is in Maven. If you use Gradle's default
output directories, then you will need to set this input with something 
like: `jacoco-csv-file: build/reports/jacoco/test/jacocoTestReport.csv`.

If you have a multi-module project, you can pass the paths (including filenames)
to all of the `jacoco.csv` files for all of the sub-projects. Separate these by spaces,
and in particular see the [Multi-Module Example Workflows](#multi-module-example-workflows)
for an example of how to do this. Multi-module support is limited to cases where
each module has its own test coverage report, and where those reports don't overlap.

You can also use a glob pattern to specify the set of JaCoCo reports for your modules.
For example, `jacoco-csv-file: "**/jacoco.csv"` will match all `jacoco.csv` files found
across all directories within your project. Or for example `jacoco-csv-file: "**/*.csv"`
will match all `csv` files found within your project, but be careful with such a pattern
if your project has other `csv` files that are not JaCoCo reports. Or as another example,
maybe all of your JaCoCo reports are in the same directory, but with names with numbers.
The pattern `jacoco-csv-file: "target/site/jacoco/module*.csv"` will match all `csv` files
in the directory `target/site/jacoco/` whose name begins with `module`. Note that in all of 
these examples you need the quotes around the glob pattern or else GitHub Actions will 
give you an error that your workflow file is invalid.

The action assumes that all reports passed via this input are 
independent of each other. If you are using matrix testing, such that 
each group of tests produces a report, and where the groups overlap in what
they are testing (e.g., one group tests a portion of a class or method, 
and another group tests another portion, etc), then the coverage computed by 
this action will not be correct. The csv reports don't contain enough information
to properly merge such overlapping reports. If this applies to your use-case, then
you will need to have JaCoCo produce a single JaCoCo report first (for example, 
see [jacoco:report-aggregate](https://www.jacoco.org/jacoco/trunk/doc/report-aggregate-mojo.html)). 

#### `badges-directory`

This input is the directory for storing badges, relative to the root of the 
repository. The default is `.github/badges`. The action will create the badges
directory if it doesn't already exist, although the action itself does not commit.

#### `generate-coverage-badge`

This input controls whether or not to generate the coverage badge (Instructions 
Coverage), and defaults to `true`.

#### `coverage-badge-filename`

This input is the filename for the coverage badge (Instructions or C0 
Coverage). The default filename 
is `jacoco.svg`. The file format is an `svg`. The badge file will be 
created within the `badges-directory`
directory. __The action doesn't commit the badge file. You will 
need to have additional steps in your workflow to do that.__

#### `generate-branches-badge`

This input controls whether or not to generate the branches coverage badge, and defaults
to `false`. This defaults to `false` to avoid surprising users who upgrade from earlier
versions with a badge they didn't know would be generated.

#### `branches-badge-filename`

This input is the filename for the branches coverage badge (C1 
Coverage). The default filename 
is `branches.svg`. The file format is an `svg`. The badge file will be 
created within the `badges-directory`
directory. __The action doesn't commit the badge file. You will 
need to have additional steps in your workflow to do that.__

#### `generate-coverage-endpoint`

This input controls whether or not to generate a JSON endpoint 
for coverage (Instructions Coverage), and defaults to `false`.

#### `coverage-endpoint-filename`

This input is the filename for the coverage endpoint (Instructions or C0 
Coverage) if you have opted to generate a JSON endpoint instead of the
badge. The default filename is `jacoco.json`, and will be 
created within the `badges-directory`
directory. __The action doesn't commit the JSON file. You will 
need to have additional steps in your workflow to do that.__

#### `generate-branches-endpoint`

This input controls whether or not to generate a JSON endpoint 
for branches coverage, and defaults to `false`.

#### `branches-endpoint-filename`

This input is the filename for the branches coverage endpoint (C1 
Coverage) if you have opted to generate a JSON endpoint instead of the
badge. The default filename is `branches.json`, and will be 
created within the `badges-directory`
directory. __The action doesn't commit the JSON file. You will 
need to have additional steps in your workflow to do that.__

#### `generate-summary`

This input controls whether or not to generate a simple JSON
summary report of the following form:

```JSON
{"branches": 77.77777777777779, "coverage": 72.72727272727273}
```

The default is `generate-summary: false`. To enable, use
`generate-summary: true`.

#### `summary-filename`

This input is the filename for the summary report (see above). The
default is `summary-filename: coverage-summary.json`, and will be
created within the `badges-directory`
directory. __The action doesn't commit the JSON file. You will 
need to have additional steps in your workflow to do that.__

#### `coverage-label`

This input is the text for the label on the left side of the coverage badge, which
defaults to `coverage`.

#### `branches-label`

This input is the text for the label on the left side of the branches coverage badge, which
defaults to `branches`.

#### `colors`

This input can be used to change the colors used for the badges.
It defaults to `colors: '#4c1 #97ca00 #a4a61d #dfb317 #fe7d37 #e05d44'`,
which are the hex color codes for the colors described previously in 
section [Default Color Scheme](#default-color-scheme).
Because `#` has special meaning to YAML (it is used for comments), you 
must either put quotes around the input value as shown in this example, or
you can escape each `#`. The list of colors that you pass here can either
be space separated (as shown) or comma separated. The colors in this list
can be specified either with hex (as in the example above), or with any
named colors that are recognized by SVG, or some combination of the two.
Here is an example with named 
colors: `colors: green yellow orange red purple blue`. Notice that you don't need
quotes around the input if none of the colors are specified by hex.
Although the default uses six colors and six coverage intervals, you can have
as many or as few as you want. For example, if you want to use `green` regardless
of percentage, you can set colors like this: `colors: green`. If you pass more
colors than there are intervals, then the extra colors will be ignored. If you 
pass an empty list of colors, then the action will simply use the default colors.
__The action does not do any validation of the colors that you pass.__

#### `intervals`

This input enables specifying the coverage intervals for the 
different colors. It is a simple list of percentages. The default
is `intervals: 100 90 80 70 60 0`, which corresponds to what is
described in the section [Default Color Scheme](#default-color-scheme)
earlier.  The action assumes that the percentages in this list are in 
decreasing order. You can space separate or
comma separate the percentages. For example, `intervals: 100 90 80 70 60 0`
is equivalent to `intervals: 100, 90, 80, 70, 60, 0`. A mix of spaces and commas
will also work.

If you specify too many intervals, the extras will simply be ignored. If there
are C colors altogether, then only the first (C-1) percentages specified in 
this input are used, with the last color designated for coverages that are below 
that last cutoff.  For example, if you use the default set of 6 colors, then
`intervals: 100 90 80 70 60` is equivalent to `intervals: 100 90 80 70 60 0`.

Although these examples have integer percentages, the action 
supports floating-point values. For example, you can specify something 
like `intervals: 99.5 90 80 70 60`.

If you only want to use the first three default colors (bright green, green, 
and yellow green), then you don't necessarily need to change the value
of the `colors` input. You can keep the default colors, and
then you can use something like `intervals: 80 60`, which will assign
80 and above to bright green, 60 and above to green, and less than 60 to yellow
green.

If you like some of the default colors, but want to skip over some of them,
then you can either use a combination of the `colors` input and `intervals`
input to accomplish this, or you can leave `colors` at the default and
exploit the action's assumption of decreasing percentages in the `intervals`
input to skip the ones you don't like. For example, if 
you want to use bright green for 80 and above, 
yellow for 60 and above, and red for less than 60, you might do something like the
following: `intervals: 80 80 80 60 60 0`. The 0 at the end is optional.  

#### `on-missing-report`

This input controls what happens if one or more `jacoco.csv` files do not exist.
This input accepts one of three possible values: `fail`, `quiet`, or `badges`.
The behavior of these is defined as follows:
* The default is `on-missing-report: fail`, in which case the action will 
  return a non-zero exit code (causing the workflow run to fail) if one 
  or more files listed in the `jacoco-csv-file` input do not exist, or if
  an empty list of files is passed to the action. We recommend that you use
  this default since missing coverage report files in most cases probably means
  that there is either a bug in your workflow (e.g., typo in path to jacoco.csv)
  or that something went wrong in an earlier step (e.g., unit tests failed, halting
  generation of the coverage report).
* You can use `on-missing-report: quiet` if you would rather the workflow
  itself not fail, in which case the action will instead quietly exit 
  without producing badges if any JaCoCo reports are missing.
* Although not recommended, a third option, `on-missing-report: badges`, will
  cause the action to produce badges from the report files that do exist, simply
  ignoring missing report files, provided that at least one such report file 
  exists. We do not recommend this option since such a case is likely due to an 
  error in your workflow, and any badges produced are likely computed with missing data.

Regardless of value passed to this input, the action will log warnings for
any files listed in the `jacoco-csv-file` input that do not exist, for your 
inspection in the workflow run. 

#### `fail-if-coverage-less-than`

This input enables directing the action to fail the workflow run if
the computed coverage is less than a minimum. The default is 0, effectively
disabling the option. You can specify it as either a floating point value
in the interval 0.0 to 1.0, or as a percent (with or without the percent sign).
For example, all of the following are equivalent: `fail-if-coverage-less-than: 0.6`,
`fail-if-coverage-less-than: 60`, or `fail-if-coverage-less-than: "60%"`.
Note that in the last case, you need the quotes due to the percent sign.
Values greater than 1 are assumed percents.

#### `fail-if-branches-less-than`

This input enables directing the action to fail the workflow run if
the computed branches coverage is less than a minimum. The default is 0, effectively
disabling the option. You can specify it as either a floating point value
in the interval 0.0 to 1.0, or as a percent (with or without the percent sign).
For example, all of the following are equivalent: `fail-if-branches-less-than: 0.6`,
`fail-if-branches-less-than: 60`, or `fail-if-branches-less-than: "60%"`.
Note that in the last case, you need the quotes due to the percent sign.
Values greater than 1 are assumed percents.

#### `fail-on-coverage-decrease`

This input enables directing the action to fail the workflow run if
the computed coverage is less than it was on the previous run as recorded in either the
existing coverage badge, the existing coverage Shields endpoint, or the JSON summary 
report (see the `generate-summary` input), if one of these exists. The default 
is `false`.  Use `fail-on-coverage-decrease: true` to enable. 

Additionally, at least one of the `generate-summary`, `generate-coverage-badge`, 
or `generate-coverage-endpoint` inputs must also be `true`, as the action will otherwise assume
that there is no existing badge or summary report from which to get the prior coverage.
If more than one of these exist, this feature will use the summary report to determine if coverage
decreased since it is more precise than the truncated coverage percentage stored in 
the badge or Shields endpoint. __Therefore, when using this feature, it is recommended that
you also set `generate-summary: true` and commit the summary report JSON file to the repository.__

#### `fail-on-branches-decrease`

This input enables directing the action to fail the workflow run if
the computed branches coverage is less than it was on the previous run as recorded in either the
existing branches coverage badge, the existing branches coverage Shields endpoint, or the JSON summary 
report (see the `generate-summary` input), if one of these exists. The default is `false`. 
Use `fail-on-branches-decrease: true` to enable. 

Additionally, at least one of the `generate-summary`, `generate-branches-badge`, 
or `generate-branches-endpoint` inputs must also be `true`, as the action will otherwise assume
that there is no existing badge or summary report from which to get the prior coverage.
If more than one of these exist, this feature will use the summary report to determine if branches coverage
decreased since it is more precise than the truncated coverage percentage stored in 
the badge or Shields endpoint. __Therefore, when using this feature, it is recommended that
you also set `generate-summary: true` and commit the summary report JSON file to the repository.__

#### `generate-workflow-summary`

This input controls whether or not to log the coverage percentages to the GitHub Actions
Workflow Job Summary. The default is `generate-workflow-summary: true`. This input is only 
relevant when running in GitHub Actions mode, and not when running as a CLI tool.


### Outputs

The action also outputs the actual computed coverage percentages as double-precision
floating-point numbers. So you can add a step to your workflow to access these if 
desired (these action outputs are values in the interval from 0.0 to 1.0).

#### `coverage`

This output is the actual computed coverage percentage in the interval 
from 0.0 to 1.0.  This is coverage computed from the instructions
coverage data in the JaCoCo csv report.

#### `branches`

This output is the actual computed branches coverage percentage 
in the interval from 0.0 to 1.0.  This is the percentage of branches
covered, computed from the branches data in the JaCoCo csv report.


### Example Workflows

#### Prerequisite: Running JaCoCo

##### Running JaCoCo via Maven

The example workflows assume that you are using Maven to build and test
a Java project, and that you have the `jacoco-maven-plugin`
configured in your `pom.xml` in the test phase with something
along the lines of the following:

```XML
<build>
  <plugins>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <version>0.8.10</version>
      <executions>
        <execution>
          <goals>
            <goal>prepare-agent</goal>
          </goals>
        </execution>
        <execution>
          <id>generate-code-coverage-report</id>
          <phase>test</phase>
          <goals>
            <goal>report</goal>
          </goals>
        </execution>
      </executions>
      </plugin>
  </plugins>
</build>
```

Note that the jacoco-badge-generator action has been tested with
the `jacoco.csv` files generated by `jacoco-maven-plugin` versions
0.8.6 through 0.8.10, and has not been tested with earlier versions
of JaCoCo.

##### Running JaCoCo via Gradle

If you use gradle as your build tool, then you can configure JaCoCo
in `build.gradle.kts` with:

```Kotlin
plugins {
    jacoco
}

tasks.jacocoTestReport {
    reports {
        csv.isEnabled = true
    }
}
```

Or the equivalent in `build.gradle`:

```Gradle
plugins {
    id 'jacoco'
}

jacocoTestReport {
    reports {
        csv.enabled true
    }
}
```

#### Basic Action Syntax

If you use Maven as your build tool, then you will have steps
in your workflow along the lines of the following (which assumes
that Maven is configured to run JaCoCo during the test phase:

```yml
    - name: Build with Maven
      run: mvn -B test

    - name: Generate JaCoCo Badge
      uses: cicirello/jacoco-badge-generator@v2
      with:
        generate-branches-badge: true
```

The equivalent for Gradle is:

```yml
      - name: Run Tests
        run: ./gradlew test

      - name: Run Test Coverage
        run: ./gradlew jacocoTestReport

      - name: Generate JaCoCo Badge
        uses: cicirello/jacoco-badge-generator@v2
        with:
          generate-branches-badge: true
          jacoco-csv-file: build/reports/jacoco/test/jacocoTestReport.csv
```

You can also use a specific release with:

```yml
    - name: Generate JaCoCo Badge
      uses: cicirello/jacoco-badge-generator@v2.10.0
      with:
        generate-branches-badge: true
```

#### All Possible Action Inputs

This shows a workflow step that uses all of the
possible inputs of the `jacoco-badge-generator` action.
It simply shows all of the inputs with their default values.
See the [Inputs](#inputs) section for complete details of
what these inputs do.

```yml
    - name: Generate JaCoCo Badge
      uses: cicirello/jacoco-badge-generator@v2
      with:
        jacoco-csv-file: target/site/jacoco/jacoco.csv
        badges-directory: .github/badges
        generate-coverage-badge: true
        coverage-badge-filename: jacoco.svg
        generate-branches-badge: false
        branches-badge-filename: branches.svg
        generate-coverage-endpoint: false
        coverage-endpoint-filename: jacoco.json
        generate-branches-endpoint: false
        branches-endpoint-filename: branches.json
        generate-summary: false
        summary-filename: coverage-summary.json
        coverage-label: coverage
        branches-label: branches
        colors: '#4c1 #97ca00 #a4a61d #dfb317 #fe7d37 #e05d44'
        intervals: 100 90 80 70 60 0
        on-missing-report: fail
        fail-if-coverage-less-than: 0
        fail-if-branches-less-than: 0
        fail-on-coverage-decrease: false
        fail-on-branches-decrease: false
        generate-workflow-summary: true
```

Since the above shows all of the default values of the action inputs, 
it is equivalent to:

```yml
    - name: Generate JaCoCo Badge
      uses: cicirello/jacoco-badge-generator@v2
```

#### Example Workflow 1: Generate instructions (or C0) coverage badge only.

This sample workflow runs on pushes to the main
branch.  It first sets up Java, and runs the tests with Maven. If you
have JaCoCo configured to run during the test phase, this will also
produce the JaCoCo reports.  The jacoco-badge-generator action is then
run to parse the `jacoco.csv`, compute the coverage percentage, and
generate the badge.  The coverage percentage is then logged in the
workflow so you can inspect later if necessary. The next step of the workflow
checks if any changes were made to the badge, and if so, does a commit and a push (note
that there are also GitHub Actions that you can use for that step). And 
finally, the JaCoCo coverage reports are uploaded as a workflow
artifact using the [actions/upload-artifact](https://github.com/actions/upload-artifact)
GitHub Action, so you can inspect them if necessary.

```yml
name: build

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up the Java JDK
      uses: actions/setup-java@v2
      with:
        java-version: '17'
        distribution: 'adopt'

    - name: Build with Maven
      run: mvn -B test

    - name: Generate JaCoCo Badge
      id: jacoco
      uses: cicirello/jacoco-badge-generator@v2

    - name: Log coverage percentage
      run: |
        echo "coverage = ${{ steps.jacoco.outputs.coverage }}"
        echo "branch coverage = ${{ steps.jacoco.outputs.branches }}"

    - name: Commit the badge (if it changed)
      run: |
        if [[ `git status --porcelain` ]]; then
          git config --global user.name 'YOUR NAME HERE'
          git config --global user.email 'YOUR-GITHUB-USERID@users.noreply.github.com'
          git add -A
          git commit -m "Autogenerated JaCoCo coverage badge"
          git push
        fi

    - name: Upload JaCoCo coverage report
      uses: actions/upload-artifact@v2
      with:
        name: jacoco-report
        path: target/site/jacoco/
```

#### Example Workflow 2: Generate instructions coverage and branches coverage badges.

This example workflow is just like the above example, however, it generates
both badges (instructions coverage percentage and branches coverage percentage).
This example also uses 
the [EndBug/add-and-commit](https://github.com/EndBug/add-and-commit) action to 
commit and push the badge, whereas the previous example did this step with 
shell commands.

```yml
name: build

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up the Java JDK
      uses: actions/setup-java@v2
      with:
        java-version: '17'
        distribution: 'adopt'

    - name: Build with Maven
      run: mvn -B test

    - name: Generate JaCoCo Badge
      id: jacoco
      uses: cicirello/jacoco-badge-generator@v2
      with:
        generate-branches-badge: true

    - name: Log coverage percentage
      run: |
        echo "coverage = ${{ steps.jacoco.outputs.coverage }}"
        echo "branch coverage = ${{ steps.jacoco.outputs.branches }}"

    - name: Commit and push the badge (if it changed)
      uses: EndBug/add-and-commit@v7
      with:
        default_author: github_actions
        message: 'commit badge'
        add: '*.svg'

    - name: Upload JaCoCo coverage report
      uses: actions/upload-artifact@v2
      with:
        name: jacoco-report
        path: target/site/jacoco/
```

### Multi-Module Example Workflows

#### Example Workflow 3: Generate Instructions and Coverage Badges for a Multi-Module Project.

This example workflow generates both badges (instructions coverage percentage 
and branches coverage percentage) for a multi-module project. The badges that are generated
are computed over all modules. To do so, simply pass the paths to all of the JaCoCo reports
that you want to include via the `jacoco-csv-file` input. The `>` is just Yaml's way of writing
a string across multiple lines. You can also just list all on a single space-separated line,
but your workflow file will be easier for you to read if you put them one per line.
In this example, there are three subprojects: `module1`, `module2`, and `module3`.

```yml
name: build

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up the Java JDK
      uses: actions/setup-java@v2
      with:
        java-version: '17'
        distribution: 'adopt'

    - name: Build with Maven
      run: mvn -B test

    - name: Generate JaCoCo Badge
      id: jacoco
      uses: cicirello/jacoco-badge-generator@v2
      with:
        generate-branches-badge: true
        jacoco-csv-file: >
          module1/target/site/jacoco/jacoco.csv
          module2/target/site/jacoco/jacoco.csv
          module3/target/site/jacoco/jacoco.csv

    - name: Log coverage percentage
      run: |
        echo "coverage = ${{ steps.jacoco.outputs.coverage }}"
        echo "branch coverage = ${{ steps.jacoco.outputs.branches }}"

    - name: Commit the badge (if it changed)
      run: |
        if [[ `git status --porcelain` ]]; then
          git config --global user.name 'YOUR NAME HERE'
          git config --global user.email 'YOUR-GITHUB-USERID@users.noreply.github.com'
          git add -A
          git commit -m "Autogenerated JaCoCo coverage badge"
          git push
        fi
```

#### Example Workflow 4: Glob Pattern to Specify Reports of a Multi-Module Project.

This example workflow uses a glob pattern to specify the reports of a multi-module project,
and generates both badges (instructions coverage percentage and branches coverage percentage). 
The badges that are generated are computed over all modules. In this example, all of the JaCoCo
reports are named `jacoco.csv` but reside in different directories. You can match all of them
with `jacoco-csv-file: "**/jacoco.csv"`. The quotes around the glob are required to avoid an
invalid workflow error from GitHub Actions.

```yml
name: build

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up the Java JDK
      uses: actions/setup-java@v2
      with:
        java-version: '17'
        distribution: 'adopt'

    - name: Build with Maven
      run: mvn -B test

    - name: Generate JaCoCo Badge
      id: jacoco
      uses: cicirello/jacoco-badge-generator@v2
      with:
        generate-branches-badge: true
        jacoco-csv-file: "**/jacoco.csv"

    - name: Log coverage percentage
      run: |
        echo "coverage = ${{ steps.jacoco.outputs.coverage }}"
        echo "branch coverage = ${{ steps.jacoco.outputs.branches }}"

    - name: Commit the badge (if it changed)
      run: |
        if [[ `git status --porcelain` ]]; then
          git config --global user.name 'YOUR NAME HERE'
          git config --global user.email 'YOUR-GITHUB-USERID@users.noreply.github.com'
          git add -A
          git commit -m "Autogenerated JaCoCo coverage badge"
          git push
        fi
```

#### Example Workflow 5: Multi-Module Project with Separate Badges for Each Module.

If you would prefer to generate separate coverage badges for each of the
modules of a multi-module project, then just include multiple steps of the
`jacoco-badge-generator` in your workflow, such as in this example. Be sure to use
the inputs to specify names for the badge files, otherwise with the defaults
the subsequent steps will overwrite the previous. This example assumes that there
are two modules. You also will likely want to use the `coverage-label` and `branches-label`
inputs to change the text on the left side of the badges if you are displaying badges
for multiple modules in the README of the same repository. This example demonstrates that
as well.

```yml
name: build

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up the Java JDK
      uses: actions/setup-java@v2
      with:
        java-version: '17'
        distribution: 'adopt'

    - name: Build with Maven
      run: mvn -B test

    - name: Generate JaCoCo Badges for Module 1
      id: jacocoMod1
      uses: cicirello/jacoco-badge-generator@v2
      with:
        generate-branches-badge: true
        jacoco-csv-file: module1/target/site/jacoco/jacoco.csv
        coverage-badge-filename: jacoco1.svg
        branches-badge-filename: branches1.svg
        coverage-label: coverage (module 1)
        branches-label: branches (module 1)

    - name: Generate JaCoCo Badges for Module 2
      id: jacocoMod2
      uses: cicirello/jacoco-badge-generator@v2
      with:
        generate-branches-badge: true
        jacoco-csv-file: module2/target/site/jacoco/jacoco.csv
        coverage-badge-filename: jacoco2.svg
        branches-badge-filename: branches2.svg
        coverage-label: coverage (module 2)
        branches-label: branches (module 2)

    - name: Commit the badge (if it changed)
      run: |
        if [[ `git status --porcelain` ]]; then
          git config --global user.name 'YOUR NAME HERE'
          git config --global user.email 'YOUR-GITHUB-USERID@users.noreply.github.com'
          git add -A
          git commit -m "Autogenerated JaCoCo coverage badge"
          git push
        fi
```

### Examples in Other Projects

#### Template Repository with Runnable Workflow Examples 
We now have
a [template repository](https://github.com/cicirello/examples-jacoco-badge-generator) 
with a simple Maven Java project, using the `jacoco-maven-plugin`,
along with several live, runnable workflows to demonstrate a variety of use-cases
for the `jacoco-badge-generator` action. That repository,
[cicirello/examples-jacoco-badge-generator](https://github.com/cicirello/examples-jacoco-badge-generator),
is a template so that you can potentially use it as a project starter. You can of course
fork it instead. Its README
explains the contents of that repository, especially the details of the various 
workflows it contains, and includes examples inserting the badges into its README.

#### Live Real Examples

If you would like to see examples where the action is actively used, here 
are a few repositories that are actively using the `jacoco-badge-generator` action.
The table provides a link to repositories using the action, and direct links to the
relevant workflow as well as the relevant build configuration (e.g., Maven `pom.xml` 
or Gradle `build.gradle.kts`) so you can see how JaCoCo is 
configured. Note that in all of the Maven examples, JaCoCo is configured within a 
Maven profile within the `pom.xml`, which is then activated via a command line 
option when `mvn` is run by the workflow on all push/pull request events. Configuration 
can instead be done in the `<build>` section if you'd rather not use a profile.

| Repository | Workflow | Build Configuration | 
| :----- | :----- | :-----|
| [Chips-n-Salsa](https://github.com/cicirello/Chips-n-Salsa) | [build.yml](https://github.com/cicirello/Chips-n-Salsa/blob/master/.github/workflows/build.yml) | [pom.xml](https://github.com/cicirello/Chips-n-Salsa/blob/master/pom.xml) |
| [JavaPermutationTools](https://github.com/cicirello/JavaPermutationTools) | [build.yml](https://github.com/cicirello/JavaPermutationTools/blob/master/.github/workflows/build.yml) | [pom.xml](https://github.com/cicirello/JavaPermutationTools/blob/master/pom.xml) |
| [&rho;&mu;](https://github.com/cicirello/rho-mu) | [build.yml](https://github.com/cicirello/rho-mu/blob/main/.github/workflows/build.yml) | [pom.xml](https://github.com/cicirello/rho-mu/blob/main/pom.xml) |
| [XpathQS](https://github.com/nachg/xpathqs) | [build.yml](https://github.com/nachg/xpathqs/blob/master/.github/workflows/build.yml) | [build.gradle.kts](https://github.com/nachg/xpathqs/blob/master/build.gradle.kts) |


## Command-Line Usage

The jacoco-badge-generator started its life as a GitHub Action, but due to interest can now
be used as a command-line utility outside of GitHub Actions. 

### Installing from PyPI

The jacoco-badge-generator requires Python 3 (and has been tested with 3.8 and above).

To install from PyPi (Unix and MacOS):

```Shell
python3 -m pip install jacoco-badge-generator
```

To install from PyPi (Windows):

```Shell
py -m pip install jacoco-badge-generator
```

To upgrade to the latest version from PyPi (Unix and MacOS):

```Shell
python3 -m pip install --upgrade jacoco-badge-generator
```

To upgrade to the latest version from PyPi (Windows):

```Shell
py -m pip install --upgrade jacoco-badge-generator
```

### Running for the First Time

After installing, we recommend running it once with the `-h` or `--help` flag
to see the details of all of the available command-line options.

On Unix or MacOS:

```Shell
python3 -m jacoco_badge_generator --help
```

On Windows:

```Shell
py -m jacoco_badge_generator --help
```

### CLI Examples

All GitHub Action inputs have a counterpart command-line option that can be
used in CLI mode. See the [Inputs](#inputs) section earlier for details. If the GitHub 
Actions input is named `input-name`, then in CLI mode, the corresponding command-line 
option is `--input-name`. All options are optional and provide relevant defaults 
for the basic use-case. The defaults are nearly identical to those of the GitHub Action, 
with a few exceptions.

Here are a few examples. Note that all examples assume Unix (e.g., Python command is
`python3`). If on Windows, just change `python3` to `py` in all of the examples below.

#### All Defaults

As an example, from the root of your project (assuming you've already run JaCoCo), execute
the following. In this example, all of the defaults are used, which will generate only the
instructions coverage badge, and will place it in a `badges` directory (creating it if it 
doesn't exist). Note that the default directory for the generated badges is one of the differences
between the defaults in CLI mode vs GitHub Actions mode.

```Shell
python3 -m jacoco_badge_generator
```

#### Generating Instructions Coverage and Branches Coverage Badges

```Shell
python3 -m jacoco_badge_generator --generate-branches-badge true
```

#### Generating Shields JSON Endpoints Instead of Badges

If you want to generate Shields JSON endpoints instead of badges, you need
to disable generating the coverage badge, and enable the JSON endpoints:

```Shell
python3 -m jacoco_badge_generator --generate-coverage-badge false --generate-coverage-endpoint true --generate-branches-endpoint true
```

#### Changing Colors and Coverage Intervals

If you want to change the colors used and the coverage intervals for each color,
you can use the `--colors` and `--intervals` options. In the following example,
green is used if coverage is at least 90 percent, yellow if coverage is less than 90 but
at least 75 percent, orange is used if coverage is less than 75 percent but at least 60
percent, and red is used if coverage is less than 60 percent.

```Shell
python3 -m jacoco_badge_generator --colors green yellow orange red --intervals 90 75 60
```

Colors can be specified as either SVG named colors as above or as 6-digit or 3-digit hex colors
(see the [Inputs](#inputs) earlier for more detail).

#### Changing the Badges Directory

```Shell
python3 -m jacoco_badge_generator --badges-directory put/badges/here
```

#### Gradle Location of JaCoCo Report

The utility by default assumes that the JaCoCo report is the Maven default 
of `target/site/jacoco/jacoco.csv`. If it is somewhere else, there is an option
to specify its location. Here is an example with Gradle's standard location
and name of the JaCoCo csv report.

```Shell
python3 -m jacoco_badge_generator --jacoco-csv-file build/reports/jacoco/test/jacocoTestReport.csv
```

#### Multi-Module Example

If you have a multi-module project with multiple coverage reports that you want to combine (provided
they are independent), then you can specify the locations and names of all of the report files with
something like:

```Shell
python3 -m jacoco_badge_generator --jacoco-csv-file reports/report1.csv reports/report2.csv
```

In CLI mode, glob patterns will be handled by your shell. You can accomplish the above with:

```Shell
python3 -m jacoco_badge_generator --jacoco-csv-file reports/report*.csv
```

Or perhaps all of your reports are named `jacoco.csv` but in different directories, then you can
match all of them with:

```Shell
python3 -m jacoco_badge_generator --jacoco-csv-file **/jacoco.csv
```

## Summary of Input Defaults

The following table summarizes the default values of all inputs for both the GitHub Actions
usage as well as the CLI usage. If your use-case requires the defaults as specified below, then
you do not need to include them.

| GitHub Actions Default | CLI Default |
| --- | --- |
| `jacoco-csv-file: target/site/jacoco/jacoco.csv` | `--jacoco-csv-file target/site/jacoco/jacoco.csv`<br>or<br>`-j target/site/jacoco/jacoco.csv` |
| `badges-directory: .github/badges` | `--badges-directory badges`<br>or<br>`-d badges` |
| `generate-coverage-badge: true` | `--generate-coverage-badge true` |
| `coverage-badge-filename: jacoco.svg` | `--coverage-badge-filename jacoco.svg` |
| `generate-branches-badge: false` | `--generate-branches-badge false` |
| `branches-badge-filename: branches.svg` | `--branches-badge-filename branches.svg` |
| `generate-coverage-endpoint: false` | `--generate-coverage-endpoint false` |
| `coverage-endpoint-filename: jacoco.json` | `--coverage-endpoint-filename jacoco.json` |
| `generate-branches-endpoint: false` | `--generate-branches-endpoint false` |
| `branches-endpoint-filename: branches.json` | `--branches-endpoint-filename branches.json` |
| `generate-summary: false` | `--generate-summary false` |
| `summary-filename: coverage-summary.json` | `--summary-filename coverage-summary.json` |
| `coverage-label: coverage` | `--coverage-label coverage` |
| `branches-label: branches` | `--branches-label branches` |
| `colors: '#4c1 #97ca00 #a4a61d #dfb317 #fe7d37 #e05d44'` | On Windows: `--colors #4c1 #97ca00 #a4a61d #dfb317 #fe7d37 #e05d44`<br>Bash or anywhere `#` has special meaning: `--colors '#4c1' '#97ca00' '#a4a61d' '#dfb317' '#fe7d37' '#e05d44'` |
| `intervals: 100 90 80 70 60 0` | `--intervals 100 90 80 70 60 0` |
| `on-missing-report: fail` | `--on-missing-report fail` |
| `fail-if-coverage-less-than: 0` | `--fail-if-coverage-less-than 0` |
| `fail-if-branches-less-than: 0` | `--fail-if-branches-less-than 0` |
| `fail-on-coverage-decrease: false` | `--fail-on-coverage-decrease false` |
| `fail-on-branches-decrease: false` | `--fail-on-branches-decrease false` |
| `generate-workflow-summary: true` | n/a |

## Blog Posts

Here is a selection of blog posts about the jacoco-badge-generator on DEV.to:
* [JaCoCo Coverage Badges for Multi-Module Projects in GitHub Actions](https://dev.to/cicirello/jacoco-coverage-badges-for-multi-module-projects-in-github-actions-ace), posted on DEV on May 25, 2023.
* [Using GitHub Actions to Build a Java Project With Pull Request Coverage Commenting and Coverage Badges](https://dev.to/cicirello/using-github-actions-to-build-a-java-project-with-pull-request-coverage-commenting-and-coverage-badges-50a2), posted on DEV on November 9, 2022.
* [The jacoco-badge-generator GitHub Action is now also available as a CLI tool from PyPI](https://dev.to/cicirello/the-jacoco-badge-generator-github-action-is-now-also-available-as-a-cli-tool-from-pypi-3ma0), posted on DEV on July 8, 2022.
* [JaCoCo coverage badges, PR coverage checks, and PR coverage comments, from GitHub Actions](https://dev.to/cicirello/jacoco-coverage-badges-pr-coverage-checks-and-pr-coverage-comments-from-github-actions-4a8f), posted on DEV on November 29, 2021.

## Support the Project

You can support the project in a number of ways:
* __Starring__: If you find the `jacoco-badge-generator` action 
  useful, consider starring the repository.
* __Sharing with Others__: Consider sharing it with others who
  you feel might find it useful.
* __Reporting Issues__: If you find a bug or have a suggestion for
  a new feature, please report it via 
  the [Issue tracker](https://github.com/cicirello/jacoco-badge-generator/issues).
* __Contributing Code__: If there is an open issue that you think
  you can help with, submit a pull request.
* __Sponsoring__: You can also consider 
  [becoming a sponsor](https://github.com/sponsors/cicirello).

## License

This GitHub action is released under
the [MIT License](https://github.com/cicirello/jacoco-badge-generator/blob/main/LICENSE).
