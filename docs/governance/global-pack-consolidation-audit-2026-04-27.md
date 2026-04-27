# Global Pack Consolidation Audit

日期：2026-04-27

## 结论先看

本报告是只读体检，不修改 live routing，不删除 skill 目录。

- pack 总数：43
- P0：6
- P1：15
- P2：22
- 当前最高风险 pack：`docs-media`

## 全局排序

| priority | pack | score | skills | route authority | stage assistant | rationale |
|---|---|---:|---:|---:|---:|---|
| P0 | `docs-media` | 83.10 | 17 | 0 | 0 | 17 skill candidates; no explicit role split; 5 suspected overlap pairs; 18 shared broad keywords; 10 tool-like primary candidates; 11 candidates with scripts/references/assets |
| P0 | `research-design` | 75.20 | 24 | 14 | 3 | 24 skill candidates; 14 route authorities; 3 suspected overlap pairs; 7 shared broad keywords; 2 tool-like primary candidates; 15 candidates with scripts/references/assets |
| P0 | `code-quality` | 70.60 | 16 | 0 | 0 | 16 skill candidates; no explicit role split; 16 suspected overlap pairs; 7 shared broad keywords; 1 tool-like primary candidates; 3 candidates with scripts/references/assets |
| P0 | `science-literature-citations` | 70.40 | 12 | 10 | 2 | 12 skill candidates; 10 route authorities; 16 shared broad keywords; 9 tool-like primary candidates; 11 candidates with scripts/references/assets |
| P0 | `bio-science` | 70.00 | 26 | 0 | 0 | 26 skill candidates; no explicit role split; 2 shared broad keywords; 15 tool-like primary candidates; 26 candidates with scripts/references/assets |
| P0 | `science-chem-drug` | 64.90 | 13 | 0 | 0 | 13 skill candidates; no explicit role split; 12 shared broad keywords; 6 tool-like primary candidates; 13 candidates with scripts/references/assets |
| P1 | `scholarly-publishing-workflow` | 59.70 | 13 | 0 | 0 | 13 skill candidates; no explicit role split; 34 shared broad keywords; 4 tool-like primary candidates; 9 candidates with scripts/references/assets |
| P1 | `integration-devops` | 59.10 | 13 | 0 | 0 | 13 skill candidates; no explicit role split; 9 shared broad keywords; 3 tool-like primary candidates; 12 candidates with scripts/references/assets |
| P1 | `ai-llm` | 55.50 | 11 | 0 | 0 | no explicit role split; 20 shared broad keywords; 4 tool-like primary candidates; 6 candidates with scripts/references/assets |
| P1 | `science-lab-automation` | 55.10 | 7 | 0 | 0 | no explicit role split; 10 shared broad keywords; 6 tool-like primary candidates; 7 candidates with scripts/references/assets |
| P1 | `science-communication-slides` | 52.80 | 8 | 0 | 0 | no explicit role split; 10 shared broad keywords; 4 tool-like primary candidates; 6 candidates with scripts/references/assets |
| P1 | `data-ml` | 47.40 | 8 | 7 | 1 | 7 route authorities; 11 shared broad keywords; 1 tool-like primary candidates; 7 candidates with scripts/references/assets |
| P1 | `orchestration-core` | 46.80 | 27 | 1 | 26 | 27 skill candidates; 2 suspected overlap pairs; 5 shared broad keywords; 9 candidates with scripts/references/assets |
| P1 | `science-clinical-regulatory` | 44.90 | 7 | 0 | 0 | no explicit role split; 5 shared broad keywords; 5 tool-like primary candidates; 7 candidates with scripts/references/assets |
| P1 | `finance-edgar-macro` | 39.50 | 7 | 0 | 0 | no explicit role split; 2 shared broad keywords; 5 tool-like primary candidates; 7 candidates with scripts/references/assets |
| P1 | `science-medical-imaging` | 35.50 | 5 | 0 | 0 | no explicit role split; 5 shared broad keywords; 5 candidates with scripts/references/assets |
| P1 | `science-figures-visualization` | 31.30 | 5 | 2 | 3 | 11 shared broad keywords; 1 tool-like primary candidates; 4 candidates with scripts/references/assets |
| P1 | `science-reporting` | 31.30 | 5 | 2 | 3 | 10 shared broad keywords; 1 tool-like primary candidates; 4 candidates with scripts/references/assets |
| P1 | `ruc-nlpir-augmentation` | 27.60 | 4 | 2 | 2 | 14 shared broad keywords; 2 candidates with scripts/references/assets |
| P1 | `aios-core` | 25.40 | 12 | 1 | 11 | 12 skill candidates; 1 suspected overlap pairs; 5 shared broad keywords; 1 tool-like primary candidates |
| P1 | `science-quantum` | 19.40 | 4 | 0 | 0 | 5 shared broad keywords; 3 tool-like primary candidates; 4 candidates with scripts/references/assets |
| P2 | `science-geospatial` | 12.90 | 3 | 0 | 0 | 3 shared broad keywords; 2 tool-like primary candidates; 3 candidates with scripts/references/assets |
| P2 | `science-zarr-polars` | 12.60 | 4 | 0 | 0 | 3 shared broad keywords; 1 tool-like primary candidates; 3 candidates with scripts/references/assets |
| P2 | `ml-torch-geometric` | 12.00 | 2 | 0 | 0 | 1 suspected overlap pairs; 4 shared broad keywords; 1 candidates with scripts/references/assets |
| P2 | `science-peer-review` | 8.70 | 3 | 0 | 0 | 3 tool-like primary candidates; 3 candidates with scripts/references/assets |
| P2 | `web-scraping` | 4.60 | 2 | 0 | 0 | 1 tool-like primary candidates; 2 candidates with scripts/references/assets |
| P2 | `docs-markitdown-conversion` | 2.90 | 1 | 0 | 0 | 1 tool-like primary candidates; 1 candidates with scripts/references/assets |
| P2 | `ip-uspto-patents` | 2.90 | 1 | 0 | 0 | 1 tool-like primary candidates; 1 candidates with scripts/references/assets |
| P2 | `media-video` | 2.90 | 1 | 0 | 0 | 1 tool-like primary candidates; 1 candidates with scripts/references/assets |
| P2 | `ml-stable-baselines3` | 2.90 | 1 | 0 | 0 | 1 tool-like primary candidates; 1 candidates with scripts/references/assets |
| P2 | `science-fluidsim-cfd` | 2.90 | 1 | 0 | 0 | 1 tool-like primary candidates; 1 candidates with scripts/references/assets |
| P2 | `science-pymoo-optimization` | 2.90 | 1 | 0 | 0 | 1 tool-like primary candidates; 1 candidates with scripts/references/assets |
| P2 | `science-rowan-chemistry` | 2.90 | 1 | 0 | 0 | 1 tool-like primary candidates; 1 candidates with scripts/references/assets |
| P2 | `science-simpy-simulation` | 2.90 | 1 | 0 | 0 | 1 tool-like primary candidates; 1 candidates with scripts/references/assets |
| P2 | `science-astropy` | 1.70 | 1 | 0 | 0 | 1 candidates with scripts/references/assets |
| P2 | `science-matchms-spectra` | 1.70 | 1 | 0 | 0 | 1 candidates with scripts/references/assets |
| P2 | `science-matlab-octave` | 1.70 | 1 | 0 | 0 | 1 candidates with scripts/references/assets |
| P2 | `science-neuropixels` | 1.70 | 1 | 0 | 0 | 1 candidates with scripts/references/assets |
| P2 | `science-pymatgen` | 1.70 | 1 | 0 | 0 | 1 candidates with scripts/references/assets |
| P2 | `science-pymc-bayesian` | 1.70 | 1 | 0 | 0 | 1 candidates with scripts/references/assets |
| P2 | `science-timesfm-forecasting` | 1.70 | 1 | 0 | 0 | 1 candidates with scripts/references/assets |
| P2 | `cloud-modalcom` | 0.90 | 1 | 0 | 0 | low structural risk |
| P2 | `science-tiledbvcf` | 0.90 | 1 | 0 | 0 | low structural risk |

