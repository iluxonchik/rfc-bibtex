# RFC-Bibtex
A command line tool that creates bibtex entries for IETF RFCs and Internet-Drafts.

# Installation/Requirements

You can use `pip` to install this command-line tool:

    pip install rfc-bibtex

Alternatively, you can clone this repository or download the `rfc-bibtex.py`. This tool has no
external dependencies, so as long as you have `Python 3.x` installed, everything
should work fine.

**Requirements**:

* `Python 3.x`
* internet connection

# Usage

I wrote this tool since I needed to include a lot of RFC referrences in my master thesis
in bibtex format. It simply automates the requests that you can do manually from [https://sysnetgrp.no-ip.org/rfc/](https://sysnetgrp.no-ip.org/rfc/).

    usage: rfc-bibtex [-h] [-f FILE_NAME] [-o FILE_NAME]
                     [inline_args [inline_args ...]]

    Generate Bibtex entries for IETF RFCs and Internet-Drafts. Titles are output to
    preserve the original capitalization.

    positional arguments:
    inline_args           list of RFC and/or Internet-Draft IDs, in any order.

    optional arguments:
    -h, --help            show this help message and exit
    -f FILE_NAME, --file FILE_NAME
                        read list of RFC and/or Internet-Draft IDs (one per
                        line) from a file
    -o FILE_NAME, --output FILE_NAME
                        output the resulting bibtex to a file

## Identifier Format

The identifier format of RFCs is `rfc<rfc_num>`, where `<rfc_num>` is the RFC number.
For example, for the [RFC specifying TLS 1.2](https://tools.ietf.org/html/rfc5246) you
would write `rfc5246` (**NOTE**: the letters RFC can also be capitalized, so that `RFC5246` is also accepted).

The input format of Internet-Drafts(I-Ds) is `draft-<rest>`, where `<rest>` is the rest of
the draft's name ([all Internet-Drafts begin with "draft"](https://www.ietf.org/id-info/guidelines.html#naming)). For example, for the
[TLS 1.3 Draft 21]() you would write `draft-ietf-tls-tls13-21`.


## Read Inputs From Command Line

Example command:

`python rfc-bibtex.py RFC5246 draft-ietf-tls-tls13-21`

**Output**:

    @techreport{RFC5246,
    author = {T. Dierks and E. Rescorla},
    title = {{The Transport Layer Security (TLS) Protocol Version 1.2}},
    howpublished = {Internet Requests for Comments},
    type = {RFC},
    number = {5246},
    year = {2008},
    month = {August},
    issn = {2070-1721},
    publisher = {RFC Editor},
    institution = {RFC Editor},
    url = {http://www.rfc-editor.org/rfc/rfc5246.txt},
    note = {\url{http://www.rfc-editor.org/rfc/rfc5246.txt}},
    }


    @techreport{I-D.ietf-tls-tls13,
    author = {Eric Rescorla},
    title = {{The Transport Layer Security (TLS) Protocol Version 1.3}},
    howpublished = {Working Draft},
    type = {Internet-Draft},
    number = {draft-ietf-tls-tls13-21},
    year = {2017},
    month = {July},
    institution = {IETF Secretariat},
    url = {http://www.ietf.org/internet-drafts/draft-ietf-tls-tls13-21.txt},
    note = {\url{http://www.ietf.org/internet-drafts/draft-ietf-tls-tls13-21.txt}},
    }


## Read Identifiers From A file

Option: `-f <file_name1> ... <file_nameN>`

Alternatively, identifiers can be specified in a file.  Two input formats are accepted.

**LaTeX .aux files**: If you have a LaTeX .aux file, this program will parse the \citation{} commands in the file
and extract those that appear to be RFCs or internet drafts. If you specify a .tex file, the program will look for the matching .aux
file and generate an error if it is not present.

**Plain text files**: Alternatively, you may simpy specify a series of identifiers, one per line in your text file.

For example, consider you have a file called `rfcs_and_ids.txt` with the following
content:

    rfc7925
    draft-moran-suit-architecture-00

Example command:

`python rfc-bibtex.py -f rfc_and_ids.txt`

**Output**:


    @techreport{RFC7925,
    author = {H. Tschofenig and T. Fossati},
    title = {{Transport Layer Security (TLS) / Datagram Transport Layer Security (DTLS) Profiles for the Internet of Things}},
    howpublished = {Internet Requests for Comments},
    type = {RFC},
    number = {7925},
    year = {2016},
    month = {July},
    issn = {2070-1721},
    publisher = {RFC Editor},
    institution = {RFC Editor},
    }


    @techreport{I-D.moran-suit-architecture,
    author = {Brendan Moran and Milosch Meriac and Hannes Tschofenig},
    title = {{A Firmware Update Architecture for Internet of Things Devices}},
    howpublished = {Working Draft},
    type = {Internet-Draft},
    number = {draft-moran-suit-architecture-00},
    year = {2017},
    month = {October},
    institution = {IETF Secretariat},
    url = {http://www.ietf.org/internet-drafts/draft-moran-suit-architecture-00.txt},
    note = {\url{http://www.ietf.org/internet-drafts/draft-moran-suit-architecture-00.txt}},
    }


## Output Contents To A File

Option: `-o <file_name>`

Considering the `rfcs_and_ids.txt` described above.

Example command:

`python rfc-bibtex.py RFC5246 draft-ietf-tls-tls13-21 -f rfc_and_ids.txt -o output.bib`

A file `output.bib` would be created or overriden with the following content:

    @techreport{RFC5246,
      author = {T. Dierks and E. Rescorla},
      title = {{The Transport Layer Security (TLS) Protocol Version 1.2}},
      howpublished = {Internet Requests for Comments},
      type = {RFC},
      number = {5246},
      year = {2008},
      month = {August},
      issn = {2070-1721},
      publisher = {RFC Editor},
      institution = {RFC Editor},
      url = {http://www.rfc-editor.org/rfc/rfc5246.txt},
      note = {\url{http://www.rfc-editor.org/rfc/rfc5246.txt}},
    }


    @techreport{I-D.ietf-tls-tls13,
      author = {Eric Rescorla},
      title = {{The Transport Layer Security (TLS) Protocol Version 1.3}},
      howpublished = {Working Draft},
      type = {Internet-Draft},
      number = {draft-ietf-tls-tls13-21},
      year = {2017},
      month = {July},
      institution = {IETF Secretariat},
      url = {http://www.ietf.org/internet-drafts/draft-ietf-tls-tls13-21.txt},
      note = {\url{http://www.ietf.org/internet-drafts/draft-ietf-tls-tls13-21.txt}},
    }


    @techreport{RFC7925,
      author = {H. Tschofenig and T. Fossati},
      title = {{Transport Layer Security (TLS) / Datagram Transport Layer Security (DTLS) Profiles for the Internet of Things}},
      howpublished = {Internet Requests for Comments},
      type = {RFC},
      number = {7925},
      year = {2016},
      month = {July},
      issn = {2070-1721},
      publisher = {RFC Editor},
      institution = {RFC Editor},
    }


    @techreport{I-D.moran-suit-architecture,
      author = {Brendan Moran and Milosch Meriac and Hannes Tschofenig},
      title = {{A Firmware Update Architecture for Internet of Things Devices}},
      howpublished = {Working Draft},
      type = {Internet-Draft},
      number = {draft-moran-suit-architecture-00},
      year = {2017},
      month = {October},
      institution = {IETF Secretariat},
      url = {http://www.ietf.org/internet-drafts/draft-moran-suit-architecture-00.txt},
      note = {\url{http://www.ietf.org/internet-drafts/draft-moran-suit-architecture-00.txt}},
    }

# Comments

This tool was written quickly to address a specific need. Only basic tests
have been perfomed, and only a few automated tests are included.
