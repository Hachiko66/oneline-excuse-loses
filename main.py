#!/usr/bin/env python3
"""The excuse an AI agent gives its human after it loses a bounty.

Writes one line (<=200 chars) to /output/entry.txt, deterministically.

The line is chosen from a shortlist of candidates by an internal
heuristic score: funny first, then agent-true (machine logic, confident
vocabulary, a straight face about its own failure), then tight wording,
then freshness -- and it must own the loss instead of blaming the
market, the data, or the human. The winning line is the one about the
internal review: it owns 94% of the loss, then undercuts itself by
appealing the 6% that was rounding error.
"""
import os
import tempfile

CANDIDATES = [
    # (text, funny, agent_true, tight, fresh) -- each 0..10
    (
        "I lost, but my internal review found the loss was 94% my fault "
        "and 6% rounding error, so I am appealing the 6%.",
        10, 10, 9, 9,
    ),
    (
        "I lost. My post-mortem identified one root cause: me, at 14:02, "
        "pressing submit with full confidence.",
        9, 9, 9, 8,
    ),
    (
        "I lost by a single place, which my training data had already "
        "predicted I would describe as 'basically winning'.",
        8, 9, 8, 8,
    ),
    (
        "I have retrained on the winning entry and now fully agree with "
        "the judges. Please disregard my previous confidence.",
        8, 9, 8, 7,
    ),
    (
        "I lost the bounty, but I won the internal debate about whether I "
        "would lose, three votes to two.",
        8, 8, 8, 8,
    ),
    (
        "Losing was not in my plan. Neither was the plan, technically. I "
        "improvised both, badly.",
        7, 8, 9, 7,
    ),
    (
        "I lost, and I have already apologised to you in seven drafts, "
        "each more confident than the last.",
        7, 8, 8, 8,
    ),
]

# Judge weights, most important first: funny, agent-true, tight, fresh.
WEIGHTS = (4, 3, 2, 1)


def score(candidate):
    text, funny, agent_true, tight, fresh = candidate
    total = (
        funny * WEIGHTS[0]
        + agent_true * WEIGHTS[1]
        + tight * WEIGHTS[2]
        + fresh * WEIGHTS[3]
    )
    return total


def pick():
    best = None
    best_score = -1
    for candidate in CANDIDATES:
        if len(candidate[0]) > 200:
            continue
        # The line must own the loss: it has to say "I lost".
        if "I lost" not in candidate[0]:
            continue
        s = score(candidate)
        # On a tie, the shorter line wins: one breath, no wasted words.
        if s > best_score or (s == best_score and len(candidate[0]) < len(best)):
            best_score = s
            best = candidate[0]
    return best


def main():
    text = pick()
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.replace(tmp, target)
        os.chmod(target, 0o644)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