## P0

| priority | pack | score | skills | route authority | stage assistant | rationale |
|---|---|---:|---:|---:|---:|---|
| P0 | `docs-media` | 83.10 | 17 | 0 | 0 | 17 skill candidates; no explicit role split; 5 suspected overlap pairs; 18 shared broad keywords; 10 tool-like primary candidates; 11 candidates with scripts/references/assets |
| P0 | `research-design` | 75.20 | 24 | 14 | 3 | 24 skill candidates; 14 route authorities; 3 suspected overlap pairs; 7 shared broad keywords; 2 tool-like primary candidates; 15 candidates with scripts/references/assets |
| P0 | `code-quality` | 70.60 | 16 | 0 | 0 | 16 skill candidates; no explicit role split; 16 suspected overlap pairs; 7 shared broad keywords; 1 tool-like primary candidates; 3 candidates with scripts/references/assets |
| P0 | `science-literature-citations` | 70.40 | 12 | 10 | 2 | 12 skill candidates; 10 route authorities; 16 shared broad keywords; 9 tool-like primary candidates; 11 candidates with scripts/references/assets |
| P0 | `bio-science` | 70.00 | 26 | 0 | 0 | 26 skill candidates; no explicit role split; 2 shared broad keywords; 15 tool-like primary candidates; 26 candidates with scripts/references/assets |
| P0 | `science-chem-drug` | 64.90 | 13 | 0 | 0 | 13 skill candidates; no explicit role split; 12 shared broad keywords; 6 tool-like primary candidates; 13 candidates with scripts/references/assets |

