# Runtime Contract Goldens

`runtime-contract-golden.json` stores a curated governed-runtime baseline for public runtime artifacts.

Rules:

- it validates a stable semantic subset, not full JSON parity
- dynamic values must be normalized before comparison
- packet and manifest goldens are allowed to evolve only through governed runtime contract changes
