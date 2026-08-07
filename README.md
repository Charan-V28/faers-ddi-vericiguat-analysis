# Real-World FAERS Safety Signal Analysis: Vericiguat Drug-Drug Interactions

This repository contains an end-to-end data pipeline to ingest, process, and analyze post-marketing adverse event reports from the **FDA Adverse Event Reporting System (FAERS)**. The project evaluates real-world safety signals and potential drug-drug interactions (DDIs) between **Vericiguat (Verquvo)** and concomitant cardiovascular medications in heart failure patients.

---

## 📌 Project Overview

* **Target Drug:** Vericiguat (`VERQUVO`, `VERICIGUAT`)
* **Primary Adverse Event:** Hypotension
* **Co-administered Drugs Analyzed:** Sacubitril/Valsartan (`ENTRESTO`), Furosemide, Spironolactone, Bisoprolol, Empagliflozin (`JARDIANCE`).
* **Key Finding:** A statistically significant disproportionality signal was detected for **Vericiguat + Sacubitril/Valsartan (Entresto)** regarding Hypotension ($\text{ROR} = 2.606$, $95\%\text{ CI: }[1.222, 5.555]$, $\chi^2 = 5.459$, $p = 0.0195$).

---

## 📁 Repository Structure

```text
├── data/
│   ├── raw/                 # Raw FAERS quarterly extract files (ASCII / TXT)
│   └── processed/           # Filtered case datasets and output CSV summaries
│       ├── etripamil_drugs.csv
│       ├── etripamil_reactions.csv
│       ├── ddi_signals_summary.csv
│       └── forest_plot_ror.png
├── src/
│   ├── ingestion.py         # Pipeline to identify target cases and extract concomitant records
│   ├── statistics.py        # 2x2 contingency table calculations (ROR, PRR, Chi-Square)
│   └── visualization.py     # Script to generate Forest Plots for disproportionality signals
├── REPORT.md                # Comprehensive Results and Discussion markdown report
├── .gitignore               # Git ignore rule file
└── README.md                # Project documentation

```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.9+
* Required libraries: `pandas`, `numpy`, `scipy`, `matplotlib`

### Installation

1. **Clone the repository:**
```bash
git clone [https://github.com/Charan-V28/faers-ddi-vericiguat-analysis.git](https://github.com/Charan-V28/faers-ddi-vericiguat-analysis.git)
cd faers-ddi-vericiguat-analysis

```


2. **Set up a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate        # On macOS/Linux
venv\Scripts\activate           # On Windows

```


3. **Install dependencies:**
```bash
pip install pandas numpy scipy matplotlib

```
---

## ⚙️ Running the Pipeline

### Step 1: Data Ingestion

Extracts target case IDs matching Vericiguat and pulls all concomitant drug and reaction records:

```bash
python src/ingestion.py

```

### Step 2: Statistical Disproportionality Screening

Constructs $2 \times 2$ contingency tables for top co-administered cardiovascular medications and exports summary metrics to `data/processed/ddi_signals_summary.csv`:

```bash
python src/statistics.py

```

### Step 3: Visualization

Generates a publication-ready Forest Plot saved to `data/processed/forest_plot_ror.png`:

```bash
python src/visualization.py

```

---

## 📊 Summary Results

| Concomitant Drug | $a$ (Pair + AE) | $b$ (Pair - AE) | ROR | 95% CI | $\chi^2$ | Signal Detected |
| --- | --- | --- | --- | --- | --- | --- |
| **Entresto / Sacubitril** | 15 | 68 | **2.606** | **[1.222, 5.555]** | **5.459** | **True** |
| **Furosemide** | 11 | 70 | 1.050 | [0.470, 2.345] | 0.012 | False |
| **Spironolactone** | 7 | 46 | 0.980 | [0.380, 2.520] | 0.001 | False |
| **Bisoprolol** | 5 | 34 | 0.920 | [0.310, 2.730] | 0.020 | False |
| **Jardiance / Empagliflozin** | 4 | 27 | 0.890 | [0.260, 3.040] | 0.040 | False |

---

## 📈 Visualizations

---

## 📄 Full Report

For a detailed analysis covering pharmacological mechanisms, clinical implications, and study limitations, read the complete [REPORT.md](REPORT.md).

```

```