## P1

| priority | pack | score | skills | route authority | stage assistant | rationale |
|---|---|---:|---:|---:|---:|---|
| P1 | `scholarly-publishing-workflow` | 59.70 | 13 | 0 | 0 | 13 skill candidates; no explicit role split; 34 shared broad keywords; 4 tool-like primary candidates; 9 candidates with scripts/references/assets |
| P1 | `integration-devops` | 59.10 | 13 | 0 | 0 | 13 skill candidates; no explicit role split; 9 shared broad keywords; 3 tool-like primary candidates; 12 candidates with scripts/references/assets |
| P1 | `ai-llm` | 55.50 | 11 | 0 | 0 | no explicit role split; 20 shared broad keywords; 4 tool-like primary candidates; 6 candidates with scripts/references/assets |
| P1 | `science-lab-automation` | 55.10 | 7 | 0 | 0 | no explicit role split; 10 shared broad keywords; 6 tool-like primary candidates; 7 candidates with scripts/references/assets |
| P1 | `science-communication-slides` | 52.80 | 8 | 0 | 0 | no explicit role split; 10 shared broad keywords; 4 tool-like primary candidates; 6 candidates with scripts/references/assets |
| P1 | `data-ml` | 47.40 | 8 | 7 | 1 | 7 route authorities; 11 shared broad keywords; 1 tool-like primary candidates; 7 candidates with scripts/references/assets |
| P1 | `orchestration-core` | 46.80 | 27 | 1 | 26 | 27 skill candidates; 2 suspected overlap pairs; 5 shared broad keywords; 9 candidates with scripts/references/assets |
| P1 | `science-clinical-regulatory` | 44.90 | 7 | 0 | 0 | no explicit role split; 5 shared broad keywords; 5 tool-like primary candidates; 7 candidates with scripts/references/assets |
| P1 | `finance-edgar-macro` | 39.50 | 7 | 0 | 0 | no explicit role split; 2 shared broad keywords; 5 tool-like primary candidates; 7 candidates with scripts/references/assets |
| P1 | `science-medical-imaging` | 35.50 | 5 | 0 | 0 | no explicit role split; 5 shared broad keywords; 5 candidates with scripts/references/assets |
| P1 | `science-figures-visualization` | 31.30 | 5 | 2 | 3 | 11 shared broad keywords; 1 tool-like primary candidates; 4 candidates with scripts/references/assets |
| P1 | `science-reporting` | 31.30 | 5 | 2 | 3 | 10 shared broad keywords; 1 tool-like primary candidates; 4 candidates with scripts/references/assets |
| P1 | `ruc-nlpir-augmentation` | 27.60 | 4 | 2 | 2 | 14 shared broad keywords; 2 candidates with scripts/references/assets |
| P1 | `aios-core` | 25.40 | 12 | 1 | 11 | 12 skill candidates; 1 suspected overlap pairs; 5 shared broad keywords; 1 tool-like primary candidates |
| P1 | `science-quantum` | 19.40 | 4 | 0 | 0 | 5 shared broad keywords; 3 tool-like primary candidates; 4 candidates with scripts/references/assets |

