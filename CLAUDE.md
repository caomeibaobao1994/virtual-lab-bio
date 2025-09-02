# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Virtual Lab is an AI-human collaboration platform for scientific research. It enables human researchers to work with teams of large language model (LLM) agents through team meetings (multi-agent discussions) and individual meetings (one-on-one interactions). The project includes a real-world application for nanobody design against SARS-CoV-2.

## Development Commands

This project uses Python packaging with hatchling as the build backend.

### Installation
```bash
# Create conda environment (optional but recommended)
conda create -y -n virtual_lab python=3.12
conda activate virtual_lab

# Install package (development mode)
pip install -e .

# Install with nanobody design dependencies
pip install -e .[nanobody-design]

# Or install frozen requirements for nanobody design
pip install -r nanobody_design/requirements_nanobody_design_frozen.txt
```

### Environment Setup
Set your OpenAI API key:
```bash
export OPENAI_API_KEY=<your_key>
```

### Running the Application
- Main notebook example: `nanobody_design/run_nanobody_design.ipynb`
- Human evaluation: `nanobody_design/human_eval.ipynb`
- Results analysis: `nanobody_design/plot_results.ipynb`

## Code Architecture

### Core Components

**src/virtual_lab/**: Main package
- `agent.py`: LLM agent class with title, expertise, goal, role, and model properties
- `run_meeting.py`: Core meeting orchestration for team and individual meetings
- `prompts.py`: System prompts for different agent types and meeting contexts
- `constants.py`: Configuration constants including temperatures and tool descriptions
- `utils.py`: Utilities for message handling, token counting, cost calculation, and file I/O

**Meeting Types**:
- **Team meetings**: Multi-agent discussions with team lead + team members
- **Individual meetings**: One-on-one with agent + scientific critic

### Key Workflows

**Meeting Execution Pattern**:
1. Agent creation with specialized expertise/roles
2. Meeting setup (team vs individual)
3. Multi-round discussions with OpenAI Assistants API
4. Tool integration (PubMed search when enabled)
5. Discussion saving (JSON + Markdown formats)
6. Summary generation and token/cost tracking

**Nanobody Design Pipeline**:
1. Team selection → Project specification → Tools selection
2. Implementation: ESM (mutations) → AlphaFold-Multimer (structure) → Rosetta (binding energy)
3. Workflow design with iterative improvement process
4. Experimental validation of designed nanobodies

### Agent Types
- Principal Investigator (project leadership)
- Machine Learning Specialist (ESM implementation)
- Computational Biologist (AlphaFold/Rosetta)
- Scientific Critic (peer review in individual meetings)
- Domain-specific agents with fine-tuned expertise

### Data Organization
- Discussion results stored as both JSON and Markdown
- Experimental data in CSV format
- Figures generated using matplotlib/seaborn
- Concurrent execution for multiple discussion iterations
- Proper summary merging across discussion rounds

## Important Notes

- Requires OpenAI API access (GPT-4o)
- Uses OpenAI Assistants API with tools integration
- Discussions are automatically saved with token counting and cost tracking
- Built-in PubMed search tool support
- Temperature controls for creative vs consistent outputs
- Designed for scientific research collaboration workflows