"""
Whois lookup module.
"""

import socket
import traceback
from typing import Optional, Dict, Any


def whois_lookup(domain: str, server: str = "whois.iana.org", port: int = 43) -> str:
    """
    Perform a basic WHOIS lookup for a domain.

    Args:
        domain: The domain name to look up
        server: WHOIS server to query (default: whois.iana.org)
        port: WHOIS server port (default: 43)

    Returns:
        WHOIS response as a string

    Raises:
        ConnectionError: If unable to connect to WHOIS server
        TimeoutError: If the connection times out
    """
    # Clean the domain
    domain = domain.strip().lower()
    if not domain:
        raise ValueError("Domain cannot be empty")

    # Remove protocol if present
    if "://" in domain:
        domain = domain.split("://")[1]
    # Remove path if present
    if "/" in domain:
        domain = domain.split("/")[0]

    # First, get the referral server from IANA
    try:
        response = _query_whois_server(domain, server, port)
        # Parse the response to find the registrar WHOIS server
        whois_server = _extract_whois_server(response)
        if whois_server and whois_server.lower() != server.lower():
            # Query the registrar's WHOIS server
            return _query_whois_server(domain, whois_server, port)
        else:
            return response
    except Exception as e:
        # If we get an error, try to return what we got or raise
        if 'response' in locals():
            return response
        raise


def _query_whois_server(domain: str, server: str, port: int, timeout: float = 10.0) -> str:
    """
    Query a specific WHOIS server.

    Args:
        domain: Domain to query
        server: WHOIS server hostname
        port: WHOIS server port
        timeout: Connection timeout in seconds

    Returns:
        Raw WHOIS response
    """
    # Convert server to IP if needed
    try:
        ip = socket.gethostbyname(server)
    except socket.gaierror:
        raise ConnectionError(f"Unable to resolve WHOIS server: {server}")

    # Create socket connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        sock.connect((ip, port))
        # Send query with CRLF
        sock.sendall(f"{domain}\r\n".encode("utf-8"))

        # Receive response
        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data

        return response.decode("utf-8", errors="ignore")
    finally:
        sock.close()


def _extract_whois_server(response: str) -> Optional[str]:
    """
    Extract WHOIS server from WHOIS response.

    Looks for lines like:
    ReferralURL:   http://www.example.net
    or
    whois: whois.example.net
    or
    whois server: whois.example.net
    or
    Registrar WHOIS Server: whois.example.net

    Args:
        response: Raw WHOIS response

    Returns:
        WHOIS server hostname or None if not found
    """
    lines = response.split("\n")
    for line in lines:
        line = line.strip()
        # Common patterns for WHOIS server referral
        if line.lower().startswith("whois server:"):
            return line.split(":", 1)[1].strip()
        elif line.lower().startswith("registrar whois server:"):
            return line.split(":", 1)[1].strip()
        elif line.lower().startswith("whois:"):
            return line.split(":", 1)[1].strip()
        elif line.lower().startswith("referral url:"):
            # Extract domain from URL
            url = line.split(":", 1)[1].strip()
            # Simple extraction - in reality would need proper URL parsing
            if "://" in url:
                url = url.split("://")[1]
            if "/" in url:
                url = url.split("/")[0]
            return url
    return None


def parse_whois_response(response: str) -> Dict[str, Any]:
    """
    Parse WHOIS response into a dictionary.

    Args:
        response: Raw WHOIS response string

    Returns:
        Dictionary of parsed WHOIS fields
    """
    parsed = {}
    current_key = None

    for line in response.split("\n"):
        line = line.strip()
        if not line:
            continue

        # Check if line contains a key-value pair
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip().lower().replace(" ", "_")
            value = value.strip()
            parsed[key] = value
            current_key = key
        elif current_key and line:
            # Continuation of previous value
            parsed[current_key] += " " + line

    return parsed


if __name__ == "__main__":
    # Simple test when run directly
    import sys
    if len(sys.argv) > 1:
        domain = sys.argv[1]
        try:
            result = whois_lookup(domain)
            print(result)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: python whois.py <domain>", file=sys.stderr)
        sys.exit(1)