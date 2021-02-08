# jacoco-badge-generator

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/cicirello/jacoco-badge-generator?label=Marketplace&logo=GitHub)](https://github.com/marketplace/actions/jacoco-badge-generator)
[![build](https://github.com/cicirello/jacoco-badge-generator/workflows/build/badge.svg)](https://github.com/cicirello/jacoco-badge-generator/actions?query=workflow%3Abuild)
[![GitHub](https://img.shields.io/github/license/cicirello/jacoco-badge-generator)](https://github.com/cicirello/jacoco-badge-generator/blob/main/LICENSE)
![GitHub top language](https://img.shields.io/github/languages/top/cicirello/jacoco-badge-generator)

The jacoco-badge-generator GitHub Action parses a `jacoco.csv` from a Jacoco coverage report,
computes the overall coverage percentage and the percentage of covered branches, and generates 
badges for one or both of these (configurable with action inputs) to provide an easy 
to read visual summary of the code coverage of your
test cases.  The badges that are generated are inspired by the style of the badges 
of [Shields.io](https://github.com/badges/shields), however, the badges are entirely generated
within the jacoco-badge-generator GitHub Action, with no external calls.  Here are
a few samples of what the badges look like:
* ![Coverage 100%](https://github.com/cicirello/jacoco-badge-generator/blob/main/tests/100.svg): We use bright green for 100% coverage.
* ![Coverage 99.9%](https://github.com/cicirello/jacoco-badge-generator/blob/main/tests/999.svg): We use green for coverage from 90% up through 99.9%.
* ![Coverage 80%](https://github.com/cicirello/jacoco-badge-generator/blob/main/tests/80.svg): We use yellow green for coverage from 80% up through 89.9%.
* ![Coverage 70%](https://github.com/cicirello/jacoco-badge-generator/blob/main/tests/70.svg): We use yellow for coverage from 70% up through 79.9%.
* ![Coverage 60%](https://github.com/cicirello/jacoco-badge-generator/blob/main/tests/60.svg): We use orange for coverage from 60% up through 69.9%.
* ![Coverage 59.9%](https://github.com/cicirello/jacoco-badge-generator/blob/main/tests/599.svg): We use red for coverage from 0% up through 59.9%.
* ![Branches Coverage 99.9%](https://github.com/cicirello/jacoco-badge-generator/blob/main/tests/999b.svg): A sample of a branch coverage badge.

The coverage displayed in the badge is the result of truncating to one 
decimal place.  If that decimal place is 0, then it is displayed as an 
integer.  The rationale for truncating to one decimal place, rather than 
rounding is to avoid displaying a just failing coverage as passing. For
example, if the user of the action considers 80% to be a passing level,
then we wish to avoid the case of 79.9999% being rounded to 80% (it will
instead be truncated to 79.9%).  

The action also outputs the actual computed coverage percentages as double-precision
floating-point numbers. So you can add a step to your workflow to access these if 
desired (these action outputs are values in the interval from 0.0 to 1.0).  

## Inputs

All inputs include default values, and are thus optional provided the
defaults are relevant to your use-case.

### `jacoco-csv-file`

This input is the full path, relative to the root of the repository, to 
the `jacoco.csv` file, including filename.  It defaults 
to `target/site/jacoco/jacoco.csv`, which is the default location and filename
assuming you are using the Jacoco Maven plugin and don't change the default
output location.

### `badges-directory`

This input is the directory for storing badges, relative to the root of the 
repository. The default is `.github/badges`. The action will create the badges
directory if it doesn't already exist, although the action itself does not commit.

### `coverage-badge-filename`

This input is the filename for the coverage badge. The default filename 
is `jacoco.svg`. The file format is an `svg`. The badge file will be 
created within the `badges-directory`
directory. __The action doesn't commit the badge file. You will 
need to have additional steps in your workflow to do that.__

### `branches-badge-filename`

This input is the filename for the branches coverage badge. The default filename 
is `branches.svg`. The file format is an `svg`. The badge file will be 
created within the `badges-directory`
directory. __The action doesn't commit the badge file. You will 
need to have additional steps in your workflow to do that.__

### `generate-coverage-badge`

This input controls whether or not to generate the overall coverage badge, and defaults
to `true`.

### `generate-branches-badge`

This input controls whether or not to generate the branches coverage badge, and defaults
to `false`. This defaults to `false` to avoid surprising users who upgrade from earlier
versions with a badge they didn't know would be generated.

### `jacoco-badge-file`

__This input is DEPRECATED.__ You should instead use the combination of 
the `badges-directory` and `coverage-badge-filename` inputs. This input 
will be removed in the next release, and has been retained only to ease 
transition from earlier versions of this GitHub Action. If this input is 
used it takes precedence over the new `badges-directory` 
and `coverage-badge-filename` inputs. This input is the full path, relative 
to the root of the repository, to the created coverage badge, including 
filename. This defaults to the empty string. Note that if you were using 
the old default value for this input in prior versions, then you should be all
set with the default values for the new pair of replacement inputs.

## Outputs

### `coverage`

This output is the actual computed coverage percentage in the interval 
from 0.0 to 1.0.  This is overall coverage computed from the instruction
coverage data in the Jacoco csv report.

### `branches`

This output is the actual computed branches coverage percentage 
in the interval from 0.0 to 1.0.  This is the percentage of branches
covered, computed from the branches data in the Jacoco csv report.

## Example Workflow

### Prerequisite: Running Jacoco

This example workflow assumes that you are using Maven to build and test
a Java project, and that you have the `jacoco-maven-plugin`
configured in your `pom.xml` in the test phase with something
along the lines of the following:

```XML
<build>
  <plugins>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <version>0.8.6</version>
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

### Example Workflow 1: Generate overall coverage badge only.

This sample workflow runs on pushes to the main
branch.  It first sets up Java, and runs the tests with Maven. If you
have Jacoco configured to run during the test phase, this will also
produce the Jacoco reports.  The jacoco-badge-generator action is then
run to parse the `jacoco.csv`, compute the coverage percentage, and
generate the badge.  The coverage percentage is then logged in the
workflow so you can inspect later if necessary. The next step of the workflow
checks if any changes were made to the badge, and if so, does a commit and a push (note
that there are also GitHub Actions that you can use for that step). And 
finally, the Jacoco coverage reports are uploaded as a workflow
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

    - name: Set up JDK 1.11
      uses: actions/setup-java@v1
      with:
        java-version: 1.11

    - name: Build with Maven
      run: mvn -B test

    - name: Generate Jacoco Badge
      id: jacoco
      uses: cicirello/jacoco-badge-generator@v1.2.0

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

    - name: Upload Jacoco coverage report
      uses: actions/upload-artifact@v2
      with:
        name: jacoco-report
        path: target/site/jacoco/
```

### Example Workflow 2: Generate overall coverage and branches coverage badges.

This example workflow is just like the above example, however, it generates
both badges (overall coverage percentage and branches coverage percentage).

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

    - name: Set up JDK 1.11
      uses: actions/setup-java@v1
      with:
        java-version: 1.11

    - name: Build with Maven
      run: mvn -B test

    - name: Generate Jacoco Badge
      id: jacoco
      uses: cicirello/jacoco-badge-generator@v1.2.0
      with:
        generate-branches-badge: true

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

    - name: Upload Jacoco coverage report
      uses: actions/upload-artifact@v2
      with:
        name: jacoco-report
        path: target/site/jacoco/
```


## License

This GitHub action is released under
the [MIT License](https://github.com/cicirello/jacoco-badge-generator/blob/main/LICENSE).
