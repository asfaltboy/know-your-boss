# Know your boss

A tool to quickly collect info on companies when considering them as your
employer.

This info includes basic info from [Crunchbase][crunchbase], as well as scores
from [Glassdoor][glassdoor].

**Disclaimer**: this tool is meant for educational demonstration purpose only.
The maintainers of this repo do not take responsibility over misuse that breaks
any site's terms or conditions.

## Usage

This is a CLI tool (in the future a web UI may be added), you invoke it with:

```bash
kyb <company-name>
```

This starts by searching [Crunchbase][crunchbase] for the name, once you find
the company, it will scrape it's detail page, using your authenticated Cookie
if you set `CRUNCHBASE_COOKIE`, and then proceed to scrape
[Glassdoor][glassdoor].

## Installing

```bash
pip install <git-repo>
```

## Architecture

The tool uses [curl-cffi][curl-cffi] to pretend a browser as we retrieve the
page, as it's the simplest way to bypass basic restrictions on scraping that
some sites have.

The retrieved data is stored in a `.temp` directory relative to the directory
you run the tool from. This includes the raw files (either HTML or JSON) as
well as a Sqlite DB file.

[curl-cffi]: https://curl-cffi.readthedocs.io/
[crunchbase]: https://www.crunchbase.com/
[glassdoor]: https://www.glassdoor.co.uk/
