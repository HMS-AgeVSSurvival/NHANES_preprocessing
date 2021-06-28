import os
import time
import numpy as np
import gspread


def get_worksheet(main_category):
    service_acccount_id = np.random.randint(1, 6)
    gc = gspread.service_account(filename=f"credentials/credentials_{service_acccount_id}.json")
    google_sheet = gc.open_by_key(os.environ.get("GOOGLE_SPLIT_SHEET_ID"))
    
    return google_sheet.worksheet(main_category)


def update_cell(main_category, row, col, value):
    cell_updated = False
    while not cell_updated:
        try:
            worksheet = get_worksheet(main_category)
            worksheet.update_cell(row, col, value)
            cell_updated = True
        except gspread.exceptions.APIError:  # Means too many Google Sheet API's calls
            sleep_time = np.random.randint(101, 1000)
            print(f"Sleep {sleep_time}")
            time.sleep(sleep_time)


def find_cell(main_category, name):
    got_cell = False
    while not got_cell:
        try:
            worksheet = get_worksheet(main_category)
            cell = worksheet.find(name)
            got_cell = True
        except gspread.exceptions.APIError:  # Means too many Google Sheet API's calls
            sleep_time = np.random.randint(101, 1000)
            print(f"Sleep {sleep_time}")
            time.sleep(sleep_time)

    return cell


def get_col_values(main_category, col):
    got_col = False
    while not got_col:
        try:
            worksheet = get_worksheet(main_category)
            col_values = worksheet.col_values(col)
            got_col = True
        except gspread.exceptions.APIError:  # Means too many Google Sheet API's calls
            sleep_time = np.random.randint(101, 1000)
            print(f"Sleep {sleep_time}")
            time.sleep(sleep_time)

    return col_values