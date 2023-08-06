# PEALS: Peak-based Enhancement Analysis PipeLine for MeRIP-Seq

Latest Release:
* Github: [![Github Release](https://img.shields.io/github/v/release/peals-project/PEALS)](https://github.com/kerenzhou062/PEALS/releases)
* PyPI: [![PyPI Release](https://img.shields.io/pypi/v/peals.svg) ![PyPI Python Version](https://img.shields.io/pypi/pyversions/peals) ![PyPI Format](https://img.shields.io/pypi/format/peals)](https://pypi.org/project/peals/)

## Introduction

MeRIP-seq stands for methylated RNA immunoprecipitation sequencing, which is the most popular method for detection of post-transcriptional RNA modifications. Here, we presented
the **P**-based **E**nhancement **A**nalysis Pipe**L**ine for MeRIP-**S**eq (PEALS), for
identifying enriched methylation regions. PEALS is designed for capturing the enriched methylated regions from MeRIP-seq, where IP signals are significantly over the input signals. Unlike other tools, PEALS not only can detect the peaks located across the exons, but also can detect peaks located in introns. It will be very usefull to detect the methylated peaks in caRNAs, primary transcripts, etc. After peak detections, PEALS wrap DESeq2 framework to estimate the enrichment and their significance. When detecting the differentially methylated (DM) peaks, PEALS use complex strategies to normalized the reads count under different conditions to avoid over-normalization.

## Required third party software

PEALS relies on the following third party software. Before installing PEALS, please to ensure the following software have been properly installed.

 * [bedTools (>=2.30.0)](https://bedtools.readthedocs.io/en/latest/content/installation.html)
 * [samtools (>=1.14)](http://www.htslib.org/download/)
 * [featureCounts (>=2.0.2)](https://subread.sourceforge.net/featureCounts.html)

The following R pacakges should be also installed.
 * [getopt (>=1.20.3)](https://bioconductor.org/packages/release/bioc/html/DESeq2.html)
 * [DESeq2 (>=1.32.0)](https://bioconductor.org/packages/release/bioc/html/DESeq2.html)
 * [ggplot2 (>=3.4.1)](https://ggplot2.tidyverse.org/index.html)
 * [ashr (>=2.2.54)](https://github.com/stephens999/ashr)
 * [apeglm (>=1.14.0)](https://bioconductor.org/packages/release/bioc/html/apeglm.html)
 * [glmGamPoi (>=1.4.0)](https://bioconductor.org/packages/release/bioc/html/glmGamPoi.html)

## Install

The common way to install PEALS is through
[PYPI](https://pypi.org/project/peals/)).

Please check [INSTALL](./docs/INSTALL.md) document for detail.

## Usage

Example for regular peak calling on MeRIP-seq.

For sample matrix, please chek the [sample matrix](./example/peals.callpeak.sample.txt) here as reference.

`peals callpeak -i <bam directory> -m <sample matrix> -P <prefix> -o <output directory>`

Example for differentially methylated peak calling on MeRIP-seq.

For sample matrix, please chek the [sample matrix](./example/peals.diffpeak.sample.txt) here as reference.

`peals diffpeak -i <bam directory> -m <sample matrix> -P <prefix> -o <output directory>`


Subcommand | Description
-----------|----------
[`callpeak`](./docs/callpeak.md) | Main function to call peaks from alignment results.
[`diffpeak`](./docs/diffpeak.md) | Main function to call differentially methylated peaks from alignment results.

## Contribute
If you have any questions, suggestion/ideas, or just want to have conversions with
developers and other users in the community, we recommand you using [discussion](https://github.com/kerenzhou062/PEALS/discussion) section or posting to our
[Issues](https://github.com/kerenzhou062/PEALS/issues) page.

## Ackowledgement

PEALS project also relies on the following python packages.

 * [CSAPS](https://pypi.org/project/csaps/)
 * [findpeaks](https://pypi.org/project/findpeaks/)
