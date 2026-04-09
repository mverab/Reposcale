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

        case_context = yaml.dump(case, default_flow_style=False)

        response_text = ""
        for key, section_data in response.get("sections", {}).items():
            response_text += f"\n## {key}\n{section_data.get('content', '')}\n"

        hints_text = ""
        if "hints" in response:
            hints_text = yaml.dump(response["hints"], default_flow_style=False)

        return (
            f"{judge_template}\n\n---\n\n"
            f"## Case metadata\n```yaml\n{case_context}```\n\n"
            f"## Model response\n{response_text}\n\n"
            f"## Evaluation hints\n```yaml\n{hints_text}```\n\n"
            f"Please provide your evaluation as a JSON object following the output format in the rubric."
        )

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
        }
