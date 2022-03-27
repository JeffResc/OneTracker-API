![PyPI](https://img.shields.io/pypi/v/onetracker-api)
![PyPI - Downloads](https://img.shields.io/pypi/dm/onetracker)
![GitHub](https://img.shields.io/github/license/JeffResc/OneTracker-API)
# OneTracker-API
Asynchronous Python client for OneTracker.

## Installing
```bash
pip install onetracker-api
```

# Quick-Start Example
```python
import asyncio

from onetracker_api import OneTracker

async def main():
    async with OneTracker() as onetracker:
        # Authenticate with the OneTracker API
        await onetracker.login("demo@onetracker.app", "P@S5W0RD!")
        # > AuthenticationTokenResponse(message='ok', session=SessionObject(user_id=156, token='eP0FUZhN76Wu7igUkCPigR2wEMBDtzaW', expiration=datetime.datetime(2020, 8, 3, 3, 15, 54)))

        # Get a list of parcels, archived defaults to false
        parcels = await onetracker.list_parcels(archived=False)
        # > ListParcelsResponse(message='ok', parcels=[Parcel(id=174, user_id=6, email_id=183, email_sender='example.com', retailer_name='Example', description='Camera', notification_level=1, is_archived=0, carrier='FedEx', carrier_name='FedEx', carrier_redirection_available=True, tracker_cached=False, tracking_id='407072905722', tracking_url='', tracking_status='delivered', tracking_status_description='', tracking_status_text='', tracking_extra_info='', tracking_location='Sunnyvale, CA', tracking_time_estimated=datetime.datetime(2018, 8, 8, 20, 0, 0), tracking_time_delivered=datetime.datetime(2018, 8, 8, 15, 51, 0), tracking_lock=0, tracking_events=[], time_added=datetime.datetime(2018, 8, 7, 0, 50, 30), time_updated=datetime.datetime(2018, 8, 18, 20, 1, 23))])

        # Get a single parcel
        parcel = await onetracker.get_parcel(id=174)
        # > GetParcelResponse(message='ok', parcel=Parcel(id=174, user_id=6, email_id=183, email_sender='example.com', retailer_name='Example', description='Camera', notification_level=1, is_archived=0, carrier='FedEx', carrier_name='FedEx', carrier_redirection_available=True, tracker_cached=False, tracking_id='407072905722', tracking_url='', tracking_status='delivered', tracking_status_description='', tracking_status_text='', tracking_extra_info='', tracking_location='Sunnyvale, CA', tracking_time_estimated=datetime.datetime(2018, 8, 8, 20, 0, 0), tracking_time_delivered=datetime.datetime(2018, 8, 8, 15, 51, 0), tracking_lock=0, tracking_events=[], time_added=datetime.datetime(2018, 8, 7, 0, 50, 30), time_updated=datetime.datetime(2018, 8, 18, 20, 1, 23)))

        # Delete a parcel
        parcel = await onetracker.delete_parcel(id=174)
        # > DeleteParcelResponse(message='ok')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

- [See the full documentation](https://jeffresc.dev/OneTracker-API/)

## See Also
- [PyPi Project](https://pypi.org/project/onetracker-api/)
- [GitHub Project](https://github.com/JeffResc/OneTracker-API)
- [OneTracker API Reference](https://support.onetracker.app/apis/)
