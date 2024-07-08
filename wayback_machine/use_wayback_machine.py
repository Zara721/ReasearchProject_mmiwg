import asyncio
import datetime
from waybackpy import WaybackMachineCDXServerAPI

# optimze code to grab urls from import, or txt file

urls_to_check = []

print("Checking", len(urls_to_check), "urls")


async def fetch_oldest_snapshot(url):
    """
    Fetches the oldest snapshot of the given URL.
    Returns a tuple (title, body_text) if successful, else None.
    """
    try:
        # Instantiate the CDX Server API
        cdx_api = WaybackMachineCDXServerAPI(url)

        # Retrieve snapshots
        snapshots = list(cdx_api.snapshots())

        # Check if we found any snapshots
        if snapshots:
            # Select the oldest snapshot
            oldest_snapshot = snapshots[0]
            # print(oldest_snapshot.timestamp)

            # Use the snapshot URL to fetch the page content
            # Construct the original URL for the oldest snapshot
            # Format: http://web.archive.org/web/<timestamp>/<original_url>
            original_url = f"http://web.archive.org/web/{oldest_snapshot.timestamp}/{oldest_snapshot.original}"
            print(original_url)
            with open('output_files/wayback_urls3.txt', 'a') as file:
                file.write(str(original_url) + '\n')
            return original_url
        else:
            print("no snapshot")
            return "no snapshot", f"No snapshots found for {url}"
    except Exception as e:
        print({str(e)})
        with open('output_files/retry_wayback.txt', 'a') as file:
            file.write(str(url) + '\n')
        return None, f"Error fetching {url}: {str(e)}"


# Initialize lists to hold results
successful_fetches = []
failed_fetches = []


async def main(url_list):
    async with asyncio.Semaphore(10):  # Limit concurrency to 10
        tasks = [fetch_oldest_snapshot(url) for url in url_list]
        for task in asyncio.as_completed(tasks):
            result = await task
            if result[0] is not None and result[0] != "no snapshot":
                successful_fetches.append(result)
            else:
                failed_fetches.append(result)


start_time = datetime.datetime.now()

asyncio.run(main(urls_to_check))

end_time = datetime.datetime.now()

elapsed_time = end_time - start_time

print("Successful Fetches:")
print(successful_fetches)

print("\nFailed Fetches:")
print(failed_fetches)

print(f"Code took {elapsed_time}.")
