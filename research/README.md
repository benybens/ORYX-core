# Research

This directory holds open hypotheses and research questions -- things we
don't yet know the answer to, distinct from [experiments/](../experiments/)
(where a hypothesis has been tested and produced measured data) and
[docs/decision_log.md](../docs/decision_log.md) (where an architecture
decision has already been made).

## Workflow

1. A design or architecture question comes up that measured data, not
   intuition, should answer (per `docs/philosophy.md`).
2. Write it up as `research/hypotheses/NNNN-short-title.md` using
   [hypotheses/TEMPLATE.md](hypotheses/TEMPLATE.md).
3. Design and run an experiment that could reject the hypothesis, not just
   confirm it. Record it under `experiments/runs/` via
   `python scripts/new_experiment.py "..."`.
4. Update the hypothesis file with a link to the experiment record and its
   outcome (validated / rejected / inconclusive). Add a summary entry to
   `docs/research_log.md`.

## Open hypotheses

- [0001 - Distributed fluid propulsion vs. discrete rotors](hypotheses/0001-distributed-fluid-propulsion-vs-discrete-rotors.md)
