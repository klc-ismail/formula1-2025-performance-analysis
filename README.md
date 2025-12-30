# Formula 1 2025 Performance Analysis
**Pit Stops • Drivers • Strategy**

This repository contains the complete data pipeline and analysis behind the Medium article:

**Who Really Made the Difference in Formula 1 2025?**  
*A Data-Driven Analysis of Pit Stops, Drivers, and Strategy*

The goal of this project is to identify **where race performance is actually created in Formula 1**, by jointly analyzing pit stop execution, driver contribution, and strategic decision timing using race data from the 2025 season.

---

## Project Overview

Formula 1 performance is often explained through simplified narratives:

- *“It’s the car.”*
- *“It’s the driver.”*
- *“They lost it on the pit wall.”*

This project approaches the problem differently.

Instead of analyzing pit stops, drivers, or strategy in isolation, the analysis connects them **within the same race context** to understand how execution, performance, and timing interact over the course of a race.

The repository is structured around two main layers:

1. **Data pipeline** – collecting and processing raw OpenF1 data  
2. **Analytics layer** – producing the figures and insights used in the article  

---

## Scope of the Analysis

- **Season:** Formula 1 – 2025  
- **Sessions:** Race sessions only  
- **Teams analyzed:**
  - Ferrari  
  - Red Bull Racing  
  - McLaren  
  - Mercedes  
  - Aston Martin  

These teams were selected to represent a mix of front-running and upper-midfield performance while maintaining consistent data coverage across races.

---

## Data Sources

All data used in this project is publicly available.

### Primary Source
- **OpenF1 API**

### Data Included
- Lap-level timing data (clean laps only)
- Pit stop timing and duration
- Stint length and tyre compound information
- Session-level race metadata

Laps affected by pit entry, pit exit, or abnormal conditions are excluded where necessary to focus on representative race pace.

---

## Repository Structure

formula1-2025-performance-analysis/
├── formula1_pipeline/
│ ├── main.py # Pipeline entry point
│ ├── convert_to_raw_to_master.py # Raw OpenF1 → master tables
│ ├── build_analytics_table.py # Analytics-ready datasets
│ ├── modules/
│ │ ├── cache.py
│ │ ├── collector.py
│ │ ├── drivers.py
│ │ ├── races.py
│ │ ├── season.py
│ │ ├── team_filter.py
│ │ └── utils.py
│ └── raw_data/
│ └── 2025/
│ └── <race_id><track_name>/
│ ├── <driver><team>.json
│ ├── drivers.json
│ ├── grid.json
│ ├── race_control.json
│ └── session_result.json
│
├── formula1_analytics/
│ ├── part1_pit_stop_analyze_en.ipynb
│ ├── part2_driver_or_car.ipynb
│ ├── master_laps.csv
│ ├── master_pit.csv
│ ├── master_stints.csv
│ └── master_summary.csv

---

## Pipeline Description

### 1. Data Collection & Normalization
Race-level data is collected from the OpenF1 API and stored under `raw_data/2025/`, organized by race.

Each race directory includes:
- Driver-specific telemetry JSON files  
- Session metadata  
- Grid and race control information  

---

### 2. Master Table Construction
Raw JSON responses are consolidated into four master tables:

- `master_laps.csv` – clean lap-level performance  
- `master_pit.csv` – pit stop timing and duration  
- `master_stints.csv` – stint length and tyre usage  
- `master_summary.csv` – session-level race context  

This structure enables consistent cross-race and cross-team analysis.

---

### 3. Analytics & Visualization
The analytics layer is implemented using Jupyter notebooks:

- **Section 1 – Pit Stops**  
  Distribution-based analysis of pit stop speed, consistency, and strategic impact.

- **Section 2 – Driver vs Car**  
  Teammate comparisons, pace consistency, and tyre degradation profiles.

- **Section 3 – Strategy & Timing**  
  Stint length, pit timing, and post-pit pace outcomes  
  *(integrated into the Medium article)*

Figures generated in these notebooks are used directly in the published article.

---

## Methodological Principles

- Median lap times are used instead of single fastest laps to reduce noise.
- Distributional metrics are preferred over extreme values.
- Teammate comparisons isolate driver contribution while controlling for car performance.
- Strategy is evaluated through **timing effects**, not pit stop count alone.

This project does **not** aim to predict race results.  
Its purpose is to explain **how performance differences emerge**.

---

## Reproducibility

The full pipeline is designed to be reproducible.

To rerun the analysis:
1. Execute the pipeline scripts in `formula1_pipeline/`
2. Generate master tables
3. Run the analytics notebooks in order

The structure can be extended to:
- Additional seasons  
- Different team selections  
- Alternative strategic hypotheses  

---

## Related Article

The full narrative and interpretation of the analysis is available on Medium:

**Who Really Made the Difference in Formula 1 2025?**  
*A Data-Driven Analysis of Pit Stops, Drivers, and Strategy*

*(Medium link to be added)*

---

## License

This project is licensed under the **MIT License**.

---

## Disclaimer

This project is an independent analytical study based on publicly available data.  
It is not affiliated with Formula 1, FIA, or any team.
