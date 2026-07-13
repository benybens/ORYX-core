# Assets

Static reference assets: exported CAD models (STEP/STL) worth keeping in
version control, reference images, diagrams source files, etc.

Generated CAD output from `scripts/generate_cad.py` lands in
`cad/output/` (gitignored, reproducible on demand). Only promote a
specific generated artifact here if it needs to be preserved as a
reference point (e.g. "the hull design used in experiment X") -- link to
the corresponding `experiments/runs/` record when you do.
