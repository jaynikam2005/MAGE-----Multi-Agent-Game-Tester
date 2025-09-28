"""Tests for cross-agent validation system"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from typing import Dict, Any

from src.agents.validators.cross_agent import (
    CrossAgentValidator,
    ValidationConfig,
    ValidationStrategy,
    ValidationResult
)
from src.agents.models.test_report import VerdictStatus


class MockAgent:
    """Mock agent for testing"""
    def __init__(self, agent_id: str, verdict: VerdictStatus, confidence: float = 1.0):
        self.agent_id = agent_id
        self.verdict = verdict
        self.confidence = confidence
        self.validate_result = AsyncMock(return_value={
            "validator_id": agent_id,
            "verdict": verdict,
            "confidence": confidence
        })


@pytest.fixture
def validator():
    """Create a validator instance for testing"""
    config = ValidationConfig(
        min_validators=2,
        consensus_threshold=0.7,
        timeout_seconds=5,
        retry_count=1,
        strategy=ValidationStrategy.CONSENSUS
    )
    return CrossAgentValidator(config)


@pytest.fixture
def test_result():
    """Sample test result for validation"""
    return {
        "test_id": "test_001",
        "result": "success",
        "metrics": {"duration": 1.5}
    }


@pytest.mark.asyncio
async def test_consensus_validation_full_agreement(validator, test_result):
    """Test consensus validation with full agreement"""
    agents = [
        MockAgent("agent1", VerdictStatus.PASS),
        MockAgent("agent2", VerdictStatus.PASS),
        MockAgent("agent3", VerdictStatus.PASS)
    ]

    result = await validator.validate_test_result(test_result, agents)
    
    assert result.agreement_score == 1.0
    assert len(result.discrepancies) == 0
    assert len(result.validated_by) == 3


@pytest.mark.asyncio
async def test_consensus_validation_partial_agreement(validator, test_result):
    """Test consensus validation with partial agreement"""
    agents = [
        MockAgent("agent1", VerdictStatus.PASS),
        MockAgent("agent2", VerdictStatus.PASS),
        MockAgent("agent3", VerdictStatus.FAIL)
    ]

    result = await validator.validate_test_result(test_result, agents)
    
    assert result.agreement_score == 2/3
    assert len(result.discrepancies) == 1
    assert len(result.validated_by) == 3


@pytest.mark.asyncio
async def test_weighted_vote_validation(validator, test_result):
    """Test weighted voting validation"""
    validator.config.strategy = ValidationStrategy.WEIGHTED_VOTE
    agents = [
        MockAgent("agent1", VerdictStatus.PASS, confidence=0.9),
        MockAgent("agent2", VerdictStatus.PASS, confidence=0.8),
        MockAgent("agent3", VerdictStatus.FAIL, confidence=0.5)
    ]

    result = await validator.validate_test_result(test_result, agents)
    
    assert result.agreement_score > 0.7
    assert len(result.validated_by) == 3


@pytest.mark.asyncio
async def test_sequential_validation(validator, test_result):
    """Test sequential validation"""
    validator.config.strategy = ValidationStrategy.SEQUENTIAL
    agents = [
        MockAgent("agent1", VerdictStatus.PASS),
        MockAgent("agent2", VerdictStatus.PASS),
        MockAgent("agent3", VerdictStatus.FAIL)
    ]

    result = await validator.validate_test_result(test_result, agents)
    
    assert result.agreement_score < 1.0
    assert "Sequential validation stopped" in result.recommendations[0]


@pytest.mark.asyncio
async def test_parallel_validation(validator, test_result):
    """Test parallel validation"""
    validator.config.strategy = ValidationStrategy.PARALLEL
    agents = [
        MockAgent("agent1", VerdictStatus.PASS),
        MockAgent("agent2", VerdictStatus.PASS),
        MockAgent("agent3", VerdictStatus.PASS)
    ]

    result = await validator.validate_test_result(test_result, agents)
    
    assert result.agreement_score == 1.0
    assert "Parallel validation completed" in result.recommendations[0]


@pytest.mark.asyncio
async def test_validation_with_insufficient_validators(validator, test_result):
    """Test validation with insufficient validators"""
    agents = [MockAgent("agent1", VerdictStatus.PASS)]

    with pytest.raises(ValueError, match="Need at least 2 validators"):
        await validator.validate_test_result(test_result, agents)


@pytest.mark.asyncio
async def test_validation_with_failing_agents(validator, test_result):
    """Test validation when some agents fail"""
    failing_agent = MockAgent("agent1", VerdictStatus.PASS)
    failing_agent.validate_result = AsyncMock(side_effect=Exception("Validation failed"))
    
    agents = [
        failing_agent,
        MockAgent("agent2", VerdictStatus.PASS),
        MockAgent("agent3", VerdictStatus.PASS)
    ]

    result = await validator.validate_test_result(test_result, agents)
    
    assert result.agreement_score == 1.0
    assert len(result.validated_by) == 2


@pytest.mark.asyncio
async def test_validation_with_timeout(validator, test_result):
    """Test validation with timeout"""
    validator.config.strategy = ValidationStrategy.PARALLEL
    validator.config.timeout_seconds = 0.1
    
    slow_agent = MockAgent("agent1", VerdictStatus.PASS)
    slow_agent.validate_result = AsyncMock(side_effect=asyncio.sleep(1))
    
    agents = [
        slow_agent,
        MockAgent("agent2", VerdictStatus.PASS),
        MockAgent("agent3", VerdictStatus.PASS)
    ]

    result = await validator.validate_test_result(test_result, agents)
    
    assert result.agreement_score == 1.0
    assert len(result.validated_by) == 3