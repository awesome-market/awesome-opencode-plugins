<div align="center">
  <img src="logo/banner.png" alt="Kernel Evo banner" />
</div>

**Evolutionary generation of efficient GPU kernels.** Use a coding agent to author candidates while
KernelEvo manages correctness checks, benchmarks, profiling, and the evolution archive. Direct-LLM
evolution is also available through [GigaEvo](https://github.com/FusionBrainLab/gigaevo-core).

[Agent quickstart](#quickstart-with-a-coding-agent) · [Direct-LLM evolution](docs/direct-llm.md) ·
[Agent reference](docs/agent-guide.md)

<div align="center">
  <img src="logo/plotly_speedup_vs_tokens_level1_v3.gif" alt="Speedup vs tokens lvl 1" width="49%" />
  <img src="logo/plotly_speedup_vs_tokens_level2_v3.gif" alt="Speedup vs tokens lvl 2" width="49%" />
</div>


## Requirements

Python 3.12+, an NVIDIA GPU environment with the task's dependencies, and a coding agent with shell
access and subagent support (Codex, Claude Code, or OpenCode).

## Quickstart with a coding agent

### 1. Install KernelEvo and the skill

In a Python 3.12+ environment on your GPU host:

```bash
git clone https://github.com/AXXX-Institute/kernel-evo.git
cd kernel-evo
python -m pip install -e .
kernel-evo --help
```

Backend dependencies come from your existing conda/venv environment. Run your agent from this checkout
with `kernel-evo` on `PATH`; the skills are already included.

To use KernelEvo in **another repository**, copy these paths from this checkout into the same relative
locations in your project. Copy only the listed files/directories, preserving existing agent settings:

| Agent | Files to copy into your project |
| --- | --- |
| All agents | `.agents/skills/kernelevo/` and `docs/bundles.md` |
| Codex | No additional files |
| Claude Code | `.claude/skills/kernelevo/` and `.claude/agents/kernelevo-*.md` |
| OpenCode | `.opencode/agents/kernelevo-*.md` |

Restart the agent in your project after copying. Keep the shared skill and its references together:
the Claude wrapper links to them. Skill discovery: [Codex](https://developers.openai.com/codex/skills/),
[Claude Code](https://code.claude.com/docs/en/skills), [OpenCode](https://opencode.ai/docs/skills/).

### 2. Initialize your project

Ask your agent (replace paths and test requirements):

> Use the kernelevo skill to init this repo for optimizing `src/my_kernel.py`.
> Create eval with tests: output L2 error under 1e-4 against the reference.
> Generate config with CuTe + Triton, BF16, cuda:0, 3 islands for 8 iters.
> Use my conda env `/path/to/conda/envs/kernels/bin/python`.
> Use subagents for authoring (Codex: `gpt-5.6-sol`, or `gpt-6-astra`).
> Use ncu/torch.compile profiling.
> Initialize the run and report its ID.

Choose the error metric and tolerance for your workload. NCU and PyTorch are profiler runners;
`torch.compile` identifies the execution to profile.

The agent generates the config. Main settings you can change before initialization:

| Setting | Config field |
| --- | --- |
| Kernel languages | `backends.allowed`, `backends.required` |
| Precision and GPU | `evaluation.precision`, `evaluation.device` |
| Iterations per island / island count | `run.steps`, `run.islands` |
| Existing conda/venv interpreter | `environment.python` (absolute path) |
| Profiling | `profiling.enabled`, `profiling.runners: [torch, ncu]` |

See the [example config](examples/agent/evo.yaml), [mixed backend settings](docs/bundles.md),
and [agent reference](docs/agent-guide.md) for details.

### 3. Start, continue, or steer

Replace `RUN` with the returned run ID:

| Action | Tell the agent |
| --- | --- |
| Start | Start evolution for run `RUN` and complete all 8 iterations per island. |
| Resume | Continue run `RUN` from where it stopped. |
| Extend | Add 5 more iterations per island to run `RUN` and continue. |
| Steer | For run `RUN`, focus the next candidates on attention fusion. |

The skill handles status checks, extension, and steering through KernelEvo. Runs are saved under
`.kernelevo/runs`; resume from the same project directory. To inspect progress yourself:

```bash
kernel-evo run status --run-id RUN
kernel-evo iter report --run-id RUN --format markdown
```

## Further reading

- [Agent configuration and CLI reference](docs/agent-guide.md)
- [Direct-LLM evolution](docs/direct-llm.md) — API/Redis setup, evaluation server, monitoring, extraction, and memory.
- [OpenCode setup](.opencode/README.md)
- [Build with Docker](build/README.md)
- [Release qualification](docs/release.md)
