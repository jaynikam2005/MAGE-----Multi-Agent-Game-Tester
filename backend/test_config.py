import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.core.architecture import TestCase
import asyncio
from typing import List
import json
from datetime import datetime

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def sample_test_cases() -> List[TestCase]:
    return [
        TestCase(
            name="Basic Navigation Test",
            steps=[
                {"action": "navigate", "url": "https://play.ezygamers.com/"},
                {"action": "wait", "selector": "#game-container"}
            ],
            priority=1,
            complexity=0.3,
            estimated_duration=60,
            tags=["navigation", "basic"]
        ),
        TestCase(
            name="Game Interaction Test",
            steps=[
                {"action": "navigate", "url": "https://play.ezygamers.com/"},
                {"action": "wait", "selector": "#game-container"},
                {"action": "click", "selector": "#start-button"}
            ],
            priority=2,
            complexity=0.5,
            estimated_duration=120,
            tags=["gameplay", "interaction"]
        )
    ]

@pytest.fixture
def mock_execution_result():
    return {
        "test_case_id": "test123",
        "success": True,
        "execution_time": 45.5,
        "artifacts": {
            "screenshot_1": "base64_encoded_image",
            "console_logs": "[]"
        }
    }

@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()