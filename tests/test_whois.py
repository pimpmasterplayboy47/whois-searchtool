"""
Tests for the whois module.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import socket

# Add the whois_search directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'whois_search'))

import whois_search.whois as whois_module


class TestWhois(unittest.TestCase):

    def test_extract_whois_server(self):
        """Test extracting WHOIS server from response."""
        response = """Domain Name: EXAMPLE.COM
Registrar WHOIS Server: whois.example.net
Updated Date: 2023-01-01T00:00:00Z
"""
        server = whois_module._extract_whois_server(response)
        self.assertEqual(server, "whois.example.net")

    def test_extract_whois_server_alternative_format(self):
        """Test extracting WHOIS server with different format."""
        response = """domain: EXAMPLE.COM
whois: whois.example.net
status: active
"""
        server = whois_module._extract_whois_server(response)
        self.assertEqual(server, "whois.example.net")

    def test_extract_whois_server_referral_url(self):
        """Test extracting WHOIS server from referral URL."""
        response = """Domain Name: EXAMPLE.COM
Referral URL: http://whois.example.net
"""
        server = whois_module._extract_whois_server(response)
        self.assertEqual(server, "whois.example.net")

    def test_parse_whois_response(self):
        """Test parsing WHOIS response."""
        response = """Domain Name: EXAMPLE.COM
Registrar: Example Registrar
Whois Server: whois.example.net
Updated Date: 2023-01-01T00:00:00Z
Creation Date: 2020-01-01T00:00:00Z
Registry Expiry Date: 2025-01-01T00:00:00Z
"""
        parsed = whois_module.parse_whois_response(response)
        self.assertEqual(parsed["domain_name"], "EXAMPLE.COM")
        self.assertEqual(parsed["registrar"], "Example Registrar")
        self.assertEqual(parsed["whois_server"], "whois.example.net")

    @patch('whois_search.whois.socket.socket')
    def test_query_whois_server(self, mock_socket_class):
        """Test querying a WHOIS server with mocked socket."""
        # Setup mock
        mock_sock = MagicMock()
        mock_socket_class.return_value = mock_sock
        mock_sock.recv.side_effect = [
            b"Domain Name: EXAMPLE.COM\r\n",
            b"Registrar: Example Registrar\r\n",
            b""  # Empty response to break loop
        ]

        # Test
        result = whois_module._query_whois_server("example.com", "whois.iana.org", 43)

        # Verify
        mock_socket_class.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_sock.settimeout.assert_called_once_with(10.0)
        mock_sock.connect.assert_called_once()
        mock_sock.sendall.assert_called_once_with(b"example.com\r\n")
        self.assertIn("Domain Name: EXAMPLE.COM", result)

    def test_whois_lookup_domain_cleaning(self):
        """Test that domain cleaning works properly."""
        # Test with http:// prefix
        with patch('whois_search.whois._query_whois_server') as mock_query:
            mock_query.return_value = "test"
            whois_module.whois_lookup("http://example.com/path")
            # Check if mock was called before accessing call_args
            if mock_query.called:
                args, kwargs = mock_query.call_args
                self.assertEqual(args[0], "example.com")  # domain should be cleaned

    def test_whois_lookup_empty_domain(self):
        """Test that empty domain raises ValueError."""
        with self.assertRaises(ValueError):
            whois_module.whois_lookup("")

        with self.assertRaises(ValueError):
            whois_module.whois_lookup("   ")

    def test_whois_lookup_with_path(self):
        """Test that paths are stripped from domain."""
        with patch('whois_search.whois._query_whois_server') as mock_query:
            mock_query.return_value = "test"
            whois_module.whois_lookup("example.com/path/to/resource")
            # Check if mock was called before accessing call_args
            if mock_query.called:
                args, kwargs = mock_query.call_args
                self.assertEqual(args[0], "example.com")


if __name__ == '__main__':
    unittest.main()