"""Parse raw LLM text responses into structured RepoScale response format."""

from __future__ import annotations

import re
from datetime import datetime, timezone


EVIDENCE_PATTERN = re.compile(r"\[evidence(?::\s*([^\]]+))?\]", re.IGNORECASE)
HYPOTHESIS_PATTERN = re.compile(r"\[hypothesis\]", re.IGNORECASE)
HEADING_PATTERN = re.compile(r"^#{1,3}\s+\d*\.?\s*(.+)$", re.MULTILINE)
FILE_REF_PATTERN = re.compile(r"`([a-zA-Z0-9_/.\-]+\.[a-zA-Z0-9]+)`")


def _extract_sections(raw_text: str) -> dict[str, str]:
    headings = list(HEADING_PATTERN.finditer(raw_text))

    if not headings:
        return {"raw_output": raw_text}

    sections = {}
    for i, match in enumerate(headings):
        title = match.group(1).strip()
        key = _normalize_section_key(title)
        start = match.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(raw_text)
        sections[key] = raw_text[start:end].strip()

    return sections


def _normalize_section_key(title: str) -> str:
    key = title.lower()
    key = re.sub(r"[^a-z0-9\s]", "", key)
    key = re.sub(r"\s+", "_", key.strip())
    return key


def _extract_evidence(text: str) -> list[dict]:
    evidence = []
    for match in EVIDENCE_PATTERN.finditer(text):
        ref = match.group(1) or ""
        entry = {"type": "file", "ref": ref.strip()}

        if ref.startswith(("http://", "https://")):
            entry["type"] = "other"
        elif re.match(r"[a-f0-9]{7,40}", ref):
            entry["type"] = "commit"
        elif ref.endswith((".md", ".txt", ".rst")):
            entry["type"] = "doc"
        elif "test" in ref.lower():
            entry["type"] = "test"

        evidence.append(entry)

    for match in FILE_REF_PATTERN.finditer(text):
        ref = match.group(1)
        if not any(e["ref"] == ref for e in evidence):
            evidence.append({"type": "file", "ref": ref})

    return evidence


def parse_response(
    raw_text: str,
    case_data: dict,
    model: str,
    mode: str = "prompt_only",
) -> dict:
    sections_raw = _extract_sections(raw_text)

    sections = {}
    for key, content in sections_raw.items():
        section_entry = {"content": content}
        evidence = _extract_evidence(content)
        if evidence:
            section_entry["evidence"] = evidence
        sections[key] = section_entry

    response_data = {
        "case_id": case_data["id"],
        "track": case_data["track"],
        "mode": mode,
        "model": {"name": model},
        "sections": sections,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    return response_data
