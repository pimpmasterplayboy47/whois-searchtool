# WORK IN PROGRESS
- Readme and basic code are finished but project is not finished or ready for use.

# Whois Search Tool

A simple, pure Python WHOIS lookup tool that follows WHOIS referrals to get accurate domain registration information.

## Features

- Pure Python implementation (no external dependencies)
- Follows WHOIS referrals from IANA to registrar servers
- Clean, modular code structure
- Comprehensive test suite
- Easy to use command-line interface
- Proper error handling

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/whois_search_tool.git
cd whois_search_tool

# Install (optional, for development)
pip install -e .
```

## Usage

### As a module

```python
from whois_search.whois import whois_lookup

# Lookup a domain
result = whois_lookup("example.com")
print(result)

# Parse the response into a dictionary
from whois_search.whois import parse_whois_response
parsed = parse_whois_response(result)
print(parsed["registrar"])
```

### Command line

```bash
# Direct execution
python -m whois_search.whois example.com

# Or run the script directly
python whois_search/whois.py example.com
```

## Running Tests

```bash
# Run the test suite
python -m unittest discover tests

# Or run specific test file
python -m unittest tests.test_whois
```

## How It Works

1. Queries IANA's WHOIS server (whois.iana.org) for the initial domain
2. Parses the response to find the registrar's WHOIS server
3. Queries the registrar's WHOIS server for detailed information
4. Returns the complete WHOIS record

## Limitations

- Basic implementation - doesn't handle all WHOIS response formats
- No caching mechanism
- Rate limiting not implemented (be respectful when querying)
- Some TLDs may have different WHOIS structures

## Limitations may be improved upon future revisions

- For now this is simply a passion project with the goal of improving
