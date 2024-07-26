import gc
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from janitor import clean_names, remove_empty
from loguru import logger
from requests import get

import pipelines.terceirizados.constants as const
from pipelines.settings import Settings
from pipelines.terceirizados.db import import_csv, is_data_present

read_csv = partial(
    pd.read_csv,
    sep=";",
    na_values=const.NA_VALUES,
    dtype=object,
)

read_excel = partial(
    pd.read_excel,
    na_values=const.NA_VALUES,
    dtype=object,
)


def get_date_extension(url: str) -> tuple[str, str]:
    """Get the date and the extension from the file in the URL."""
    file_name = url.split("/")[-1]
    name, extension = file_name.split(".")

    date = (
        name.removeprefix("terceirizados")
        .removeprefix("-")
        .removeprefix("_")
        .removesuffix("_1")
    )

    year = date[:4]
    month = date[4:]

    date = f"{year}-{month}-01"

    return date, extension


def add_date_column(data: pd.DataFrame) -> pd.DataFrame:
    """Create a date column in the YYYY-MM-DD format."""
    month = const.DATE_COLUMNS[0]
    year = const.DATE_COLUMNS[1]
    date = pd.to_datetime(data[year].astype(str) + "-" + data[month].astype(str))
    data = data.assign(date=date)

    return data.drop(const.DATE_COLUMNS, axis=1)


def check_header(data: pd.DataFrame) -> pd.DataFrame:
    """Add a header to the data.

    It checks if the header is correct. If it is not, it will get
    the first line of the data and consider as the first line of
    the dataframe and add the correct header.
    """
    first_line = list(data.columns)
    header = list(const.COLUMNS)

    if first_line != header:
        first_line = pd.DataFrame(first_line).transpose()

        for df in [first_line, data]:
            df.columns = header

        return pd.concat([first_line, data], ignore_index=True)

    return data


def handle_numeric_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Handle numeric columns with special characters."""
    for column in const.NUMERIC_COLUMNS:
        data[column] = (
            data[column]
            .astype(str)
            .str.replace(",", ".")
            .str.replace("_", "")
            .astype(float)
        )

    return data


@logger.catch
def clear(data: pd.DataFrame) -> pd.DataFrame:
    """Aggregate all cleaning steps."""
    return (
        data.pipe(remove_empty)
        .pipe(check_header)
        .pipe(clean_names)
        .pipe(handle_numeric_columns)
        .pipe(add_date_column)
    )


@logger.catch
def download(url: str) -> None:
    """Download a spreadsheet."""
    date, ext = get_date_extension(url)

    if is_data_present(date):
        logger.info(f"Data already present - date: {date}")
        return

    tempfile = Path(f"output/{date}.csv")
    tempfile.parent.mkdir(exist_ok=True)

    logger.info(f"Downloading - date: {date}, extension: {ext}")

    try:
        data = read_csv(url) if ext == "csv" else read_excel(url)
    except UnicodeDecodeError:
        logger.error("Encoding error")
        logger.info("Using latin-1 encoding")
        data = read_csv(url, encoding="latin-1")
    finally:
        logger.success("Download completed")

    data.pipe(clear).to_csv(tempfile, index=False)

    del data
    gc.collect()


def get_links(settings: Settings) -> list[str]:
    """Get all spreadsheets from the website."""
    response = get(settings.BASE_URL, timeout=const.REQUEST_TIMEOUT)
    page = BeautifulSoup(response.text, "html.parser")
    divs = page.find_all("div", {"class": const.DOWNLOAD_LINK_CLASS})

    return [
        anchor["href"]
        for div in divs
        for anchor in div.find_all("a")
        if anchor["href"].endswith((".csv", ".xlsx"))
    ]


def get_data(urls: list[str], max_workers: int = 6) -> None:
    """Run pipeline."""
    with ThreadPoolExecutor(max_workers) as executor:
        executor.map(download, urls)

    import_csv(Path("output"))
