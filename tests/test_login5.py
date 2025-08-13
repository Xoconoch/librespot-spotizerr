#!/usr/bin/env python3
"""
Test script to verify Login5 authentication is working
"""

import logging
import sys
import os
from librespot.core import Session

# Enable debug logging to see what's happening
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_with_stored_credentials():
    """Test using stored credentials (if available)"""
    print("=== Testing with stored credentials ===")
    
    try:
        if os.path.exists("credentials.json"):
            session = Session.Builder().stored_file("credentials.json").create()
            print(f"✓ Successfully authenticated as: {session.username()}")
            
            # Test token retrieval
            token_provider = session.tokens()
            try:
                token = token_provider.get("playlist-read")
                print(f"✓ Successfully got playlist-read token: {token[:20]}...")
                
                # Check if Login5 token is available
                login5_token = session.get_login5_token()
                if login5_token:
                    print(f"✓ Login5 token available: {login5_token[:20]}...")
                else:
                    print("⚠ Login5 token not available")
                
                session.close()
                return True
            except Exception as e:
                print(f"✗ Token retrieval failed: {e}")
                session.close()
                return False
        else:
            print("⚠ No credentials.json file found")
            return False
            
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        return False

def test_with_username_password():
    """Test with username/password (requires user input)"""
    print("\n=== Testing with username/password ===")
    
    username = input("Enter Spotify username (or press Enter to skip): ").strip()
    if not username:
        print("Skipping username/password test")
        return False
        
    password = input("Enter Spotify password: ").strip()
    if not password:
        print("Skipping username/password test")
        return False
    
    try:
        session = Session.Builder().user_pass(username, password).create()
        print(f"✓ Successfully authenticated as: {session.username()}")
        
        # Test token retrieval
        token_provider = session.tokens()
        try:
            token = token_provider.get("playlist-read")
            print(f"✓ Successfully got playlist-read token: {token[:20]}...")
            
            # Check if Login5 token is available
            login5_token = session.get_login5_token()
            if login5_token:
                print(f"✓ Login5 token available: {login5_token[:20]}...")
            else:
                print("⚠ Login5 token not available")
            
            session.close()
            return True
        except Exception as e:
            print(f"✗ Token retrieval failed: {e}")
            session.close()
            return False
            
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        return False

def main():
    print("Testing Login5 Authentication Implementation")
    print("=" * 50)
    
    # Test 1: Stored credentials
    stored_success = test_with_stored_credentials()
    
    # Test 2: Username/password (optional)
    manual_success = test_with_username_password()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Stored credentials: {'✓ PASS' if stored_success else '✗ FAIL'}")
    print(f"Username/password: {'✓ PASS' if manual_success else '✗ FAIL'}")
    
    if stored_success or manual_success:
        print("\n🎉 Login5 authentication is working!")
        return 0
    else:
        print("\n⚠ Could not test authentication - no valid credentials")
        return 1

if __name__ == "__main__":
    sys.exit(main())