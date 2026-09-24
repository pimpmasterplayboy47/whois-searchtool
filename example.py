"""
Example usage of the whois search tool.
"""

from whois_search.whois import whois_lookup, parse_whois_response

if __name__ == "__main__":
    # Example domains to lookup
    domains = [
        "example.com",
        "google.com",
        "github.com"
    ]

    for domain in domains:
        print(f"\n{'='*50}")
        print(f"WHOIS lookup for: {domain}")
        print('='*50)

        try:
            # Perform the lookup
            result = whois_lookup(domain)

            # Parse the result for easier reading
            parsed = parse_whois_response(result)

            # Display key information
            print(f"Domain: {parsed.get('domain_name', 'N/A')}")
            print(f"Registrar: {parsed.get('registrar', 'N/A')}")
            print(f"Creation Date: {parsed.get('creation_date', 'N/A')}")
            print(f"Expiry Date: {parsed.get('registry_expiry_date', 'N/A')}")
            print(f"Updated Date: {parsed.get('updated_date', 'N/A')}")

            # Show raw response (first 500 chars)
            print(f"\nRaw Response (first 500 chars):")
            print("-" * 30)
            print(result[:500] + ("..." if len(result) > 500 else ""))

        except Exception as e:
            print(f"Error looking up {domain}: {e}")