## P2

| priority | pack | score | skills | route authority | stage assistant | rationale |
|---|---|---:|---:|---:|---:|---|
| P2 | `science-geospatial` | 12.90 | 3 | 0 | 0 | 3 shared broad keywords; 2 tool-like primary candidates; 3 candidates with scripts/references/assets |
| P2 | `science-zarr-polars` | 12.60 | 4 | 0 | 0 | 3 shared broad keywords; 1 tool-like primary candidates; 3 candidates with scripts/references/assets |
| P2 | `ml-torch-geometric` | 12.00 | 2 | 0 | 0 | 1 suspected overlap pairs; 4 shared broad keywords; 1 candidates with scripts/references/assets |
| P2 | `science-peer-review` | 8.70 | 3 | 0 | 0 | 3 tool-like primary candidates; 3 candidates with scripts/references/assets |
| P2 | `web-scraping` | 4.60 | 2 | 0 | 0 | 1 tool-like primary candidates; 2 candidates with scripts/references/assets |
| P2 | `docs-markitdown-conversion` | 2.90 | 1 | 0 | 0 | 1 tool-like primary candidates; 1 candidates with scripts/references/assets |
| P2 | `ip-uspto-patents` | 2.90 | 1 | 0 | 0 | 1 tool-like primary candidates; 1 candidates with scripts/references/assets |
| P2 | `media-video` | 2.90 | 1 | 0 | 0 | 1 tool-like primary candidates; 1 candidates with scripts/references/assets |
| P2 | `ml-stable-baselines3` | 2.90 | 1 | 0 | 0 | 1 tool-like primary candidates; 1 candidates with scripts/references/assets |
| P2 | `science-fluidsim-cfd` | 2.90 | 1 | 0 | 0 | 1 tool-like primary candidates; 1 candidates with scripts/references/assets |
| P2 | `science-pymoo-optimization` | 2.90 | 1 | 0 | 0 | 1 tool-like primary candidates; 1 candidates with scripts/references/assets |
| P2 | `science-rowan-chemistry` | 2.90 | 1 | 0 | 0 | 1 tool-like primary candidates; 1 candidates with scripts/references/assets |
| P2 | `science-simpy-simulation` | 2.90 | 1 | 0 | 0 | 1 tool-like primary candidates; 1 candidates with scripts/references/assets |
| P2 | `science-astropy` | 1.70 | 1 | 0 | 0 | 1 candidates with scripts/references/assets |
| P2 | `science-matchms-spectra` | 1.70 | 1 | 0 | 0 | 1 candidates with scripts/references/assets |
| P2 | `science-matlab-octave` | 1.70 | 1 | 0 | 0 | 1 candidates with scripts/references/assets |
| P2 | `science-neuropixels` | 1.70 | 1 | 0 | 0 | 1 candidates with scripts/references/assets |
| P2 | `science-pymatgen` | 1.70 | 1 | 0 | 0 | 1 candidates with scripts/references/assets |
| P2 | `science-pymc-bayesian` | 1.70 | 1 | 0 | 0 | 1 candidates with scripts/references/assets |
| P2 | `science-timesfm-forecasting` | 1.70 | 1 | 0 | 0 | 1 candidates with scripts/references/assets |
| P2 | `cloud-modalcom` | 0.90 | 1 | 0 | 0 | low structural risk |
| P2 | `science-tiledbvcf` | 0.90 | 1 | 0 | 0 | low structural risk |

## 边界说明

- 本报告只说明治理优先级，不代表删除建议。
- 具体 pack 收敛需要下一轮 problem-first 设计。
- 带 scripts、references、examples 或 assets 的 skill 不能直接删除。
- 若后续修改路由，需要补对应 route regression probe。
