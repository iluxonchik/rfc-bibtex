# RFC-Bibtex
A command line tool that creates bibtex entries for IETF RFCs and Internet-Drafts.

# Installation/Requirements

Simply clone this repository or download the `rfc-bibtex.py`. This tool has no
external dependencies, so as long as you have `Python 3.x` installed, everything
should work fine.

**Requirements**:

* `Python 3.x`
* internet connection

# Usage

I wrote this tool since I needed to include a lot of RFC referrences in my master thesis
in bibtex format. It simply automates the requests that you can do manually from [https://sysnetgrp.no-ip.org/rfc/](https://sysnetgrp.no-ip.org/rfc/).

## Input Format

The input format of RFCs is `rfc<rfc_num>`, where `<rfc_num>` is the RFC number.
For example, for the [RFC specifying TLS 1.2](https://tools.ietf.org/html/rfc5246) you
would write `rfc5246` (**NOTE**: `RFC5246` is also accepted).

The input format of Internet-Drafts(I-Ds) is `draft-<rest>`, where `<rest>` is the rest of
the draft's name ([all Internet-Drafts begin with "draft"](https://www.ietf.org/id-info/guidelines.html#naming)). For example, for the
[TLS 1.3 Draft 21]() you would write `draft-ietf-tls-tls13-21`.


## Read Inputs From Command Line

Example command:

`python rfc-bibtex.py RFC5246 draft-ietf-tls-tls13-21`

**Output**:

    Type the output
    here.

## Read Inputs From A file

Option: `-f <file_name>`

Consider that you have a file called `rfcs_and_ids.txt` with the following
content:

    rfc7925
    draft-moran-suit-architecture-00

Example command:

`python rfc-bibtex.py -f rfc_and_ids.txt`

**Output**:

    Type the output
    here.  

## Output Contents To A File

Option: `-o <file_name>`

Considering the `rfcs_and_ids.txt` described above.

Example command:

`python rfc-bibtex.py RFC5246 draft-ietf-tls-tls13-21 -f rfc_and_ids.txt -o output.bib`

A file `output.bib` would be created or overriden wit the following content:

    Type the output
    here.

# Comments

This tool was written quickly to address a specific need. Only basic tests
have been perfomed, no testing suite is included.
