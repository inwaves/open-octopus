import asyncio
import os
from datetime import datetime, timedelta
from collections import defaultdict
from open_octopus.client import OctopusClient

async def main():
    api_key = os.environ.get("OCTOPUS_API_KEY", "")
    account = os.environ.get("OCTOPUS_ACCOUNT", "")
    mpan = os.environ.get("OCTOPUS_MPAN")
    meter_serial = os.environ.get("OCTOPUS_METER_SERIAL")
    
    print(f"MPAN: {mpan}")
    print(f"Meter Serial: {meter_serial}")
    
    client = OctopusClient(
        api_key=api_key,
        account=account,
        mpan=mpan,
        meter_serial=meter_serial
    )
    
    async with client:
        print("\n=== Fetching consumption data ===")
        consumption = await client.get_consumption(periods=96)
        print(f"Total consumption records: {len(consumption)}")
        
        if consumption:
            print(f"\nFirst few records:")
            for c in consumption[:5]:
                print(f"  {c.start} - {c.end}: {c.kwh} kWh")
            
            # Debug the grouping logic from menubar_server.py
            daily = defaultdict(float)
            hourly_by_day = defaultdict(lambda: defaultdict(float))
            
            for c in consumption:
                day = c.start.strftime("%Y-%m-%d")
                hour = c.start.hour
                daily[day] += c.kwh
                hourly_by_day[day][hour] += c.kwh
            
            print(f"\nDaily totals:")
            for day, kwh in sorted(daily.items()):
                print(f"  {day}: {kwh:.2f} kWh")
            
            sorted_days = sorted(daily.keys(), reverse=True)
            print(f"\nSorted days (newest first): {sorted_days}")
            
            today = datetime.now().strftime("%Y-%m-%d")
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            print(f"\nCurrent date strings:")
            print(f"  today = {today}")
            print(f"  yesterday = {yesterday}")
            
            print(f"\nData availability:")
            print(f"  today in daily: {today in daily}")
            print(f"  yesterday in daily: {yesterday in daily}")

if __name__ == "__main__":
    asyncio.run(main())
