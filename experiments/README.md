# Experiments

Every experiment -- simulated or physical -- gets its own dated directory
under `experiments/runs/`, seeded from `experiments/template/RECORD.md`:

```bash
python scripts/new_experiment.py "short experiment title"
```

## Why this exists

Per `docs/philosophy.md`, ORYX treats this repository as an engineering
notebook: a claim about the vehicle's performance isn't established until
there's an `experiments/runs/<date>-<slug>/RECORD.md` behind it with a
stated hypothesis, method, measured data, and conclusion -- including when
the conclusion is "hypothesis rejected." Experiment data is committed to
the repository, not gitignored -- it's the primary artifact this project
produces.

## Directory layout

```
experiments/
  template/
    RECORD.md           the record template
  runs/
    2026-07-13-example-sweep/
      RECORD.md
      results.csv       raw or summarized data, plots, etc.
```

## Linking back

When an experiment bears on an open question in `research/hypotheses/` or
changes the picture described in `docs/research_log.md`, update both with
a link to the new `RECORD.md`.
