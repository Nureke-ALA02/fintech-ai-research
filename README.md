# The Impact of AI Adoption on Employee Productivity and Work Efficiency

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Research](https://img.shields.io/badge/Research-Empirical%20Study-green.svg)](#research-objectives)

**Authors:** Nurkassym Nurdaulet, Tursyn Zhaniya

---

## 1. Project Overview

This project investigates the relationship between the adoption of artificial intelligence (AI) tools and employee productivity and work efficiency in IT companies.

The repository contains a Python-based data processing pipeline, synthetic data generation utilities, feature engineering functions, and a benchmarking framework. These components support the preparation and systematic analysis of data related to AI usage frequency, perceived productivity, perceived efficiency, and task completion time.

The project aims to establish a reproducible research workflow in which data preparation, feature construction, and computational performance measurements can be executed and evaluated consistently.

**Research topic:** The impact of AI adoption on employee productivity and work efficiency.

## 2. Research Objectives

The study focuses on the following research questions:

- **RQ1:** How do employees integrate AI technologies into their daily work processes?
- **RQ2:** What relationship exists between the frequency of AI use and employees' perceived productivity?
- **RQ3:** What relationship exists between the frequency of AI use and employees' perceived work efficiency?

The study examines whether more frequent AI use is associated with higher perceived productivity and work efficiency.

### Research Hypotheses

- **H1:** The frequency of AI use is positively associated with employees' perceived productivity.
- **H2:** The frequency of AI use is positively associated with employees' perceived work efficiency.

These hypotheses require empirical evaluation. Their validity should be determined from the collected research data rather than assumed in advance.

## 3. Methodology

The project follows a structured data analysis workflow.

### 3.1 Data Collection and Preparation

The pipeline supports reading survey data from a CSV file. If the expected raw data file is unavailable, a synthetic dataset can be generated for development and testing purposes.

The preprocessing stage removes rows containing missing values and saves the resulting dataset in CSV format.

### 3.2 Synthetic Data Generation

Synthetic data are generated to test the pipeline before real survey data are available. The generated variables include:

- Employee identifier
- Developer seniority
- Frequency of AI use
- Perceived productivity
- Perceived work efficiency
- Task completion time

Synthetic data are intended for software testing and methodological development. They must not be treated as observations from real employees or used as empirical evidence for the research hypotheses.

### 3.3 Feature Engineering

The feature engineering module derives additional variables from the input dataset:

- `is_heavy_ai_user`: a binary indicator equal to 1 when AI usage frequency is at least 4, and 0 otherwise.
- `perf_efficiency_index`: the arithmetic mean of perceived productivity and perceived work efficiency.

These features support subsequent exploratory analysis and statistical evaluation.

### 3.4 Benchmarking and Reproducibility

The benchmarking framework measures the execution time of selected data processing operations. It separates warm-up runs from measured runs and records execution metadata and success status in JSON Lines (JSONL) format.

The benchmark is intended to support reproducible computational performance evaluation. Its measurements describe software execution time and do not directly measure the effect of AI adoption on employee productivity.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| NumPy | Numerical operations and synthetic data generation |
| Pandas | Tabular data processing and CSV input/output |
| PyYAML | Reading benchmark configuration from YAML |
| Pytest | Automated testing |
| JSONL | Recording individual benchmark measurements |
| Docker | Optional containerized execution, if configured |

## 5. Repository Structure

```text
fintech-ai-research/
├── config.yaml
├── data/
│   ├── raw/
│   │   ├── survey_responses.csv
│   │   └── test_run.jsonl
│   └── processed/
│       └── cleaned_dataset.csv
├── src/
│   ├── data/
│   │   └── data_loader.py
│   ├── features/
│   │   └── build_features.py
│   └── benchmark.py
├── tests/
│   └── test_*.py
├── requirements.txt
├── .gitignore
└── README.md
```

*Note: The structure above describes the intended project layout. Some files, including raw datasets and generated outputs, may not exist until the corresponding workflow has been executed.*

## 6. Installation

### Prerequisites

- Python 3.11 or a compatible Python version
- Git
- pip

### Step 1: Clone the repository

```bash
git clone https://github.com/Nureke-ALA02/fintech-ai-research.git
cd fintech-ai-research
```

### Step 2: Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `requirements.txt` does not include PyYAML, install it separately:

```bash
python -m pip install PyYAML
```

## 7. Usage

Run the following commands from the repository root directory.

### 7.1 Generate Synthetic Data

```bash
python -c "from src.data.data_loader import generate_synthetic_data; print(generate_synthetic_data(n_samples=100).head())"
```

This command generates a synthetic dataset containing 100 records and displays its first five rows.

### 7.2 Preprocess the Dataset

```bash
python -c "from src.data.data_loader import load_and_preprocess_data; load_and_preprocess_data()"
```

The function reads `data/raw/survey_responses.csv` if the file exists. Otherwise, it generates a synthetic dataset. The processed output is saved to `data/processed/cleaned_dataset.csv`.

### 7.3 Build Features

```bash
python -c "from src.data.data_loader import load_and_preprocess_data; from src.features.build_features import build_features; print(build_features(load_and_preprocess_data()).head())"
```

This command prepares the dataset, derives the additional features, and displays the resulting records.

### 7.4 Run the Benchmark

If `src/benchmark.py` and `config.yaml` have been configured as described in the project, execute:

```bash
python -m src.benchmark
```

The benchmark records individual measurements in `data/raw/test_run.jsonl`. The exact number of records depends on the configured operations and number of measured runs.

## 8. Testing

Automated tests are used to verify the main data processing functions and the expected structure of generated features.

Run the test suite with:

```bash
python -m pytest -v
```

The tests cover the following areas:

- Synthetic data generation
- Feature engineering
- Data loading and preprocessing
- Benchmark integration, if an integration test has been implemented

A successful test run indicates that the tested software requirements have passed. It does not, by itself, establish the research hypotheses.

## 9. Benchmarking Protocol

The benchmarking framework is designed to evaluate the execution time of selected computational operations.

The protocol includes:

1. **Configuration:** Define workload size, random seed, warm-up count, and measurement count.
2. **Warm-up:** Execute operations before recording measurements to reduce the influence of initial execution overhead.
3. **Measurement:** Record the duration of each measured execution.
4. **Logging:** Store each measurement as an individual JSON object on a separate line.
5. **Validation:** Check execution success and record error information when available.
6. **Reproducibility:** Preserve relevant execution parameters and environment metadata.

Benchmark results may vary with hardware, operating system, Python version, background processes, and data size. Comparisons should therefore be conducted under documented and consistent conditions.

## 10. Data Management and Research Ethics

The project distinguishes between raw input data, processed datasets, synthetic data, and benchmark outputs.

- Raw survey data should be stored separately from processed data.
- Personal or confidential information must not be committed to a public repository without appropriate authorization and safeguards.
- Synthetic data should be clearly identified in reports and visualizations.
- Data cleaning and transformation procedures should be documented.
- Research findings should be reported transparently, including limitations and results that do not support the hypotheses.

The removal of missing values may introduce bias if missingness is systematic. The preprocessing strategy should therefore be evaluated before drawing substantive conclusions from real survey data.

## 11. Limitations

Several limitations should be considered when interpreting the project outputs:

- Synthetic data cannot establish real-world relationships between AI adoption and employee outcomes.
- Self-reported productivity and efficiency may differ from objectively measured performance.
- Correlation between AI usage frequency and productivity does not establish causation.
- The benchmarking framework evaluates software execution time rather than employee productivity.
- The representativeness and quality of empirical conclusions depend on the sampling strategy, data quality, and statistical methods used.

These limitations should be addressed when interpreting results and preparing the final research report.

## 12. Expected Research Outputs

The intended outputs of the research workflow include:

- A cleaned and documented dataset
- Derived features for exploratory analysis
- Reproducible benchmark logs
- Descriptive statistics and visualizations
- Statistical analyses of the research hypotheses
- A discussion of findings, limitations, and implications

Numerical findings should be added to this README only after the corresponding analyses have been completed and validated.

## 13. Future Work

Potential extensions include:

- Collecting and validating empirical survey data
- Conducting exploratory data analysis
- Evaluating the hypotheses using appropriate statistical tests
- Reporting effect sizes and confidence intervals
- Investigating differences across developer seniority groups
- Extending benchmark summaries with median, p95, and p99 execution times
- Documenting the experimental environment and analysis decisions

## 14. License

This project is distributed under the MIT License, subject to the inclusion of an appropriate `LICENSE` file in the repository.

## 15. Authors

**Nurkassym Nurdaulet**  
**Tursyn Zhaniya**

Research topic: *The Impact of AI Adoption on Employee Productivity and Work Efficiency*.