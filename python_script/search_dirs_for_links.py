import calendar
import os
from datetime import datetime
from download_fits import create_dir_n_download_fits



print("\n----------------------\nFits Download Script\n----------------------\n")
print(f"Starting Date&time: {datetime.today()}\n\n")

starting_link = "http://jsoc.stanford.edu/data/hmi/fits"
base_path = os.getcwd()


# formatting days and months
def check_for_iregular(day='', month=''):
    if (day != '') and (len(str(day)) < 2):
        return "0" + str(day)
    if (month != '') and (len(str(month)) < 2):
        return "0" + str(month)
    return str(day) + str(month)


# creating download url
def create_url(year, month, day):
    day = check_for_iregular(day, '')
    month = check_for_iregular('', month)
    return starting_link + "/" + str(year) + "/" + str(month) + "/" + str(day)


# creating path where fits files fill be saved
def create_full_path(year, month, day):
    return os.path.join(base_path, "Downloaded_fits", str(year), str(month), str(day))


def check_for_downloaded():
    last_download = None

    for year in range(2010, int(datetime.today().year) + 1):
        for month in range(1, 13):
            for day in range(1, calendar.monthrange(year, month)[1] + 1):
                if os.path.exists(create_full_path(year, month, day)):
                    last_download = (year, month, day)
                else:
                    return last_download

    return None


last_downloaded_date = check_for_downloaded()

if last_downloaded_date:
    year, month, day = last_downloaded_date
    print(f"Resuming download from {year}-{month:02d}-{day}")

    for y in range(year, int(datetime.today().year) + 1):
        start_month = month if y == year else 1

        for m in range(start_month, 13):
            start_day = day if y == year and m == month else 1
            max_day = calendar.monthrange(y, m)[1]

            for d in range(start_day, max_day + 1):
                print(f"\n\n----------------------\n>>>Now downloading: {y} / {m:02d} / {d}\n----------------------")
                create_dir_n_download_fits(create_url(y, m, d), create_full_path(y, m, d))
                print(">>>Done")

            # Reset the day for the next month
            day = 1

        # Reset the month for the next year
        month = 1
else:
    print(">>>Starting the download process from scratch.")
    for year in range(2010, int(datetime.today().year) + 1):
        for month in range(1, 13):
            for day in range(1, calendar.monthrange(year, month)[1] + 1):
                print(f"\n\n----------------------\nNow downloading: {year} / {month} / {day}\n----------------------")
                create_dir_n_download_fits(create_url(year, month, day), create_full_path(year, month, day))
                print(">>>Done")


print("\n\n----------------------\n>>>All downloads finnished!\n----------------------")                
