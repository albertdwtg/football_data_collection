import sys
import os

sys.path.append(os.path.abspath("../src"))
from clients.data_formatter import DataFormatter


class TestClassDataFormatter:
    def test_get_event_statistics(self):
        formatter_client = DataFormatter(data_writter_mode="LOCAL")
        request_uuid, json_response = formatter_client.get_event_statistics(
            event_id=11352546
        )
        assert len(request_uuid) == 8
        assert isinstance(json_response, dict)
        assert "statistics" in json_response
        assert isinstance(json_response["statistics"], list)

    def test_get_event_ids_by_round(self):
        formatter_client = DataFormatter(data_writter_mode="LOCAL")
        request_uuid, event_ids = formatter_client.get_event_ids_by_round(
            tournament_id=17, season_id=52186, round_id=38
        )
        assert len(request_uuid) == 8
        assert isinstance(event_ids, list)
