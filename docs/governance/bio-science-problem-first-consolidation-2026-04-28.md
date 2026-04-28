# Bio-Science Problem-First Consolidation

Date: 2026-04-28

## Summary

This pass governs only the `bio-science` pack.

The pack keeps all 26 physical skill directories, but changes the routing contract from a flat candidate list into explicit route authorities and stage assistants.

| field | before | after |
| --- | ---: | ---: |
| `skill_candidates` | 26 | 26 |
| `route_authority_candidates` | 0 | 10 |
| `stage_assistant_candidates` | 0 | 16 |
| physical directory deletion | 0 | 0 |

Physical deletion is deferred because every candidate either owns a distinct problem or has database, reference, script, or asset value that needs a migration review before removal.

## Route Authorities

| user problem | owner |
| --- | --- |
| Single-cell RNA-seq clustering, annotation, marker genes, UMAP/t-SNE, h5ad/10X workflow | `scanpy` |
| Bulk RNA-seq differential expression, DESeq2-style statistics, volcano/MA plots | `pydeseq2` |
| BAM/SAM/CRAM/VCF parsing, pileup, coverage, variant-file handling | `pysam` |
| FASTA/GenBank/SeqIO, sequence conversion, NCBI Entrez Python workflow | `biopython` |
| Quick gene, transcript, BLAST, Ensembl, or symbol lookup | `gget` |
| Protein language model tasks and protein embeddings | `esm` |
| Metabolic network modeling, FBA, constraint-based metabolic models | `cobrapy` |
| FCS / flow cytometry file reading and channel matrix handling | `flowio` |
| Gene regulatory network inference, pySCENIC, transcription-factor network tasks | `arboreto` |
| Genomic ML and genome embedding tasks | `geniml` |

## Stage Assistants

| assistant | target owner | why stage-only |
| --- | --- | --- |
| `anndata` | `scanpy` | AnnData/h5ad is a data container inside single-cell workflows. |
| `scvi-tools` | `scanpy` | scVI modeling is useful but should not own broad single-cell prompts in this split. |
| `deeptools` | `pysam` | Genomics track processing is narrower than alignment/variant file handling. |
| `bioservices` | database assistants | Cross-database lookup should not override a specific workflow owner. |
| `alphafold-database` | `esm` | Predicted structure evidence supports protein workflows. |
| `clinvar-database` | `pysam` | Clinical variant evidence supports variant interpretation. |
| `cosmic-database` | `pysam` | Cancer variant evidence supports variant interpretation. |
| `ensembl-database` | `gget` | Ensembl evidence supports quick gene/transcript lookup. |
| `gene-database` | `gget` | Gene annotation evidence supports lookup and annotation workflows. |
| `gwas-database` | `gget` | Trait evidence supports genetics workflows. |
| `kegg-database` | `cobrapy` | KEGG evidence supports metabolism and pathway workflows. |
| `opentargets-database` | `gget` | Target-disease evidence supports gene/target workflows. |
| `pdb-database` | `esm` | Protein structure evidence supports protein workflows. |
| `reactome-database` | `cobrapy` | Pathway evidence supports metabolism and pathway interpretation. |
| `string-database` | `esm` | Protein interaction evidence supports protein workflows. |
| `cellxgene-census` | `scanpy` | Single-cell reference evidence supports scanpy workflows. |

## Protected Route Probes

| prompt | expected |
| --- | --- |
| `做单细胞RNA-seq聚类与注释，使用scanpy` | `bio-science / scanpy` |
| `读取h5ad，做Leiden clustering和marker genes` | `bio-science / scanpy` |
| `进行bulk RNA-seq差异表达分析并画volcano plot` | `bio-science / pydeseq2` |
| `解析BAM和VCF文件并统计覆盖度` | `bio-science / pysam` |
| `用BioPython处理FASTA序列并转换GenBank格式` | `bio-science / biopython` |
| `用gget快速查询基因symbol和Ensembl ID` | `bio-science / gget` |
| `用ESM生成protein embeddings` | `bio-science / esm` |
| `用COBRApy做FBA代谢通量分析` | `bio-science / cobrapy` |
| `读取FCS流式细胞文件并提取通道矩阵` | `bio-science / flowio` |
| `用pySCENIC/arboreto推断基因调控网络` | `bio-science / arboreto` |
| `用geniml做基因组机器学习和genome embedding` | `bio-science / geniml` |

## False-Positive Protection

| prompt | expected |
| --- | --- |
| `用RDKit解析SMILES并计算Morgan fingerprint` | `science-chem-drug / rdkit` |
| `在PubMed检索文献并导出BibTeX` | `science-literature-citations / pubmed-database` |
| `写论文投稿cover letter和rebuttal matrix` | `scholarly-publishing-workflow / submission-checklist` |
| `用scikit-learn训练分类模型并交叉验证` | `data-ml / scikit-learn` |
| `读取DICOM并提取tags` | `science-medical-imaging / pydicom` |

## Audit Artifacts

The problem-map gate writes:

```text
outputs/skills-audit/bio-science-problem-map.json
outputs/skills-audit/bio-science-problem-map.csv
outputs/skills-audit/bio-science-problem-consolidation.md
```

Expected audit summary:

| category | count |
| --- | ---: |
| route authorities | 10 |
| stage assistants | 16 |
| manual review | 0 |
| merge/delete after migration | 0 |

## Deletion Boundary

This pass performs routing and config cleanup only.

No physical skill directory is deleted in this pass. A future deletion pass must prove all of the following before removing any directory:

1. The skill has no distinct user problem after problem-map review.
2. Useful references, scripts, examples, and assets have been migrated or intentionally rejected.
3. No live route, profile, test, lockfile, or packaging surface depends on the directory.
4. Offline skills, config parity, and route regression gates pass after removal.

## Verification

Run:

```powershell
python -m pytest tests/runtime_neutral/test_bio_science_pack_consolidation_audit.py -q
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-bio-science-pack-consolidation-audit-gate.ps1 -WriteArtifacts -OutputDirectory outputs\skills-audit
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-skill-index-routing-audit.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\probe-scientific-packs.ps1 -Unattended
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-regression-matrix.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-pack-routing-smoke.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-generate-skills-lock.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-offline-skills-gate.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\verify\vibe-config-parity-gate.ps1 -WriteArtifacts
```

Report any unrelated pre-existing route or metadata failures separately from this pack.
