# Fetal Health CTG Analysis — Interactive Visualization

An interactive data visualization dashboard for exploring cardiotocography (CTG) examination data, built with Streamlit and Altair. Created as part of the IB031 Introduction to Machine Learning course (Homework 1).

---

## Getting Started

### Prerequisites

Make sure you have the following Python packages installed:

```bash
pip install streamlit pandas altair
```

### Running the App

To run the app from the repository root, use:

```bash
streamlit run HW01/app.py
```

To run from the HW01 directory, use:

```bash
streamlit run app.py
```

The app will open automatically in your default browser at `http://localhost:8501`.

---

## Dataset

**Location:** `dataset/fetal_health.csv`  
**Source:** Cardiotocography (CTG) examination records  
**Size:** 2,126 records, 23 features (semicolon-delimited)

Each row represents one CTG examination. Key features include:

| Feature | Description |
|---|---|
| `baseline value` | Baseline fetal heart rate (bpm) |
| `accelerations` | Number of accelerations per second |
| `fetal_movement` | Number of fetal movements per second |
| `uterine_contractions` | Number of uterine contractions per second |
| `abnormal_short_term_variability` | % of time with abnormal short-term variability |
| `fetal_health` | **Target label** — `1` Normal, `2` Suspect, `3` Pathological |

---

## Dashboard Overview

The dashboard consists of **4 linked interactive charts**:

### 1. Accelerations vs Fetal Movement *(scatter plot)*
Shows the relationship between acceleration frequency and fetal movement. Click and drag to select a region — this filters all other charts.

### 2. Health Category Counts *(bar chart)*
Displays the number of examinations per health category. Updates dynamically based on selections made in the other charts.

### 3. Fetal Movement vs Baseline FHR *(scatter plot)*
Explores the relationship between fetal movement and baseline heart rate. Has its own independent brush selection.

### 4. Acceleration Distribution *(strip plot)*
Shows the spread of acceleration values across health categories. Black tick marks indicate the current mean for each group — these update live as selections change.

---

## Interactivity

All four charts are **cross-linked**:

- **Brush selection** — click and drag in any scatter/strip plot to highlight a subset of data points
- **Legend filtering** — click a health category in the legend to isolate it across all charts
- **Combined filtering** — selections from multiple charts stack together; only points satisfying all active selections are highlighted
- **Zooming** — select an area and use the scroll wheel to zoom in or out
- Unselected points turn light gray, keeping the full data context visible

---

## Health Categories

| Label | Category | Color |
|---|---|---|
| 1 | Normal | 🟢 Green |
| 2 | Suspect | 🟡 Orange |
| 3 | Pathological | 🔴 Red |

---

## Project Structure

```
.
├── dataset/
│   ├── description.txt
│   └── fetal_health.csv
└── HW01/
	 ├── app.py
	 ├── requirements.txt
	 └── README.md
```

---

## Course Context

This visualization was developed as **Homework 1** for *IB031 — Introduction to Machine Learning*. The assignment required building an interactive visualization with at least two linked chart types, supporting zoom/pan and cross-filtering between charts.
