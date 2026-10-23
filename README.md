# TrendPulse: Python Data Pipeline

End-to-end data pipeline that collects trending stories from the Hacker News API, cleans them, analyzes engagement and visualizes the results.

## Pipeline
| Step | File | What it does |
|------|------|--------------|
| 1 | `task1_data_collection.py` | Fetches top stories via API, assigns 5 categories by keywords, saves JSON |
| 2 | `task2_data_processing.py` | Removes duplicates and nulls, filters low scores, saves clean CSV |
| 3 | `task3_analysis.py` | Pandas + NumPy stats, engagement ratio, popularity flag |
| 4 | `task4_visualization.py` | 3 charts + dashboard (Matplotlib) |

## How to run
```bash
pip install -r requirements.txt
python task1_data_collection.py
python task2_data_processing.py
python task3_analysis.py
python task4_visualization.py
```
Charts are saved in `outputs/`.

## Tech
Python, requests, Pandas, NumPy, Matplotlib

## Output
![Dashboard](outputs/dashboard.png)
