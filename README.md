# RFC-Bibtex

A command line tool that creates `BibTex` entries for IETF `RFC`s and `Internet Drafts`.
It can read the list of `RFC`s and `Internet Drafts` to parse from various sources:

* directly from `.tex` files
* directly from `.aux` files
* from a text file (one ID per line)
* from command-line arguments

Duplicate entires are filtered out.

# Installation/Requirements

You can use `pip` to install this command-line tool:

    pip install rfc-bibtex

Alternatively, you can clone this repository or download the `rfc-bibtex.py`. This tool has no
external dependencies, so as long as you have `Python 3.x` installed, everything
should work fine.

**Requirements**:

* `Python 3.x`
* internet connection

## Testing

First, install the test dependencies:

`pipenv install --dev`

or 

`pip install -r dev-requirements.txt`

and then run:

`python -m unittest discover tests`

from the project root.

# Usage

This tool automates the requests to the `https://datatracker.ietf.org/doc/<id>/<version>/bibtex/` and `https://datatracker.ietf.org/doc/<id>/bibtex/` endpoints.

  usage: rfcbibtex [-h] [-f FILE_NAME] [-o FILE_NAME]
                  [inline_args [inline_args ...]]

  Generate BibTex entries for IETF RFCs and Internet Drafts. The list of IDs can
  be read from a file (including .tex and .aux) or directly from command-line
  arguments.

  positional arguments:
    inline_args           list of RFC and/or Internet Draft IDs, in any order.

  optional arguments:
    -h, --help            show this help message and exit
    -f FILE_NAME, --file FILE_NAME
                          read list of RFC and/or Internet Draft IDs from a
                          file. Supported file formats are the following: .tex,
                          .aux and .txt (one ID per line). If a file with any
                          other extension is provided, the tool attempts to read
                          it as a .txt file, containing one ID per line.
    -o FILE_NAME, --output FILE_NAME
                          output the resulting BibTex to a file


## Identifier Format

