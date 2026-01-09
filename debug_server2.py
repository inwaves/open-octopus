import asyncio
import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict
from open_octopus.client import OctopusClient

async def main():
    api_key = os.environ.get("OCTOPUS_API_KEY", "")
    account = os.environ.get("OCTOPUS_ACCOUNT", "")
    mpan = os.environ.get("OCTOPUS_MPAN")
    meter_serial = os.environ.get("OCTOPUS_METER_SERIAL")
    
    print(f"API Key: {api_key[:10]}...")
    print(f"Account: {account}")
    print(f"MPAN: {mpan} (type: {type(mpan)})")
    print(f"Meter Serial: {meter_serial} (type: {type(meter_serial)})")
    
    client = OctopusClient(
        api_key=api_key,
        account=account,
        mpan=mpan,
        meter_serial=meter_serial
    )
    
    print(f"\nClient MPAN: {client.mpan}")
    print(f"Client meter_serial: {client.meter_serial}")
    print(f"Has MPAN and serial: {client.mpan and client.meter_serial}")
    
    async with client:
        print("\n=== Testing get_smart_devices ===")
        try:
            devices = await client.get_smart_devices()
            print(f"Devices: {devices}")
        except Exception as e:
            print(f"get_smart_devices error: {e}")
        
        print("\n=== Testing get_consumption ===")
        if client.mpan and client.meter_serial:
            try:
                consumption = await client.get_consumption(periods=96)
                print(f"Got {len(consumption)} records")
                
                daily = defaultdict(float)
                for c in consumption:
                    day = c.start.strftime("%Y-%m-%d")
                    daily[day] += c.kwh
                
                sorted_days = sorted(daily.keys(), reverse=True)
                print(f"Sorted days: {sorted_days}")
                
                latest_day = sorted_days[0] if sorted_days else None
                prev_day = sorted_days[1] if len(sorted_days) > 1 else None
                
                print(f"latest_day: {latest_day}")
                print(f"prev_day: {prev_day}")
                
                today = datetime.now().strftime("%Y-%m-%d")
                display_today = latest_day if latest_day else today
                
                print(f"\ndisplay_today: {display_today}")
                print(f"display_today in daily: {display_today in daily}")
                if display_today in daily:
                    print(f"today_kwh would be: {daily[display_today]}")
                    
            except Exception as e:
                import traceback
                print(f"get_consumption error: {e}")
                traceback.print_exc()
        else:
            print("MPAN or meter_serial missing!")

if __name__ == "__main__":
    asyncio.run(main())
