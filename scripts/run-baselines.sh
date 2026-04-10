#!/bin/bash
# Run multi-provider baselines for RepoScale alpha corpus.
# Requires: OPENAI_API_KEY and ANTHROPIC_API_KEY in environment.
set -euo pipefail

echo "=== RepoScale Alpha Baselines ==="
echo ""

# Check API keys
if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "ERROR: OPENAI_API_KEY not set"
  exit 1
fi

if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "WARNING: ANTHROPIC_API_KEY not set — skipping Claude baselines"
  SKIP_CLAUDE=1
else
  SKIP_CLAUDE=0
fi

# --- GPT-4o baseline ---
echo ">>> Running GPT-4o baseline..."
reposcale batch cases/ --model gpt-4o
GPT4O_RUN=$(ls -td results/*gpt4o* | head -1)
echo ">>> Scoring GPT-4o with judge (repeat=3 for stability)..."
reposcale score "$GPT4O_RUN" --judge-model gpt-4o --repeat 3
echo ">>> GPT-4o summary:"
reposcale summary "$GPT4O_RUN"

# --- Claude baseline ---
if [ "$SKIP_CLAUDE" -eq 0 ]; then
  echo ""
  echo ">>> Running Claude 3.5 Sonnet baseline..."
  reposcale batch cases/ --model claude-3-5-sonnet-20241022
  CLAUDE_RUN=$(ls -td results/*claude* | head -1)
  echo ">>> Scoring Claude with judge (repeat=3 for stability)..."
  reposcale score "$CLAUDE_RUN" --judge-model gpt-4o --repeat 3
  echo ">>> Claude summary:"
  reposcale summary "$CLAUDE_RUN"

  echo ""
  echo ">>> Comparing runs..."
  reposcale compare "$GPT4O_RUN" "$CLAUDE_RUN"
fi

echo ""
echo "=== Done ==="
