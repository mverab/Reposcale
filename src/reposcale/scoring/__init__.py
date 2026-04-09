"""Scoring pipeline for RepoScale evaluations."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Scorer(ABC):
    """Base class for all scoring layers."""

    name: str = "base"

    @abstractmethod
    def score(self, case: dict, response: dict) -> dict:
        """Score a response against a case.

        Args:
            case: The case.yaml metadata.
            response: The parsed response data.

        Returns:
            A partial evaluation dict to be merged by the coordinator.
        """
        ...
