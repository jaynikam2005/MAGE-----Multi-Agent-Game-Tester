"""Cross-agent validation system for test results"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import structlog
from datetime import datetime

from ..models.test_report import ValidationResult, VerdictStatus
from src.core.config import get_settings


class ValidationStrategy(str, Enum):
    """Validation strategies for cross-agent validation"""
    CONSENSUS = "consensus"
    WEIGHTED_VOTE = "weighted_vote"
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"


@dataclass
class ValidationConfig:
    """Configuration for cross-agent validation"""
    min_validators: int = 2
    consensus_threshold: float = 0.7
    timeout_seconds: int = 300
    retry_count: int = 3
    strategy: ValidationStrategy = ValidationStrategy.CONSENSUS


class CrossAgentValidator:
    """Cross-agent validation system"""

    def __init__(self, config: Optional[ValidationConfig] = None):
        self.config = config or ValidationConfig()
        self.settings = get_settings()
        self.logger = structlog.get_logger(__name__)

    async def validate_test_result(self, 
                                 test_result: Dict[str, Any],
                                 validator_agents: List[Any]) -> ValidationResult:
        """Validate a test result using multiple agents"""
        if len(validator_agents) < self.config.min_validators:
            raise ValueError(f"Need at least {self.config.min_validators} validators")

        strategy_map = {
            ValidationStrategy.CONSENSUS: self._validate_consensus,
            ValidationStrategy.WEIGHTED_VOTE: self._validate_weighted_vote,
            ValidationStrategy.SEQUENTIAL: self._validate_sequential,
            ValidationStrategy.PARALLEL: self._validate_parallel
        }

        validator = strategy_map.get(self.config.strategy, self._validate_consensus)
        return await validator(test_result, validator_agents)

    async def _validate_consensus(self,
                                test_result: Dict[str, Any],
                                validator_agents: List[Any]) -> ValidationResult:
        """Validate using consensus strategy"""
        validations = []
        validator_ids = []

        # Get validations from all agents
        for agent in validator_agents:
            try:
                validation = await agent.validate_result(test_result)
                validations.append(validation)
                validator_ids.append(agent.agent_id)
            except Exception as e:
                self.logger.error(f"Validation failed for agent {agent.agent_id}", error=str(e))

        # Calculate agreement score
        total_validations = len(validations)
        if total_validations == 0:
            raise ValueError("No valid validations received")

        # Count verdicts
        verdict_counts = {}
        for validation in validations:
            verdict = validation.get("verdict", VerdictStatus.INCONCLUSIVE)
            verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1

        # Find majority verdict
        majority_verdict = max(verdict_counts.items(), key=lambda x: x[1])
        agreement_score = majority_verdict[1] / total_validations

        # Collect discrepancies
        discrepancies = []
        if agreement_score < 1.0:
            for validation in validations:
                if validation.get("verdict") != majority_verdict[0]:
                    discrepancies.append({
                        "validator_id": validation.get("validator_id"),
                        "verdict": validation.get("verdict"),
                        "reason": validation.get("reason", "No reason provided")
                    })

        # Generate recommendations
        recommendations = []
        if agreement_score < self.config.consensus_threshold:
            recommendations.append(
                "Low consensus among validators - manual review recommended"
            )
        if discrepancies:
            recommendations.append(
                f"Found {len(discrepancies)} discrepancies in validation results"
            )

        return ValidationResult(
            validator_id="cross_agent_validator",
            validated_by=validator_ids,
            agreement_score=agreement_score,
            discrepancies=discrepancies,
            recommendations=recommendations
        )

    async def _validate_weighted_vote(self,
                                    test_result: Dict[str, Any],
                                    validator_agents: List[Any]) -> ValidationResult:
        """Validate using weighted voting strategy"""
        weighted_votes = {}
        validator_ids = []

        for agent in validator_agents:
            try:
                validation = await agent.validate_result(test_result)
                verdict = validation.get("verdict", VerdictStatus.INCONCLUSIVE)
                confidence = validation.get("confidence", 0.5)
                
                weighted_votes[verdict] = weighted_votes.get(verdict, 0) + confidence
                validator_ids.append(agent.agent_id)
            except Exception as e:
                self.logger.error(f"Validation failed for agent {agent.agent_id}", error=str(e))

        if not weighted_votes:
            raise ValueError("No valid validations received")

        # Find verdict with highest weighted votes
        final_verdict = max(weighted_votes.items(), key=lambda x: x[1])[0]
        total_weight = sum(weighted_votes.values())
        agreement_score = weighted_votes[final_verdict] / total_weight

        return ValidationResult(
            validator_id="cross_agent_validator",
            validated_by=validator_ids,
            agreement_score=agreement_score,
            discrepancies=[],  # Weighted voting doesn't track individual discrepancies
            recommendations=[
                f"Final verdict reached with {agreement_score:.2%} weighted agreement"
            ] if agreement_score >= self.config.consensus_threshold else [
                "Low weighted agreement - consider additional validation"
            ]
        )

    async def _validate_sequential(self,
                                 test_result: Dict[str, Any],
                                 validator_agents: List[Any]) -> ValidationResult:
        """Validate using sequential strategy"""
        validations = []
        validator_ids = []
        current_verdict = None

        for agent in validator_agents:
            try:
                validation = await agent.validate_result(test_result)
                verdict = validation.get("verdict", VerdictStatus.INCONCLUSIVE)
                
                if current_verdict is None:
                    current_verdict = verdict
                elif verdict != current_verdict:
                    # Stop on first disagreement
                    validations.append(validation)
                    validator_ids.append(agent.agent_id)
                    break
                
                validations.append(validation)
                validator_ids.append(agent.agent_id)
                
            except Exception as e:
                self.logger.error(f"Validation failed for agent {agent.agent_id}", error=str(e))
                break

        if not validations:
            raise ValueError("No valid validations received")

        # Calculate agreement
        agreements = sum(1 for v in validations if v.get("verdict") == current_verdict)
        agreement_score = agreements / len(validations)

        return ValidationResult(
            validator_id="cross_agent_validator",
            validated_by=validator_ids,
            agreement_score=agreement_score,
            discrepancies=[],
            recommendations=[
                "Sequential validation completed successfully"
                if agreement_score == 1.0 else
                "Sequential validation stopped due to disagreement"
            ]
        )

    async def _validate_parallel(self,
                               test_result: Dict[str, Any],
                               validator_agents: List[Any]) -> ValidationResult:
        """Validate using parallel strategy"""
        validation_tasks = []
        validator_ids = []

        for agent in validator_agents:
            task = asyncio.create_task(agent.validate_result(test_result))
            validation_tasks.append((agent.agent_id, task))
            validator_ids.append(agent.agent_id)

        validations = []
        for agent_id, task in validation_tasks:
            try:
                validation = await asyncio.wait_for(task, timeout=self.config.timeout_seconds)
                validations.append((agent_id, validation))
            except asyncio.TimeoutError:
                self.logger.error(f"Validation timeout for agent {agent_id}")
            except Exception as e:
                self.logger.error(f"Validation failed for agent {agent_id}", error=str(e))

        if not validations:
            raise ValueError("No valid validations received")

        # Analyze results
        verdict_counts = {}
        for _, validation in validations:
            verdict = validation.get("verdict", VerdictStatus.INCONCLUSIVE)
            verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1

        majority_verdict = max(verdict_counts.items(), key=lambda x: x[1])
        agreement_score = majority_verdict[1] / len(validations)

        return ValidationResult(
            validator_id="cross_agent_validator",
            validated_by=validator_ids,
            agreement_score=agreement_score,
            discrepancies=[],
            recommendations=[
                f"Parallel validation completed with {agreement_score:.2%} agreement"
            ]
        )