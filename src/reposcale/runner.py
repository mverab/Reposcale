"""Eval runner for prompt_only mode."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import litellm
import yaml

from reposcale.config import PROMPTS_DIR, RESULTS_DIR


def _should_include_repo_path(path: Path) -> bool:
    parts = path.parts
    if any(part.startswith(".") for part in parts):
        return False
    if "__pycache__" in parts:
        return False
    if path.suffix in {".pyc", ".pyo"}:
        return False
    return True


def load_case(case_dir: Path) -> dict:
    case_file = case_dir / "case.yaml"
    if not case_file.exists():
        raise FileNotFoundError(f"No case.yaml found in {case_dir}")
    with open(case_file) as f:
        return yaml.safe_load(f)


def load_prompt_template(track: str) -> str:
    prompt_file = PROMPTS_DIR / f"{track}.md"
    if not prompt_file.exists():
        raise FileNotFoundError(f"No prompt template for track '{track}'")
    return prompt_file.read_text()


def build_file_tree(repo_dir: Path) -> str:
    if not repo_dir.exists():
        return "(no repo snapshot available)"

    lines = []
    for item in sorted(repo_dir.rglob("*")):
        rel = item.relative_to(repo_dir)
        if not _should_include_repo_path(rel):
            continue
        indent = "  " * (len(rel.parts) - 1)
        prefix = "├── " if item.is_file() else "└── "
        lines.append(f"{indent}{prefix}{item.name}")

    return "\n".join(lines) if lines else "(empty repo snapshot)"


def _read_repo_file_contents(repo_dir: Path, max_files: int = 30) -> str:
    if not repo_dir.exists():
        return ""

    blocks = []
    count = 0
    for item in sorted(repo_dir.rglob("*")):
        if not item.is_file():
            continue
        rel = item.relative_to(repo_dir)
        if not _should_include_repo_path(rel):
            continue
        try:
            content = item.read_text(errors="replace")
        except Exception:
            continue
        blocks.append(f"### {rel}\n```\n{content}\n```")
        count += 1
        if count >= max_files:
            blocks.append(f"(... truncated, {max_files} files shown)")
            break

    return "\n\n".join(blocks)


def assemble_prompt(case_data: dict, case_dir: Path) -> str:
    track = case_data["track"]
    template = load_prompt_template(track)

    repo_dir = case_dir / "repo"
    file_tree = build_file_tree(repo_dir)

    context = f"""## Case: {case_data['title']}

**Description**: {case_data['description']}
**Track**: {track}
**Case type**: {case_data['case_type']}
**Difficulty**: {case_data['difficulty']}

### File tree
```
{file_tree}
```
"""

    # Include file contents for prompt_only mode
    file_contents = _read_repo_file_contents(repo_dir)
    if file_contents:
        context += f"\n## Repository files\n\n{file_contents}\n"

    # Load additional docs if present
    docs_dir = case_dir / "docs"
    if docs_dir.exists():
        for doc_file in sorted(docs_dir.glob("*")):
            content = doc_file.read_text()
            context += f"\n### {doc_file.name}\n```\n{content}\n```\n"

    # Load history if present
    history_file = case_dir / "history.json"
    if history_file.exists():
        with open(history_file) as f:
            history = json.load(f)
        context += f"\n### Commit history (last {len(history)} commits)\n"
        for commit in history[:20]:
            context += f"- `{commit.get('hash', '?')[:7]}` {commit.get('message', '')}\n"

    return f"{template}\n\n---\n\n{context}"


def generate_run_id(model: str) -> str:
    now = datetime.now(timezone.utc)
    model_short = re.sub(r"[^a-z0-9]", "", model.lower())[:12]
    return f"{now.strftime('%Y%m%d-%H%M%S')}-{model_short}"


def invoke_model(prompt: str, model: str) -> str:
    response = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content


def persist_response(response_data: dict, run_id: str, case_id: str) -> Path:
    out_dir = RESULTS_DIR / run_id / case_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "response.json"
    with open(out_path, "w") as f:
        json.dump(response_data, f, indent=2)
    return out_path


def run_single(
    case_dir: Path,
    model: str,
    run_id: str,
    dry_run: bool = False,
) -> dict | str:
    case_data = load_case(case_dir)
    prompt = assemble_prompt(case_data, case_dir)

    if dry_run:
        return prompt

    raw_response = invoke_model(prompt, model)

    from reposcale.parser import parse_response
    response_data = parse_response(
        raw_text=raw_response,
        case_data=case_data,
        model=model,
    )

    persist_response(response_data, run_id, case_data["id"])
    return response_data


def run_batch(
    track_dir: Path,
    model: str,
    run_id: str | None = None,
    dry_run: bool = False,
) -> list[dict | str]:
    if run_id is None:
        run_id = generate_run_id(model)

    case_dirs = sorted(
        d for d in track_dir.iterdir()
        if d.is_dir() and (d / "case.yaml").exists()
    )

    results = []
    for case_dir in case_dirs:
        result = run_single(case_dir, model, run_id, dry_run)
        results.append(result)

    return results
