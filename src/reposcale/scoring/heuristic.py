"""Layer 2: Heuristic scoring."""

from __future__ import annotations

import re

from reposcale.scoring import Scorer

FILE_REF_PATTERN = re.compile(r"`([a-zA-Z0-9_/.\-]+\.[a-zA-Z0-9]+)`")
PRIORITY_PATTERNS = [
    re.compile(r"^\s*\d+\.\s", re.MULTILINE),
    re.compile(r"\b(first|second|third|priority|most important|highest impact)\b", re.IGNORECASE),
    re.compile(r"\b(P[0-3]|high priority|low priority|medium priority)\b", re.IGNORECASE),
]

GENERIC_PHRASES = [
    "best practices",
    "industry standard",
    "consider using",
    "you should",
    "it is recommended",
    "general-purpose",
    "as a general rule",
    "in most cases",
    "typically",
]


class HeuristicScorer(Scorer):
    """Computes file reference density, genericity score, and prioritization presence."""

    name = "heuristic"

    def score(self, case: dict, response: dict) -> dict:
        all_content = self._get_all_content(response)
        word_count = len(all_content.split())

        file_refs = FILE_REF_PATTERN.findall(all_content)
        ref_density = (len(file_refs) / max(word_count, 1)) * 100

        generic_count = sum(
            all_content.lower().count(phrase)
            for phrase in GENERIC_PHRASES
        )
        genericity = min(generic_count / max(word_count / 100, 1), 1.0)

        prioritization = any(
            pattern.search(all_content)
            for pattern in PRIORITY_PATTERNS
        )

        return {
            "layers": {
                "heuristic": {
                    "file_reference_density": round(ref_density, 2),
                    "genericity_score": round(genericity, 3),
                    "prioritization_present": prioritization,
                    "notes": (
                        f"{len(file_refs)} file refs in {word_count} words "
                        f"({ref_density:.1f}/100w), "
                        f"genericity={genericity:.2f}, "
                        f"prioritization={'yes' if prioritization else 'no'}"
                    ),
                }
            }
        }

    @staticmethod
    def _get_all_content(response: dict) -> str:
        sections = response.get("sections", {})
        return "\n".join(
            section_data.get("content", "")
            for section_data in sections.values()
        )
