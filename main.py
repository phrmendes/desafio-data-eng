from pipelines.settings import Settings
from pipelines.terceirizados import data

if __name__ == "__main__":
    settings = Settings()
    urls = data.get_links(settings)
    data.get_data(urls)
