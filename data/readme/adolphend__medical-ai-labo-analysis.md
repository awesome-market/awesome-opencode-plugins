# Medical AI Laboratory — Clinical Tool Development

**Mission:** develop modular, disease-specific **clinical decision-support and diagnostic workflow tools** for eventual use by qualified healthcare professionals. The project is currently in the **research and prototype-development stage**: no component has established clinical safety, effectiveness, regulatory clearance, or authorization for routine patient care. The target product is a collection of usable clinical tools, not merely a benchmarking repository or a standalone large language model.

**Intended future workflow:** clinical intake → indication and examination selection → data acquisition and QC → specialist model-assisted findings and measurements → evidence-linked draft report → clinician-reviewed diagnostic interpretation and management options → documented follow-up. Every clinical decision remains under accountable professional oversight until and unless a separately validated and appropriately authorized tool is established.

**Research areas:** clinical AI tools, medical imaging AI, open-source medical models, diagnostic decision support, ultrasound, chest X-ray, CT, MRI, medical image segmentation, MedGemma benchmarks, dataset evaluation, and agent-assisted clinical software development.

[Discoverability and research topic index](docs/DISCOVERABILITY.md) · [Medical AI model analysis](research/imaging/model-integration-registry.md) · [Clinical disease workflows](diseases/README.md) · [Evaluation and benchmark research](evaluation/README.md)

## Development status: planning first, implementation later

**The clinical tools have not been developed yet.** This repository is presently a **research, requirements, architecture and agent-planning workspace**. Existing Python scripts, JSON schemas, benchmark examples and installation helpers are exploratory infrastructure/prototypes; they are **not** implemented clinical products or evidence that disease workflows function end to end.

**Future implementation will be generated iteratively using OpenCode agents**, with human review and explicit project decisions before each increment. Agent configurations and skills currently describe intended work; they do not mean that agents have executed the work, created the external model forks, downloaded datasets, trained models, tested hardware, or validated clinical functions.

### Planned agent-led development sequence

1. **Requirements and intended-use definition:** select one clinical tool/disease and define users, patient setting, supported actions, exclusions, safety boundaries and acceptance criteria.
2. **Architecture and agent plan:** design the model selection/forking agent, source/weight/license audit agent, dataset agent, adapter/implementation agent, model evaluation agent, integration agent, UI agent and quality/safety reviewer. Specify responsibilities, input/output contracts, human approval gates and execution order.
3. **Research and model selection:** inventory all applicable small/pretrained models, legal terms and exact releases; decide whether each source requires a fork or a pinned dependency.
4. **Dataset and test design:** find legally usable datasets, expert reference labels, versioning, partitioning, metrics and pass/fail criteria **before** implementing or running model tests.
5. **Incremental code generation:** direct OpenCode to implement one bounded, testable component at a time; review every generated change, dependency and model checkpoint.
6. **Independent component evaluation:** test each candidate model on appropriate task-specific data and hardware; record actual performance, failures, abstentions and provenance.
7. **Clinical workflow integration:** assemble qualified components into one disease-specific tool; test interfaces, audit trail, interoperability and error propagation.
8. **Later clinical and regulatory work:** plan evidence generation and approvals separately; no direct patient-care deployment without the required validation and authorization.

**Not yet completed:** clinical tool implementation, operational agent orchestration, external model forks, all-model benchmarks, full 50-disease runtime pipelines, clinician validation, and clinical deployment. These are **planned deliverables**, not completed features.

## Where to start