The identifier format of RFCs is `rfc<rfc_num>`, where `<rfc_num>` is the RFC number.
For example, for the [RFC specifying TLS 1.2](https://tools.ietf.org/html/rfc5246) you
would write `rfc5246` (**NOTE**: the identifiers are case-insensitive, so `RFC5246` and `rFc5246` are also accepted).

The input format of Internet-Drafts(I-Ds) is `draft-<rest>`, where `<rest>` is the rest of
the draft's name ([all Internet-Drafts begin with "draft"](https://www.ietf.org/id-info/guidelines.html#naming)). For example, for the
[TLS 1.3 Draft 21]() you would write `draft-ietf-tls-tls13-21`.

## Read Inputs From Command Line

Example command:

`rfcbibtex RFC5246 draft-ietf-tls-tls13-21`

**Output**:

    @misc{rfc5246,
            series =        {Request for Comments},
            number =        5246,
            howpublished =  {RFC 5246},
            publisher =     {RFC Editor},
            doi =           {10.17487/RFC5246},
            url =           {https://rfc-editor.org/rfc/rfc5246.txt},
            author =        {Eric Rescorla and Tim Dierks},
            title =         {{The Transport Layer Security (TLS) Protocol Version 1.2}},
            pagetotal =     104,
            year =          2008,
            month =         aug,
            abstract =      {This document specifies Version 1.2 of the Transport Layer Security (TLS) protocol. The TLS protocol provides communications security over the Internet. The protocol allows client/server applications to communicate in a way that is designed to prevent eavesdropping, tampering, or message forgery. {[}STANDARDS-TRACK{]}},
    }

    @techreport{draft-ietf-tls-tls13-21,
            number =        {draft-ietf-tls-tls13-21},
            type =          {Internet-Draft},
            institution =   {Internet Engineering Task Force},
            publisher =     {Internet Engineering Task Force},
            note =          {Work in Progress},
            url =           {https://datatracker.ietf.org/doc/html/draft-ietf-tls-tls13-21},
            author =        {Eric Rescorla},
            title =         {{The Transport Layer Security (TLS) Protocol Version 1.3}},
            pagetotal =     143,
            year =          ,
            month =         ,
            day =           ,
            abstract =      {This document specifies version 1.3 of the Transport Layer Security (TLS) protocol. TLS allows client/server applications to communicate over the Internet in a way that is designed to prevent eavesdropping, tampering, and message forgery.},
    }



## Read Identifiers From A file

Option: `-f <file_name_1> ... <file_name_N>`

Alternatively, identifiers can be specified in a file.  The following input formats are accepted:

* `.tex`: if you specify an `.tex` file, the program will search for \cite{} commands in the file and
extract those that appear to contain RFCs or Internet Drafts identifiers.
* `.aux`: if you specify an `.aux` file, the program will search for \citation{} commands in the file
and extract those that appear to contain RFCs or Internet Drafts identifiers.
* `.txt`: the program defaults to this file type if the file's extension is neither `.tex`, nor `.aux`.
This file type must contain a list of RFCs or Internet Drafts identifiers, one per line.

Please note that the identifiers must be in the format specified in the [Identifier Format](#identifier-format) seciton.

### Reading Identifiers From A .tex File

<a id="tex-file"></a>Consider that you have a file called `rfcs_and_ids.tex` with the following content:

    \documentclass{article}
    \usepackage[utf8]{inputenc}

    \title{This Is A Simple Tex File For The RFCBibtex Project Demo}
    \author{Illya Gerasymchuk}
    \date{March 2019}

    \usepackage{natbib}
    \usepackage{graphicx}

    \begin{document}

    \maketitle

    \section{Introduction}
    
    There is nothing special here, nothing fancy, just a document with a few citations, like
    \cite{RFC5246} this one. This one here \cite{the-documentary-2005} should not be parsed.
    While this one \cite{draft-ietf-tls-tls13-21} should. And finally, let's cite the
    TLS 1.3 RFC \cite{RFC8446}. Well, that's it folks. At least for now... This is a very basic
    file, just to test if \textbf{the basic} latex parsing is working.

    You can find the RFCBitex project here: https://github.com/iluxonchik/rfc-bibtex

    \begin{figure}[h!]
    \centering
    \includegraphics[scale=1.7]{universe}
    \caption{The Universe}
    \label{fig:universe}
    \end{figure}

    \section{Conclusion}

    As you can see, your .tex file may have various citations, but only the ones that are RFCs
    and/or Internet Draft IDs are parsed.

    \bibliographystyle{plain}
    \bibliography{references}
    \end{document}

If you run:

`rfcbibtex -f rfcs_and_ids.tex`

<a id="example-output"></a>You will get the following output:

    @misc{rfc5246,
            series =        {Request for Comments},
            number =        5246,
            howpublished =  {RFC 5246},
            publisher =     {RFC Editor},
            doi =           {10.17487/RFC5246},
            url =           {https://rfc-editor.org/rfc/rfc5246.txt},
            author =        {Eric Rescorla and Tim Dierks},
            title =         {{The Transport Layer Security (TLS) Protocol Version 1.2}},
            pagetotal =     104,
            year =          2008,
            month =         aug,
            abstract =      {This document specifies Version 1.2 of the Transport Layer Security (TLS) protocol. The TLS protocol provides communications security over the Internet. The protocol allows client/server applications to communicate in a way that is designed to prevent eavesdropping, tampering, or message forgery. {[}STANDARDS-TRACK{]}},
    }

    @techreport{draft-ietf-tls-tls13-21,
            number =        {draft-ietf-tls-tls13-21},
            type =          {Internet-Draft},
            institution =   {Internet Engineering Task Force},
            publisher =     {Internet Engineering Task Force},
            note =          {Work in Progress},
            url =           {https://datatracker.ietf.org/doc/html/draft-ietf-tls-tls13-21},
            author =        {Eric Rescorla},
            title =         {{The Transport Layer Security (TLS) Protocol Version 1.3}},
            pagetotal =     143,
            year =          ,
            month =         ,
            day =           ,
            abstract =      {This document specifies version 1.3 of the Transport Layer Security (TLS) protocol. TLS allows client/server applications to communicate over the Internet in a way that is designed to prevent eavesdropping, tampering, and message forgery.},
    }

    @misc{rfc8446,
            series =        {Request for Comments},
            number =        8446,
            howpublished =  {RFC 8446},
            publisher =     {RFC Editor},
            doi =           {10.17487/RFC8446},
            url =           {https://rfc-editor.org/rfc/rfc8446.txt},
            author =        {Eric Rescorla},
            title =         {{The Transport Layer Security (TLS) Protocol Version 1.3}},
            pagetotal =     160,
            year =          2018,
            month =         aug,
            abstract =      {This document specifies version 1.3 of the Transport Layer Security (TLS) protocol. TLS allows client/server applications to communicate over the Internet in a way that is designed to prevent eavesdropping, tampering, and message forgery. This document updates RFCs 5705 and 6066, and obsoletes RFCs 5077, 5246, and 6961. This document also specifies new requirements for TLS 1.2 implementations.},
    }

### Reading Identifiers From a .aux File

Consider that you have a file called `rfcs_and_ids.aux` with the following content:

    \relax
    \citation{RFC5246}
    \citation{the-documentary-2005}
    \citation{draft-ietf-tls-tls13-21}
    \citation{RFC8446}
    \bibstyle{plain}
    \bibdata{references}
    \@writefile{toc}{\contentsline {section}{\numberline {1}Introduction}{1}}
    \@writefile{lof}{\contentsline {figure}{\numberline {1}{\ignorespaces The Universe}}{1}}
    \newlabel{fig:universe}{{1}{1}}
    \@writefile{toc}{\contentsline {section}{\numberline {2}Conclusion}{1}}


If you run:

`rfcbibtex -f rfcs_and_ids.aux`

You will get the [same output as in the previous section](#example-output).

### Reading Identifiers From a .txt File

Consider that you have a file called `rfcs_and_ids.txt` with the following content:

    RFC5246
    the-documentary-2005
    draft-ietf-tls-tls13-21
    RFC8446

If you run:

`rfcbibtex -f rfcs_and_ids.aux`

You will get the [same output as in the previous section](#example-output).

### Combining Multiple Files

You can also combine multiple files with different types. You can even combine files and command line arguments.

Let's assume you have a file called `rfcs.txt` with the following content:

    RFC5246
    rFc7231

We will also use the [rfcs_and_ids.tex from a previous example](#tex-file). If you run:

`rfcbibtex rfc1234 -f rfcs.txt rfcs_and_ids.tex`

<a id="mixed-files-output"></a>You will get the following output:

    @misc{rfc7231,
            series =        {Request for Comments},
            number =        7231,
            howpublished =  {RFC 7231},
            publisher =     {RFC Editor},
            doi =           {10.17487/RFC7231},
            url =           {https://rfc-editor.org/rfc/rfc7231.txt},
            author =        {Roy T. Fielding and Julian Reschke},
            title =         {{Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content}},
            pagetotal =     101,
            year =          2014,
            month =         jun,
            abstract =      {The Hypertext Transfer Protocol (HTTP) is a stateless \textbackslash{}\%application- level protocol for distributed, collaborative, hypertext information systems. This document defines the semantics of HTTP/1.1 messages, as expressed by request methods, request header fields, response status codes, and response header fields, along with the payload of messages (metadata and body content) and mechanisms for content negotiation.},
    }

    @techreport{draft-ietf-tls-tls13-21,
            number =        {draft-ietf-tls-tls13-21},
            type =          {Internet-Draft},
            institution =   {Internet Engineering Task Force},
            publisher =     {Internet Engineering Task Force},
            note =          {Work in Progress},
            url =           {https://datatracker.ietf.org/doc/html/draft-ietf-tls-tls13-21},
            author =        {Eric Rescorla},
            title =         {{The Transport Layer Security (TLS) Protocol Version 1.3}},
            pagetotal =     143,
            year =          ,
            month =         ,
            day =           ,
            abstract =      {This document specifies version 1.3 of the Transport Layer Security (TLS) protocol. TLS allows client/server applications to communicate over the Internet in a way that is designed to prevent eavesdropping, tampering, and message forgery.},
    }

    @misc{rfc1234,
            series =        {Request for Comments},
            number =        1234,
            howpublished =  {RFC 1234},
            publisher =     {RFC Editor},
            doi =           {10.17487/RFC1234},
            url =           {https://rfc-editor.org/rfc/rfc1234.txt},
            author =        {Don Provan},
            title =         {{Tunneling IPX traffic through IP networks}},
            pagetotal =     6,
            year =          1991,
            month =         jun,
            abstract =      {This memo describes a method of encapsulating IPX datagrams within UDP packets so that IPX traffic can travel across an IP internet. {[}STANDARDS-TRACK{]} This memo defines objects for managing DS1 Interface objects for use with the SNMP protocol. {[}STANDARDS-TRACK{]}},
    }

    @misc{rfc5246,
            series =        {Request for Comments},
            number =        5246,
            howpublished =  {RFC 5246},
            publisher =     {RFC Editor},
            doi =           {10.17487/RFC5246},
            url =           {https://rfc-editor.org/rfc/rfc5246.txt},
            author =        {Eric Rescorla and Tim Dierks},
            title =         {{The Transport Layer Security (TLS) Protocol Version 1.2}},
            pagetotal =     104,
            year =          2008,
            month =         aug,
            abstract =      {This document specifies Version 1.2 of the Transport Layer Security (TLS) protocol. The TLS protocol provides communications security over the Internet. The protocol allows client/server applications to communicate in a way that is designed to prevent eavesdropping, tampering, or message forgery. {[}STANDARDS-TRACK{]}},
    }

    @misc{rfc8446,
            series =        {Request for Comments},
            number =        8446,
            howpublished =  {RFC 8446},
            publisher =     {RFC Editor},
            doi =           {10.17487/RFC8446},
            url =           {https://rfc-editor.org/rfc/rfc8446.txt},
            author =        {Eric Rescorla},
            title =         {{The Transport Layer Security (TLS) Protocol Version 1.3}},
            pagetotal =     160,
            year =          2018,
            month =         aug,
            abstract =      {This document specifies version 1.3 of the Transport Layer Security (TLS) protocol. TLS allows client/server applications to communicate over the Internet in a way that is designed to prevent eavesdropping, tampering, and message forgery. This document updates RFCs 5705 and 6066, and obsoletes RFCs 5077, 5246, and 6961. This document also specifies new requirements for TLS 1.2 implementations.},
    }

Note that **duplicate** entries have been removed.


### Output Contents To A File

Option: `-o <file_name>`

Considering  `rfcs.txt`and `rfcs_and_ids.tex` from the above above.

If you run: 

`rfcbibtex rfc1234 -f rfcs.txt rfcs_and_ids.tex -o output.bib`

A file `output.bib` would be created **or overridden** with the [the same content as in the above output](#mixed-files-output).

## Error Handling and Warning

The tool will print a warning in the following cases:

* no explicit version defined for a draft id
* drafts which have a new draft version update
* drafts which have been assigned an `RFC` number
* invalid identifier name provided as a **command-line argument** (invalid identifier names from files are simply not parsed)
* errors in fetching from URLs

It's important to note, that such errors **DO NOT break the correct functionality of the tool**. Those errors and warnings are printed out,
but **IGNORED**. The generated BibTex files are valid, even when errors are found. Errors and warnings are only printed on the console
(into the standard error output stream) and **never to the output files** (`-o` option).

Here is an example of an output of errors and warnings:

<img src="https://i.imgur.com/1YDLsBN.png" alt="RFCBibTex Errors and Warnings Example" width="50%">