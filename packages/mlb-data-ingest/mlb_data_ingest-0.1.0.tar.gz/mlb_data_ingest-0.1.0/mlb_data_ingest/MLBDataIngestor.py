import json
import requests
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Union
from pathlib import Path


REQUEST_TIMEOUT = 10  # Timeout for requests in seconds


def get_unique_team_ids(file_path: Path) -> List[Union[str, int]]:
    """
    Extract unique team IDs from a JSON file.

    Parameters:
    - file_path: The path to the JSON file.

    Returns:
    - A list of unique team IDs.
    """
    try:
        with file_path.open() as file:
            data = json.load(file)
        team_ids = {team["id"] for team in data["teams"]}
        return list(team_ids)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from file: {file_path}")
        return []


def flatten_teams_from_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Flatten the team data from a JSON file.

    Parameters:
    - file_path: The path to the JSON file.

    Returns:
    - A list of flattened team data.
    """
    if not Path(file_path).is_file():
        raise FileNotFoundError(f"No such file: '{file_path}'")

    with open(file_path) as file:
        data = json.load(file)
        teams = data["teams"]
    return [
        {
            sub_key: sub_value
            for key, value in team.items()
            for sub_key, sub_value in (value.items() if isinstance(value, dict) else [(key, value)])
        }
        for team in teams
    ]


class MLBDataIngestor:
    """
    Class to ingest MLB data from various endpoints.
    """

    DATA_DIR = Path("./data")  # Directory to store the ingested data
    ENDPOINTS = ["teams", "divisions", "conferences", "people", "team_roster"]  # API endpoints to ingest data from
    BASE_URL = "https://statsapi.mlb.com/api"
    VERSION = "v1"

    def __init__(self):
        """Initialize directories for data storage and API base URL."""
        logging.basicConfig(filename="mlb_data_ingestor.log", level=logging.DEBUG)
        for endpoint in self.ENDPOINTS:
            (self.DATA_DIR / endpoint).mkdir(parents=True, exist_ok=True)

    def call_api(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Call the API and return the data."""
        url = f"{self.BASE_URL}/{self.VERSION}/{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()  # Raise exception if invalid response
            data = response.json()
            logging.info(f"Successful request: {url}")
            return data
        except requests.exceptions.Timeout:
            logging.error(f"Request timed out for endpoint {endpoint}")
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred for endpoint {endpoint}: {e}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed for endpoint {endpoint} with error {e}")
        return None

    def write_to_file(self, data: Dict[str, Any], dir_name: str, filename: str) -> None:
        """Write data to a JSON file."""
        dir_path = Path(self.DATA_DIR, dir_name)
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / f"{filename}.json"
        with open(file_path, "w") as file:
            json.dump(data, file)

    def get_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Get data from a specific endpoint, either from file or API."""
        data = self.call_api(endpoint, params or {})
        if data is not None:
            # Replace slashes in the endpoint with underscores
            safe_endpoint = endpoint.replace("/", "_")

            self.write_to_file(data, safe_endpoint, safe_endpoint)
        return data

    def get_endpoint_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Get data from a specific endpoint.
        Parameters:
        - endpoint: The endpoint to get data from.
        - params: Optional parameters for the API call.
        """
        return self.get_data(endpoint, params)

    def get_teams(self, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Get data from the 'teams' endpoint."""
        return self.get_data("teams", params)

    def get_divisions(self, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Get data from the 'divisions' endpoint."""
        return self.get_data("divisions", params)

    def get_conferences(self, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Get data from the 'conferences' endpoint."""
        return self.get_data("conferences", params)

    def get_people(self, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Get data from the 'people' endpoint."""
        return self.get_data("people", params)

    def get_team_roster(self, team_id: int, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Get data from the 'team_roster' endpoint.
        Parameters:
        - team_id: The ID of the team to get the roster for.
        - params: Optional parameters for the API call. Can include:
        - rosterType: The type of roster to get (e.g., "active").
        - season: The season to get the roster for.
        - date: The date to get the roster for.
        - hydrate: Additional data to include in the response.
        - fields: Specific fields to include in the response.
        """
        endpoint = f"teams/{team_id}/roster"
        data = self.call_api(endpoint, params)
        if data is not None:
            self.write_to_file(data, "team_roster", f"{team_id}_roster")
        return data

    def get_all_team_rosters(self) -> None:
        """Get rosters for all teams and save them as individual JSON files."""
        teams_file_path = self.DATA_DIR / "teams" / "teams.json"
        if teams_file_path.is_file():
            team_ids = get_unique_team_ids(teams_file_path)
            for team_id in team_ids:
                roster_data = self.get_team_roster(team_id)
                if roster_data is not None:
                    self.write_to_file(roster_data, "team_roster", f"{team_id}_roster")

    def get_schedule(
        self, params: Optional[Dict[str, Any]] = None, filename: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get data from the 'schedule' endpoint.
        Parameters:
        - params: Optional parameters for the API call.
        - filename: Optional filename for the output file.
        """
        # Check if at least one of the required parameters is provided
        required_params = ["sportId", "gamePk", "gamePks"]
        if params is not None and all(param not in params for param in required_params):
            raise ValueError(f"Must provide at least one of the following parameters: {', '.join(required_params)}")

        endpoint = "schedule"
        data = self.call_api(endpoint, params)
        if data is not None and filename is not None:
            self.write_to_file(data, "schedule", filename)
        return data

    def get_relative_day_schedule(
        self, relative_days: int, filename: str, params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get schedule for a day relative to today.
        Parameters:
        - relative_days: Number of days relative to today (can be negative for past days).
        - filename: Filename for the output file.
        - params: Optional parameters for the API call.
        """
        params = params or {}
        date = (datetime.now() + timedelta(days=relative_days)).strftime("%Y-%m-%d")
        params["startDate"] = params["endDate"] = date
        return self.get_schedule(params, filename=filename)

    def get_yesterday_schedule(self, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Get yesterday's schedule.
        """
        return self.get_relative_day_schedule(-1, "yesterday_schedule", params)

    def get_tomorrow_schedule(self, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Get tomorrow's schedule.
        """
        return self.get_relative_day_schedule(1, "tomorrow_schedule", params)

    def get_today_schedule(self, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Get today's schedule.
        """
        return self.get_relative_day_schedule(0, "today_schedule", params)

    def get_season_schedule(self, year: int, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Get the schedule for an entire season.
        """
        params = params or {}
        params["startDate"] = f"{year}-03-01"  # Assuming season starts in April
        params["endDate"] = f"{year}-10-31"  # Assuming season ends in October
        return self.get_schedule(params, filename=f"{year}_season")

    def get_metadata(self, meta_type: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Get data from the 'meta' endpoint.
        Parameters:
        - meta_type: The type of metadata to retrieve.
        - params: Optional parameters for the API call.
        """
        endpoint = f"{meta_type}"
        data = self.call_api(endpoint, params)
        if data is not None:
            self.write_to_file(data, "metadata", meta_type)
        return data

    def get_all_metadata(self, params: Optional[Dict[str, Any]] = None) -> None:
        """
        Get data from the 'meta' endpoint for all meta types.
        Parameters:
        - params: Optional parameters for the API call.
        """
        meta_types = [
            "awards",
            "baseballStats",
            "eventTypes",
            "gameStatus",
            "gameTypes",
            "hitTrajectories",
            "jobTypes",
            "languages",
            "leagueLeaderTypes",
            "logicalEvents",
            "metrics",
            "pitchCodes",
            "pitchTypes",
            "platforms",
            "positions",
            "reviewReasons",
            "rosterTypes",
            "scheduleEventTypes",
            "situationCodes",
            "sky",
            "standingsTypes",
            "statGroups",
            "statTypes",
            "windDirection",
        ]

        for meta_type in meta_types:
            endpoint = f"{meta_type}"
            data = self.call_api(endpoint, params)
            if data is not None:
                self.write_to_file(data, "meta", meta_type)
