"""Layer 3: LLM judge scoring."""

from __future__ import annotations

import json
import logging

import litellm
import yaml

from reposcale.config import PROMPTS_DIR
from reposcale.scoring import Scorer

logger = logging.getLogger(__name__)

PRIMARY_DIMENSIONS = [
    "project_understanding",
    "evidence_grounding",
    "intent_reconstruction",
    "gap_detection",
    "useful_creativity",
    "prioritization",
    "architectural_coherence",
    "actionability",
]


class LLMJudgeScorer(Scorer):
    """Invokes an LLM judge to evaluate the response using the judge rubric."""

    name = "llm_judge"

    def __init__(self, judge_model: str = "gpt-4o"):
        self.judge_model = judge_model

    def score(self, case: dict, response: dict) -> dict:
        try:
            judge_prompt = self._build_judge_prompt(case, response)
            raw_result = self._invoke_judge(judge_prompt)
            parsed = self._parse_judge_output(raw_result)
            return {"layers": {"llm_judge": parsed}}
        except Exception as e:
            logger.error(f"LLM judge scoring failed: {e}")
            return {
                "layers": {
                    "llm_judge": {
                        "judge_model": self.judge_model,
                        "overall_score": 0.0,
                        "rationale": f"Judge invocation failed: {e}",
                        "dimension_scores": {},
                    }
                }
            }

    def _build_judge_prompt(self, case: dict, response: dict) -> str:
        judge_template = (PROMPTS_DIR / "judge.md").read_text()

        case_clean = {k: v for k, v in case.items() if not k.startswith("_")}
        hints = case_clean.pop("hints", {})
        case_context = yaml.dump(case_clean, default_flow_style=False)

        response_text = ""
        for key, section_data in response.get("sections", {}).items():
            response_text += f"\n## {key}\n{section_data.get('content', '')}\n"

        hints_text = yaml.dump(hints, default_flow_style=False) if hints else "No hints available."

        repo_summary = self._build_repo_summary(case)

        return (
            f"{judge_template}\n\n---\n\n"
            f"## Case metadata\n```yaml\n{case_context}```\n\n"
            f"## Repository context\n{repo_summary}\n\n"
            f"## Model response\n{response_text}\n\n"
            f"## Evaluation hints\n```yaml\n{hints_text}```\n\n"
            f"Please provide your evaluation as a JSON object following the output format in the rubric."
        )

    MAX_REPO_FILES = 20
    MAX_REPO_BYTES = 32_000

    @staticmethod
    def _build_repo_summary(case: dict) -> str:
        from pathlib import Path as P
        case_dir = case.get("_case_dir")
        if not case_dir:
            return "Repository context not available."

        case_path = P(case_dir)
        parts = []
        budget = LLMJudgeScorer.MAX_REPO_BYTES

        tree_file = case_path / "tree.txt"
        if tree_file.exists():
            tree_text = tree_file.read_text().strip()
            parts.append(f"### File tree\n```\n{tree_text}\n```")
            budget -= len(tree_text)

        repo_dir = case_path / "repo"
        if repo_dir.is_dir():
            files_added = 0
            for f in sorted(repo_dir.rglob("*")):
                if files_added >= LLMJudgeScorer.MAX_REPO_FILES or budget <= 0:
                    break
                if not f.is_file() or f.stat().st_size > 8192:
                    continue
                rel = f.relative_to(repo_dir)
                try:
                    content = f.read_text()
                except UnicodeDecodeError:
                    continue
                chunk = f"### {rel}\n```\n{content.strip()}\n```"
                if len(chunk) > budget:
                    break
                parts.append(chunk)
                budget -= len(chunk)
                files_added += 1

        return "\n\n".join(parts) if parts else "Repository context not available."

    def _invoke_judge(self, prompt: str) -> str:
        result = litellm.completion(
            model=self.judge_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        return result.choices[0].message.content

    def _parse_judge_output(self, raw: str) -> dict:
        json_match = raw
        if "```json" in raw:
            start = raw.index("```json") + 7
            end = raw.index("```", start)
            json_match = raw[start:end]
        elif "```" in raw:
            start = raw.index("```") + 3
            end = raw.index("```", start)
            json_match = raw[start:end]

        try:
            data = json.loads(json_match.strip())
        except json.JSONDecodeError:
            return {
                "judge_model": self.judge_model,
                "overall_score": 0.0,
                "rationale": "Failed to parse judge output as JSON",
                "dimension_scores": {},
            }

        dimension_scores = {}
        raw_scores = data.get("dimension_scores", {})
        for dim in PRIMARY_DIMENSIONS:
            if dim in raw_scores:
                dimension_scores[dim] = float(raw_scores[dim])

        return {
            "judge_model": self.judge_model,
            "overall_score": float(data.get("overall_score", 0.0)),
            "rationale": data.get("rationale", ""),
            "dimension_scores": dimension_scores,
            "hallucinations": data.get("hallucinations", []),
            "strengths": data.get("strengths", []),
            "weaknesses": data.get("weaknesses", []),
        }
