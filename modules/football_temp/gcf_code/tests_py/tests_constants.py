import sys
import os

sys.path.append(os.path.abspath("../src"))
from utils.constants import (
    GCS_BUCKET, 
    PROJECT_ENV,
    POSSIBLE_BROWSERS,
    POSSIBLE_USER_AGENTS, 
    TIMEOUT,
    REFERENCE_TEAMS,
    API_BASE_URL,
)


class TestClassConstants:
    def test_gcs_bucket(self):
        assert GCS_BUCKET.startswith("football_data_collection_")

    def test_project_env(self):
        assert PROJECT_ENV in ["dev", "prd"]
        
    def test_possible_browsers(self):
        assert isinstance(POSSIBLE_BROWSERS, list)
        assert len(POSSIBLE_BROWSERS) >= 5
        
        for browser in POSSIBLE_BROWSERS:
            assert isinstance(browser, str)
            assert browser.startswith("chrome")
            assert len(browser) in [8,9]

    def test_possible_user_agents(self):
        assert isinstance(POSSIBLE_USER_AGENTS, list)
        assert len(POSSIBLE_USER_AGENTS) >= 5
        
        for agent in POSSIBLE_USER_AGENTS:
            assert isinstance(agent, str)
            assert agent.startswith("Mozilla/5.0")
    
    def test_reference_teams(self):
        assert isinstance(REFERENCE_TEAMS, dict)
        assert len(REFERENCE_TEAMS) >= 2
        assert "8" in REFERENCE_TEAMS
        assert "17" in REFERENCE_TEAMS
    
    def test_api_base_url(self):
        assert API_BASE_URL == "https://www.sofascore.com/api/v1"

    def test_timeout(self):
        assert isinstance(TIMEOUT, int)
        assert TIMEOUT >= 10