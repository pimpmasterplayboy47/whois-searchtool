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

## Project Structure

```
whois_search_tool/
├── whois_search/           # Main package
│   ├── __init__.py
│   └── whois.py            # Core WHOIS implementation
├── tests/                  # Test suite
│   ├── __init__.py
│   └── test_whois.py
├── docs/                   # Documentation (to be expanded)
├── README.md
└── requirements.txt        # Empty for now (pure Python)
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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

MIT License - see the LICENSE file for details (to be added)