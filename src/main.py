# from clients.scraper import Scraper
import logging

logging.basicConfig(level=logging.DEBUG)

# scraper_client = Scraper()
from clients.data_formatter import DataFormatter

formatter_client = DataFormatter(data_writter_mode="CLOUD")


# data = formatter_client.get_event_ids_last_round(17, 61627)
# print(data)

formatter_client.load_round_statistics(17, 61627)
# print(formatter_client.get_events_by_round(17, 61627, 5))
