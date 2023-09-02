# adapted from https://github.com/JurajNyiri/pytapo/blob/153fd77d8a1f15568870fef0ea5bd04c642a4f63/experiments/DownloadRecordings.py
from pytapo import Tapo
from pytapo.media_stream.downloader import Downloader

import asyncio
import os

import arrow

# mandatory
output_dir = os.environ.get("OUTPUT")  # directory path where videos will be saved
host = os.environ.get("HOST")  # change to camera IP
retain_days = int(os.environ.get("RETAIN_DAYS", 7))
password_cloud = os.environ.get("PASSWORD_CLOUD")  # set to your cloud password

# optional
window_size = os.environ.get(
    "WINDOW_SIZE"
)  # set to prefferred window size, affects download speed and stability, recommended: 50

print("Connecting to camera...")
tapo = Tapo(host, "admin", password_cloud, password_cloud)

def delete_old_files():
    print("deleting old files.")
    clear_from_date = arrow.utcnow().shift(days=-retain_days)
    files = os.listdir(output_dir)
    for file in files:
        start_date = file.split(" ")[0]
        arrow_start_date = arrow.get(start_date)
        if arrow_start_date < clear_from_date:
            print(f"deleting recording: {file}")
            os.remove(os.path.join(output_dir, file))

async def download_async():
    print("Getting recordings...")
    current_date = arrow.utcnow().shift(days=-(retain_days-1)).floor("day")
    while current_date < arrow.utcnow():
        current_date_formatted = current_date.format('YYYYMMDD')

        recordings = tapo.getRecordings(current_date_formatted)
        timeCorrection = tapo.getTimeCorrection()
        for recording in recordings:
            for key in recording:
                downloader = Downloader(
                    tapo,
                    recording[key]["startTime"],
                    recording[key]["endTime"],
                    timeCorrection,
                    output_dir,
                    None,
                    False,
                    window_size,
                )
                async for status in downloader.download():
                    statusString = status["currentAction"] + " " + status["fileName"]
                    if status["progress"] > 0:
                        statusString += (
                            ": "
                            + str(round(status["progress"], 2))
                            + " / "
                            + str(status["total"])
                        )
                    else:
                        statusString += "..."
                    print(
                        statusString + (" " * 10) + "\r",
                        end="",
                    )
                print("")
        current_date = current_date.shift(days=1)


delete_old_files()
loop = asyncio.get_event_loop()
loop.run_until_complete(download_async())
