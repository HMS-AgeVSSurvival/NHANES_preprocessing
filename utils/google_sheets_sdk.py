import os
import time
import numpy as np
import gspread
import requests
import json
from json.decoder import JSONDecodeError


def get_worksheet(main_category):
    service_account_id = np.random.randint(1, 6)
    gc = gspread.service_account(
        filename=f"credentials/credentials_{service_account_id}.json"
    )
    google_sheet = gc.open_by_key(os.environ.get("GOOGLE_SPLIT_SHEET_ID"))

    return google_sheet.worksheet(main_category)


def handle_gspread_error(error):
    try:
        error = json.loads(error.response._content)
    except JSONDecodeError:
        raise error

    if error["error"]["code"] in [
        404,
        429,
        101,
        500,
    ]:  # Means too many Google Sheet API's calls
        sleep_time = 61
        print(f"Sleep {sleep_time}")
        time.sleep(sleep_time)
    else:
        raise error


def update_cell(sheet_name, row, col, value):
    cell_updated = False
    while not cell_updated:
        try:
            worksheet = get_worksheet(sheet_name)
            worksheet.update_cell(row, col, str(value))
            cell_updated = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)
        except requests.exceptions.ReadTimeout:
            pass


def find_cell(sheet_name, name):
    got_cell = False
    while not got_cell:
        try:
            worksheet = get_worksheet(sheet_name)
            cell = worksheet.find(name)
            got_cell = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)
        except requests.exceptions.ReadTimeout:
            pass

    return cell


def findall_cells(sheet_name, name):
    got_cell = False
    while not got_cell:
        try:
            worksheet = get_worksheet(sheet_name)
            cells = worksheet.findall(name)
            got_cell = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)
        except requests.exceptions.ReadTimeout:
            pass

    return cells


def get_cell(sheet_name, row, col):
    got_cell = False
    while not got_cell:
        try:
            worksheet = get_worksheet(sheet_name)
            cell = worksheet.cell(row, col)
            got_cell = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)
        except requests.exceptions.ReadTimeout:
            pass

    return cell


def get_col_values(sheet_name, col_name):
    col = find_cell(sheet_name, col_name).col

    got_col = False
    while not got_col:
        try:
            worksheet = get_worksheet(sheet_name)
            col_values = worksheet.col_values(col)
            got_col = True
        except gspread.exceptions.APIError as error_gspread:
            handle_gspread_error(error_gspread)
        except requests.exceptions.ReadTimeout:
            pass

    return col_values