| Area | Documentation |
|---|---|
| 50 disease/checkup starting conditions | [Disease registry and folders](diseases/README.md) |
| Modality-specific workflow analyses | [Imaging research](research/imaging/README.md) |
| Diagnostic modules and academic evidence | [Research index](research/README.md) |
| Disease procedure JSON and interpreter | [JSON procedure pipeline](pipeline/README.md) |
| Open-source model inventory/fork methodology | [Model integration registry](research/imaging/model-integration-registry.md) · [Fork agent](automation/README.md) |
| Evaluation metrics, datasets and DVC | [Evaluation framework](evaluation/README.md) |
| **MedGemma independent technical/clinical analysis** | [MedGemma analysis](evaluation/medgemma-technical-clinical-analysis.md) |
| MedGemma 50-disease nine-stage evaluation strategy | [End-to-end evaluation](evaluation/medgemma-end-to-end-50-diseases.md) |
| **Real public image + labels example** | [PneumoniaMNIST case](evaluation/cases/pneumonia-medmnist/README.md) |
| Windows / Ubuntu / Mac model setup | [Cross-platform installation](models/medgemma-local/INSTALL-CROSS-PLATFORM.md) |
| OpenCode agents and skills | [Agent instructions](.opencode/README.md) |

## Workflow

1. Select a disease or checkup from `diseases/registry.csv`.
2. Create or refine `diseases/<slug>/procedure.json`, with patient entrypoint, required/optional tests and dependencies. Tests **need not involve imaging**.
3. Identify source-linked clinical guidelines, suitable datasets and model registries; mark unavailable, restricted, or unsupported cases explicitly.
4. Evaluate each JSON step **separately**: context, red flags, examination selection, quality control, findings, diagnostic synthesis, reporting, management evidence and follow-up.
5. Retain per-step prediction provenance, evaluation dataset version, model weights/commit, reference labels, metrics, error analysis, human review, and auditable results.
6. Only afterward study end-to-end propagation of errors. A single strong AI benchmark does not establish clinical safety.

### Repository setup

```bash
git clone https://github.com/adolphend/medical-ai-labo-analysis.git
cd medical-ai-labo-analysis
python3 scripts/scaffold_diseases.py
python3 scripts/medgemma_disease_pipeline.py --output evaluation/results/medgemma-nine-stage-plan.json
python3 scripts/run_evaluation_pipeline.py
```

The offline pipeline uses **synthetic fixtures** for code testing. It does not load model weights.

### Optional local MedGemma on NVIDIA GPUs (8 GB development example)

```bash
python3 models/medgemma-local/install.py --backend cuda
python3 models/medgemma-local/install.py --backend cuda --apply
.venv-medgemma/bin/python models/medgemma-local/verify.py
```

Then accept Google's Health AI Developer Foundations terms on [MedGemma Hugging Face](https://huggingface.co/google/medgemma-1.5-4b-it), authenticate with the local Hugging Face CLI, and explicitly run `models/medgemma-local/download.py --apply`. 4-bit weight-loading **may** fit on an RTX 4060 8GB; actual compatibility and peak VRAM have not been measured.

### One real-data image benchmark (opt-in)

```bash
# Download authorized official public image array and test labels:
python3 scripts/medgemma_pneumonia_case.py --download

# Requires local gated MedGemma weights and CUDA runtime:
.venv-medgemma/bin/python scripts/medgemma_pneumonia_case.py --infer --limit 20

# Score only genuine generated predictions, with abstention coverage:
python3 scripts/medgemma_pneumonia_case.py --score
```

