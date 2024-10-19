"""Module to handle response from specific API"""

from datetime import datetime

from clients.data_writter import DataWritter
from clients.scraper import Scraper
from constants import REFERENCE_TEAMS, API_BASE_URL


class DataFormatter:
    """Object that parse JSON response from API"""

    def __init__(self, data_writter_mode):
        self.scraper = Scraper()
        self.data_writter = DataWritter(data_writter_mode)

    def get_event_statistics(self, event_id: int):
        """_summary_

        Args:
            event_id (int): _description_

        Returns:
            _type_: _description_
        """
        request_uuid, json_response = self.scraper.make_call(
            method="GET", url=f"{API_BASE_URL}/event/{event_id}/statistics"
        )
        return request_uuid, json_response

    def get_event_ids_by_round(self, tournament_id: int, season_id: int, round_id: int):
        """_summary_

        Args:
            tournament_id (int): _description_
            season_id (int): _description_
            round_id (int): _description_

        Returns:
            _type_: _description_
        """
        request_uuid, json_response = self.scraper.make_call(
            method="GET",
            url=(
                f"{API_BASE_URL}/unique-tournament/{tournament_id}/"
                f"season/{season_id}/events/round/{round_id}"
            ),
        )
        event_ids = [
            json_response["events"][i]["id"]
            for i in range(len(json_response["events"]))
        ]
        return request_uuid, event_ids

    def get_events_by_round(self, tournament_id: int, season_id: int, round_id: int):
        """_summary_

        Args:
            tournament_id (int): _description_
            season_id (int): _description_
            round_id (int): _description_

        Returns:
            _type_: _description_
        """
        request_uuid, json_response = self.scraper.make_call(
            method="GET",
            url=(
                f"{API_BASE_URL}/unique-tournament/{tournament_id}"
                f"/season/{season_id}/events/round/{round_id}"
            ),
        )
        return request_uuid, json_response

    def get_season_ids_by_team(self, team_id: int, league_name: str = None):
        """_summary_

        Args:
            team_id (int): _description_
            league_name (str, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        request_uuid, json_response = self.scraper.make_call(
            method="GET",
            url=f"{API_BASE_URL}/team/{team_id}/team-statistics/seasons",
        )
        season_ids = []
        for tournament in json_response["uniqueTournamentSeasons"]:
            for season in tournament["seasons"]:
                if league_name is not None:
                    if league_name.upper() in season["name"].upper():
                        season_ids.append(season.get("id"))
                else:
                    season_ids.append(season.get("id"))
        return request_uuid, season_ids

    def get_last_round_of_season(
        self, team_id: int, tournament_id: int, season_id: int
    ):
        """_summary_

        Args:
            team_id (int): _description_
            tournament_id (int): _description_
            season_id (int): _description_

        Returns:
            _type_: _description_
        """
        request_uuid, json_response = self.scraper.make_call(
            method="GET",
            url=(
                f"{API_BASE_URL}/team/{team_id}/unique-tournament/{tournament_id}"
                f"/season/{season_id}/statistics/overall"
            ),
        )
        return request_uuid, json_response["statistics"]["matches"]

    def get_season_info(self, tournament_id: int, season_id: int):
        """_summary_

        Args:
            tournament_id (int): _description_
            season_id (int): _description_

        Returns:
            _type_: _description_
        """
        request_uuid, json_response = self.scraper.make_call(
            method="GET",
            url=f"{API_BASE_URL}/unique-tournament/{tournament_id}/season/{season_id}/info",
        )
        return request_uuid, json_response

    def load_round_statistics(
        self, tournament_id: int, season_id: int, round_id: int = None
    ):
        """_summary_

        Args:
            tournament_id (int): _description_
            season_id (int): _description_
            round_id (int, optional): _description_. Defaults to None.
        """
        team_id = REFERENCE_TEAMS[str(tournament_id)]
        if round_id is None:
            request_uuid, round_id = self.get_last_round_of_season(
                team_id=team_id, tournament_id=tournament_id, season_id=season_id
            )
        request_uuid, event_ids = self.get_event_ids_by_round(
            tournament_id=tournament_id, season_id=season_id, round_id=round_id
        )
        for event_id in event_ids:
            request_uuid, event_stats = self.get_event_statistics(event_id)
            metadata = {
                "request_uuid": request_uuid,
                "tournament_id": tournament_id,
                "season_id": season_id,
                "round": round_id,
                "ingestion_time": str(datetime.now()),
            }
            self.data_writter.write_json(
                json_content=event_stats,
                directory="events_stats",
                request_uuid=request_uuid,
                metadata=metadata,
            )
