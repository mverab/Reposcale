"""Layer 1: Structural validation scorer."""

from __future__ import annotations

from reposcale.scoring import Scorer


class StructuralScorer(Scorer):
    """Checks format compliance: sections present, evidence tags, hypothesis markers."""

    name = "structural"

    def score(self, case: dict, response: dict) -> dict:
        sections = response.get("sections", {})
        expected = case.get("expected_sections", [])

        present_keys = set(sections.keys())
        expected_normalized = {self._normalize(s) for s in expected}
        matched = present_keys & expected_normalized
        sections_complete = expected_normalized.issubset(present_keys)

        has_evidence = any(
            "evidence" in section_data and len(section_data["evidence"]) > 0
            for section_data in sections.values()
        )

        has_hypothesis = any(
            "[hypothesis]" in section_data.get("content", "").lower()
            for section_data in sections.values()
        )

        missing = expected_normalized - present_keys
        notes_parts = []
        if missing:
            notes_parts.append(f"Missing sections: {', '.join(sorted(missing))}")
        if not has_evidence:
            notes_parts.append("No evidence tags found in any section")

        return {
            "layers": {
                "structural": {
                    "format_valid": len(sections) > 0,
                    "sections_complete": sections_complete,
                    "evidence_marked": has_evidence,
                    "notes": "; ".join(notes_parts) if notes_parts else "All structural checks passed",
                }
            }
        }

    @staticmethod
    def _normalize(name: str) -> str:
        import re
        key = name.lower()
        key = re.sub(r"[^a-z0-9\s_]", "", key)
        key = re.sub(r"\s+", "_", key.strip())
        return key