Read the [case's methodology and limitations](evaluation/cases/pneumonia-medmnist/README.md). This dataset is a resized pediatric chest-radiograph benchmark; **it cannot validate clinical pneumonia diagnosis**, therapeutic recommendations or applicability to adults. Do not claim the pipeline measured clinical accuracy unless real inference was actually executed.

## Multi-model analysis and new-model development

The project evaluates **multiple specialized models**, not just MedGemma. Each disease may combine clinical text extraction, examination selection, quality control, segmentation, detection, interpretation and clinician-reviewed guideline evidence. Different models can also compete for the **same task**. A model is never assumed valid for a disease simply because its upstream repository is available.

### Available analysis options

| Analysis track | Representative existing models/tools | Evaluation questions |
|---|---|---|
| Clinical context and reporting | MedGemma 1.5, medSpaCy, CheXbert, RadGraph, Whisper (transcription) | Facts, missing context, contradictions, hallucinations, missed red flags, source fidelity |
| Ultrasound | EchoNet-Dynamic, SonoNet, MedSAM (prompted segmentation) | Correct plane, left-ventricular measurement error, anatomy masks, patient/site shift |
| Chest X-ray | TorchXRayVision, CheXzero, MedGemma | Per-finding sensitivity/specificity, label uncertainty, out-of-domain errors |
| CT | TotalSegmentator, task-specific MONAI bundles, LUNA16 benchmark implementations | Segmentation Dice and measurement error, nodule sensitivity/false positives per scan |
| MRI | MRIQC, ANTsPyNet, task-specific MONAI models, MedSAM | QC sensitivity, region masks, lesion reference labels, sequence/site robustness |
| Microscopy/pathology | HoVer-Net, Cellpose, QuPath, HistoQC | Nucleus masks, tissue artifacts, classification error and scanner/stain shift |
| Physiological signals | WFDB, NeuroKit2, task-specific ECG classifiers to verify | Signal quality, patient-level sensitivity, rhythm classification; not image interpretation |
| Clinical information systems | HAPI FHIR, OHIF, Orthanc, Medplum | Data provenance, interface correctness, report delivery, acknowledgement and follow-up |

These are **research candidates and infrastructure**, not an approved set of clinical diagnostic models. Some have pretrained checkpoints and some are frameworks, benchmarks or non-AI tools; weight access, code/data licenses and independent validation must be reviewed for each.

### Model selection and development decision

1. **Define the target and reference standard**: disease, patient group, imaging or non-imaging examination, intended outcome, and human review.
2. **Inventory alternatives**: use the [model integration registry](research/imaging/model-integration-registry.md) and [fork manifest](automation/model-forks.json). Distinguish a reusable pretrained model from a framework needing task-specific weights.
3. **Use the same authorized cases where comparable**: lock dataset and split using [DVC governance](evaluation/README.md), verify train/test contamination and licensing, freeze prompts and preprocessing.
4. **Test each model separately**: record exact version, weights, input/output JSON contract, reference labels, task metrics, confidence intervals where feasible, latency, peak GPU/CPU RAM, abstentions and failures.
5. **Compare only like-for-like outputs**: classification against classification, segmentation against segmentation, measurement against reference measurement, and clinical context against adjudicated context. A Dice score cannot be compared directly with medical-text F1.
6. **Test multi-model integration**: evaluate errors propagated between image quality, anatomy, finding detection and report generation; verify that a failed early stage cannot turn into a confident downstream diagnosis or management suggestion.
7. **Develop a new model only for a verified gap**: start with a deterministic baseline or pretrained model; consider calibration or parameter-efficient adaptation if permitted; train from scratch only when evidence, labeled data, rights and computing resources justify it. The developer's **8 GB RTX 4060** is one reproducible benchmark target, **not** the deployment minimum, maximum, or constraint for everyone. Profile model training and inference separately for CPU-only, low-memory, mid-range and high-memory systems.
8. **Release only research outputs with traceability**: write per-step scores/results into [disease procedure JSON](pipeline/README.md) and a model evaluation card. Human specialist verification remains mandatory before any clinical care decision; no autonomous treatment or prescription.

### Example composition: lightweight, task-specific components

**Default architecture: no large language model required.** Start with small, task-specific pretrained models, deterministic rules, or manual specialist review. MedGemma is an **optional benchmark comparator**, not a mandatory stage. Actual GPU memory, system RAM and CPU-only feasibility must be measured across hardware tiers, never assumed from the developer's machine.

```text
Patient intake        → structured form + medSpaCy (rule-based extraction)
Examination selection → guideline lookup + deterministic eligibility rules + clinician
Image QC              → metadata/geometry checks; SonoNet for fetal planes only
Anatomy/measurement   → small task-specific segmentation model or manual measurement
Finding detection     → a verified small specialist classifier; otherwise MODEL_GAP
Reporting             → structured templates with linked source observations
Management evidence   → versioned guideline retrieval and clinician review
Follow-up             → deterministic task tracking and result acknowledgement
```

For a concrete **cardiac ultrasound** research task, [EchoNet-Dynamic](https://github.com/echonet/dynamic) is a candidate for ejection-fraction assessment; for chest radiographs, a selected [TorchXRayVision](https://github.com/mlmed/torchxrayvision) checkpoint is an alternative. Both require actual checkpoint, licensing, accuracy and memory audits before use. **Do not combine unrelated modality models into one disease pipeline.** Use classical image analysis or a smaller approved model when a deep network is unnecessary.

Evaluate any candidate against a non-AI baseline and optionally against [MedGemma](evaluation/medgemma-technical-clinical-analysis.md) *only on compatible tasks with identical independent reference cases*. The disease JSON must identify exactly which components were evaluated and where clinician approval is required.

## Product development stages and clinical readiness gates

| Stage | Deliverable | Exit requirement |
|---|---|---|
| **1. Research and planning (current)** | Disease needs analysis, model inventory/forks, evidence and benchmark datasets, exploratory clinical workflow designs | Document precise intended use, target users/patients, risks, reference standards and repeatable evaluation |
| **2. Engineering prototype** | Runnable end-to-end software with verified model adapters, interfaces, traceable outputs, privacy protections and secure data processing | Integration tests, role separation, logging, error handling, versioned build, reproducible performance |
| **3. Clinical evaluation** | Locked intended-use system evaluated on representative independent clinical cases with appropriate clinician oversight | Predefined safety/performance endpoints, expert adjudication, bias and site-shift analysis, prospective study if appropriate |
| **4. Regulatory and quality review** | Jurisdiction-specific classification, risk management, quality system, clinical evidence, security and monitoring documentation | Applicable regulatory and institutional approvals; clearance/certification when legally required |
| **5. Controlled clinical deployment** | Clinician-facing installation, instructions, monitoring, rollback and post-deployment change control | Authorized use only, with human accountability and ongoing safety/performance monitoring |

A benchmark success or a GitHub fork is **not** evidence of clinical readiness. Each tool must specify its **intended clinical purpose**, end user, care environment, eligible patients, contraindicated/missing inputs, expected clinician action, claims supported by evidence and escalation/human-review behavior. Requirements and validation are tool-specific; do not assume every tool is legally regulated in the same way.

### Engineering requirements from the beginning

- **Workflow usability:** clinician-oriented interfaces, explainable findings, appropriate uncertainty display, explicit draft versus signed outputs, traceable input series and follow-up ownership.
- **Interoperability:** structured patient, encounter, imaging and report identifiers; consider DICOM/PACS for imaging and FHIR/HL7 for records as applicable.
- **Reliability and security:** least-privilege access, encryption where appropriate, audit trails, version-controlled models, data minimization, incident handling, backups and rollback.
- **Clinical risk controls:** define hazards such as false negatives, incorrect laterality, missing urgent findings, examination mismatch, unsafe management options, and automation bias; test mitigations.
- **Evidence and validation:** independently assess each forked model, complete workflow and hardware/backend deployment profile; distinguish model performance from actual clinical usefulness.
- **Development scope:** research prototypes use synthetic or appropriately authorized de-identified data. No routine real-patient diagnosis, treatment or autonomous prescription from the current repository.

## Hardware compatibility: scalable from CPU-only to large GPUs

The maintainer currently has an **NVIDIA RTX 4060 with 8 GB VRAM** for development. **That is not a required GPU**: other researchers and users may have no dedicated GPU, less memory, or substantially more GPU memory and compute. The architecture must be hardware-adaptive, while acknowledging that some specialized models cannot run on every device.

| Hardware profile | Model/runtime selection | Evaluation requirements |
|---|---|---|
| CPU only; 8 GB system RAM | Structured rules, classical algorithms, small quantized models where they fit; optionally offline manual workflows | Peak RAM, total latency, correctness, ability to complete without model installation |
| Low-end GPU (2–6 GB VRAM) | Tiny task-specific checkpoints, reduced input size only when scientifically valid, quantization | CUDA/Metal/device compatibility, OOM rate, accuracy changes versus reference |
| Mid-range GPU (8 GB VRAM; development RTX 4060) | Task-specific pretrained models and selected 4-bit medical-language comparators | Measured VRAM/host RAM, preprocessing and generation throughput, accuracy |
| Larger GPU (12–24 GB VRAM) | Higher precision, larger batches, more simultaneous components, additional model candidates | Same held-out evaluation; throughput, performance and power/cost |
| Workstation/server (24+ GB VRAM, possibly multi-GPU) | Heavy volumetric/whole-slide pipelines, expanded ensembles and training/adaptation when justified | Reproducible distributed settings, scaling gains, accuracy and resource costs |
| Apple Silicon/macOS | Metal/MPS-compatible models and runtimes; quantization availability varies | Unified-memory peak and compatibility; do not assume CUDA/bitsandbytes |

**Required architecture:** components declare minimum *tested* hardware, optional accelerators, model weight format, memory footprint, supported backend (CPU/CUDA/MPS), exact input limits and fallback behavior. A **capability detection/selection layer** chooses a compatible implementation at runtime; it must not silently substitute a medically different or unvalidated model. If no validated component fits, report `UNAVAILABLE_ON_THIS_DEVICE` and preserve manual/human-reviewed workflow instead of inventing an answer.

**Benchmark policy:** compare accuracy on exactly the same authorized dataset where model inputs remain clinically equivalent. Record separate latency, throughput, peak **system RAM** and **GPU VRAM**, loading time, quantization changes, and device-specific failures for each model. Hardware speed and medical accuracy are separate criteria. Larger hardware may support additional models or higher-resolution inputs, but does **not** confer clinical validity. Models that are not compatible with CPU-only systems remain valid optional research modules, clearly marked as such.

**Development vs deployment:** the initial developer GPU is one test profile, not a published minimum specification. Training hardware requirements can be greater than inference requirements. Windows, Linux/WSL and macOS have distinct backend support; provide per-platform installers and independently run smoke tests before claiming support. **Do not report untested hardware as compatible.**

## Minimum baseline: fork, test, evaluate and integrate **every** model

**This baseline is mandatory for all 41 identified external repositories** (including infrastructure and model frameworks), not merely the first example or MedGemma. The [full upstream manifest](automation/model-forks.json) records recommended `fork`, `dependency` or `review` dispositions. **A dependency classification does not exempt a component from integration testing**; a fork is warranted only when code modification or independent maintenance justifies it. The research objective is to evaluate **all applicable models individually**, then evaluate their compatibility and the full disease pipeline.

### 1. Model intake and forking requirements

For **each** entry in [automation/model-forks.json](automation/model-forks.json):

1. Confirm original GitHub repository/owner, latest usable release, archival/maintenance status, security implications, paper and exact clinical task. Distinguish trained weights, benchmarks, frameworks and infrastructure.
2. Audit **four independent legal elements**: code license, pretrained checkpoint/license, source dataset rights, and commercial deployment terms. Keep unverified entries blocked.
3. Determine **fork or dependency**. For an upstream source requiring code changes, create a GitHub fork under the project owner. Otherwise install a pinned dependency or managed service. A public repo is not permission to use every model weight.
4. Pin upstream commit and checkpoint hash; record architecture, preprocessing, runtime, inputs, outputs, approved evidence and responsible maintainer. Prefer **no-training/CPU-capable small models** when feasible; benchmark across hardware profiles rather than imposing a universal 8 GB GPU limit.
5. Store source forks as separate GitHub repositories. Use optional Git submodules for source pointers; **never copy all model repositories, datasets or checkpoints into the main Git history**.
6. Record fork URL and review status in `automation/forks-tracked.json` using the [forking agent](automation/fork_models.py) once executed, and make a reviewed `git add` / `git commit` / `git push`.

[Complete model-specific fork procedures](automation/README.md) · [Fork and upstream sync methods](research/imaging/model-fork-and-evaluation-process.md)

```bash
# Preflight: read every model's action and requirements
python3 automation/fork_models.py --all

# Controlled first batch; creates external forks and records them only with --apply
python3 automation/fork_models.py --models echonet,sononet --apply --push

# Explicitly attempt all 41, INCLUDING items normally better pinned as dependencies;
# review licenses and suitability individually BEFORE doing this:
# python3 automation/fork_models.py --all --apply --push
```

**No external fork has been executed or verified by this ChatGPT work.** The agent requires authenticated GitHub CLI, a clean synchronized `main` worktree and correct origin. An attempted partial batch may need recovery and GitHub rate limits or repository naming conflicts may arise.

### 2. Per-model qualification — individually, without skipping

Every model or software component must have a distinct **model/tool evaluation card** documenting:

| Gate | Required artifact or evaluation |
|---|---|
| Source provenance | Upstream/fork URL, exact Git SHA, original paper DOI, model role, maintenance |
| Legal usage | Code and weight licenses, data agreement, commercial restrictions |
| Installation | Python/runtime/OS/GPU/CPU dependencies; reproducible lock and smoke test |
| Data | Official matching dataset, patient-level split, reference labels, DVC version and hash |
| Technical correctness | Input format, modality, units, orientation, preprocessing and output schema |
| Component quality | Task-specific metric (classification, segmentation, detection, regression, context extraction, calibration or operational QC) |
| Safety & reliability | Wrong-modality rejection, abstention, missing-data handling, false negatives, provenance and error logging |
| Deployment feasibility | Measured inference time, peak RAM/VRAM and disk use on target hardware |
| Clinical validity | External-cohort or independent specialist review, subgroup performance and limitations |
| Status | `not_tested`, `blocked`, `failed`, `research_pass`, or `clinically_validated` (**never infer the last from benchmark accuracy**) |

An infrastructure service is tested for data integrity, privacy, security and handoff correctness, **not** artificial diagnostic sensitivity. An unsuitable or unavailable pretrained checkpoint is marked `MODEL_GAP`, not awarded an invented performance number.

[Evaluation protocol](evaluation/protocol.md) · [Evaluation card](evaluation/evaluation-card-template.md) · [Datasets for 50 diseases](evaluation/disease-dataset-mapping.md) · [DVC](evaluation/README.md)

### 3. Reproducible procedure for evaluating one model

```bash
# Read model-specific procedures and approved dataset status
python3 scripts/check_datasets.py
python3 scripts/check_disease_dataset_catalog.py

# Verify source-code metrics and synthetic pipeline (NO real model scored)
python3 scripts/run_evaluation_pipeline.py
python3 -m unittest discover -s tests -p 'test_*.py' -v

# Preview dataset acquisition. Download only after rights + HTTPS + checksum audit
python3 scripts/download_dataset.py --dataset DATASET_ID

# Evaluate a real model only after compatible model adapter and datasets exist
# /evaluate-model DISEASE_SLUG MODEL_ID    (inside OpenCode)
```

**Individual tests:** use dedicated task metrics. Classification: sensitivity/specificity, precision/NPV, calibration; segmentation: Dice/IoU and boundary distances; detection: FROC and false positives per scan; quantitative measurement: MAE, bias; context: fact extraction, omissions and escalations. Document confidence intervals, test prevalence, baseline and failures. The committed Python implementation currently provides **binary and structured-context scorers**, not every specialty metric.

### 4. Multi-model comparison — after individual qualification

- For each disease JSON stage, identify **every relevant candidate** from the registry (e.g., more than one CXR classifier), the deterministic/non-AI baseline and an optional general model such as MedGemma.
- Use exactly the same *authorized, task-matched* held-out cases and reference standard for like-for-like comparisons; otherwise mark `NOT_COMPARABLE`. Pin prompts, thresholds, weights and preprocessing.
- Compare model performance, abstention, false-negative risks, resource cost, model size and failure modes. Never combine scores for incompatible tasks (e.g., segmentation Dice with textual F1).
- Test ensembles/routing only after measuring their **incremental gain and error propagation**, including whether a weak QC model degrades an otherwise strong detection model.
- Record a separate JSON result for each model × disease × procedure step. A successful component test **does not certify the full workflow**.
- MedGemma remains an **optional research comparator**, not the baseline requirement or a compulsory component.

[JSON procedure contract](pipeline/README.md) · [Model-by-model integration list](research/imaging/model-integration-registry.md) · [MedGemma comparison](evaluation/medgemma-50-disease-pipeline.md)

### 5. End-to-end test — each of the 50 disease pathways

For a representative, expert-reviewed case, validate: **patient intake → red-flag/missing-context review → screening/diagnostic examination decision (including no imaging) → appropriate acquisition/QC → anatomical localization → disease finding model(s) → uncertainty and specialist report → clinician-controlled guideline evidence → results acknowledgement and follow-up**.

For every step, record `entrypoint`, `depends_on`, `required`, `input_keys`, `output_keys`, model ID/revision, independent dataset, `evaluation.status`, artifact path, abstention policy and human-review requirement in `diseases/<slug>/procedure.json`. The [interpreter](scripts/interpret_procedure.py) currently **plans and validates** steps, but **does not run** arbitrary medical models. Full care-path tests need separate compatible adapters, reviewed data and source-verified guidelines; no automatic treatment selection or prescribing.

### 6. Completion gates and progress ledger

The **minimum project completion bar** is: (a) all 41 upstream entries receive a documented fork/dependency disposition and license audit; (b) each usable model has a runnable smoke test and reproducible *individual* evaluation or explicit reason it cannot be tested; (c) all applicable models for each of the 50 diseases are compared on valid cases; (d) each disease has a reviewed stage-by-stage JSON procedure and end-to-end error-handling test; and (e) everything is referenced by Git/DVC revisions and evaluation reports. **None of these milestones is automatically complete merely because its Markdown description exists.**

**Actual status:** inventory and planning code committed; actual forks, full-dataset downloads, all-model inference, external clinical validation, and 50-disease integrated tests are **not completed**. Published upstream paper scores must never be labeled as local measurements.

## Dataset control

[Dataset candidates for the 50 conditions](evaluation/disease-dataset-mapping.md) require individual access and label reviews. Data and weights are excluded from Git. [DVC guidance](evaluation/README.md) describes local versioning and protected remotes; never push protected records to public storage. Records of completed tests must include hashes, versioned labels and source documentation.

## OpenCode

Run OpenCode from the repository root. Commands include `/build-disease heart-failure`, `/evaluate-model heart-failure echonet`, and `/run-evaluation heart-failure echonet`. The skills and commands are research aids, not clinicians. See [.opencode/README.md](.opencode/README.md).

## Project status

- **Documented:** 50 starting clinical conditions and disease folders; candidate open-source projects/datasets; modality research; JSON procedure and evaluation specifications.
- **Exploratory helper/prototype code (not clinical product implementation):** dataset download/governance, synthetic scoring, context metrics, per-disease evaluation planning, controlled local MedGemma installation, optional chest X-ray benchmark.
- **Not established:** end-to-end real-model execution across the 50 diseases, model accuracy on local hardware, dataset suitability across all conditions, clinical/regulatory validation or autonomous treatment safety.

**Evidence standards:** cite actual academic studies and clinical guidelines; separate the paper's result from our locally measured output; expose uncertainty, incomplete coverage and limitations.

## License and third-party rights

**[PolyForm Noncommercial License 1.0.0](LICENSE)** applies to the project's original material, to the extent the contributors have rights to license it. This existing source-available license permits **noncommercial use, modification, and redistribution**, with required license notices. **Commercial use is not authorized under this license**; organizations intending commercial use must contact the rights holder for a separate written agreement. The official text also disclaims warranties and limits licensor liability **as far as the law allows**; it cannot prevent lawsuits or override mandatory legal obligations.

Not all institutional research is automatically noncommercial; check the license's definitions and commercial-purpose restrictions. Source availability does not equal OSI-approved open source.

**Earlier MIT versions:** replacing the license now does not retroactively cancel permissions previously granted under MIT for earlier revisions. Third-party models, weights, datasets and dependencies retain their own license terms. Clinical-use restrictions and applicable regulatory/privacy obligations are separate from copyright licensing; the current repository is not validated for patient care.
