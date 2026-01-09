#!/usr/bin/env python3
"""Debug script to test Octopus API consumption endpoint."""

import asyncio
import os
import sys
import httpx

# Credentials from environment
API_KEY = os.environ.get("OCTOPUS_API_KEY", "")
ACCOUNT = os.environ.get("OCTOPUS_ACCOUNT", "")
MPAN = os.environ.get("OCTOPUS_MPAN", "")
METER_SERIAL = os.environ.get("OCTOPUS_METER_SERIAL", "")

REST_API_URL = "https://api.octopus.energy/v1"

async def test_consumption():
    print(f"API Key: {API_KEY[:10]}...{API_KEY[-4:]}")
    print(f"Account: {ACCOUNT}")
    print(f"MPAN: {MPAN}")
    print(f"Meter Serial: {METER_SERIAL}")
    print()
    
    if not all([API_KEY, ACCOUNT, MPAN, METER_SERIAL]):
        print("ERROR: Missing required environment variables")
        sys.exit(1)
    
    url = f"{REST_API_URL}/electricity-meter-points/{MPAN}/meters/{METER_SERIAL}/consumption/"
    print(f"URL: {url}")
    print()
    
    async with httpx.AsyncClient() as client:
        # Test 1: Basic request with default params
        print("=== Test 1: Basic request (default params) ===")
        resp = await client.get(
            url,
            params={"page_size": 10},
            auth=(API_KEY, "")
        )
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text[:500]}...")
        print()
        
        # Test 2: Check what the actual API returns
        print("=== Test 2: Full response JSON ===")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Total count: {data.get('count', 'N/A')}")
            print(f"Results count: {len(data.get('results', []))}")
            print(f"Next page: {data.get('next')}")
            print(f"Previous page: {data.get('previous')}")
            if data.get('results'):
                print("\nFirst result:")
                print(data['results'][0])
                print("\nLast result:")
                print(data['results'][-1])
        else:
            print(f"Error response: {resp.text}")

if __name__ == "__main__":
    asyncio.run(test_consumption())