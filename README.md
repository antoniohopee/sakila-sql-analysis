# Sakila SQL Analysis

SQL and Python analysis project based on the Sakila SQLite database. The goal is to extract business KPIs, explore rental behavior, generate reusable query outputs, and support a final business presentation.

## Project Overview

This project analyzes a DVD rental business using the Sakila sample database. The analysis focuses on revenue, monthly performance, customer value, geographic performance, store performance, film/category performance, actors, ratings, languages, and genre preferences by country.

The workflow is:

1. Download the Sakila SQLite database.
2. Inspect the schema and key table relationships.
3. Run SQL queries saved in `queries/`.
4. Explore results in the Jupyter notebook.
5. Export CSV outputs and PNG charts.
6. Use the results in the final presentation.

## Repository Structure

```text
sakila-sql-analysis/
├── data/
│   └── sakila.db
├── notebooks/
│   └── sakila_analysis.ipynb
├── outputs/
│   ├── *.csv
│   └── img/
│       └── *.png
├── presentation/
│   └── Sakila_Business_Data_Analysis.pdf
├── queries/
│   ├── 01_core_kpis.sql
│   ├── 02_monthly_revenue.sql
│   ├── 03_top_films_by_revenue.sql
│   ├── 04_top_countries_by_revenue.sql
│   ├── 05_top_categories_world.sql
│   ├── 06_top_customers.sql
│   ├── 07_store_performance.sql
│   ├── 08_rating_distribution.sql
│   ├── 09_top_3_genres_per_country.sql
│   ├── 10_top_genre_per_country.sql
│   ├── 11_top_actors.sql
│   ├── 12_film_length_performance.sql
│   └── 13_top_languages.sql
├── scripts/
│   ├── download_db.py
│   ├── export_outputs.py
│   └── inspect_db.py
├── README.md
└── requirements.txt
```

## Setup Instructions

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Download The Database

Download the SQLite database with:

```bash
python scripts/download_db.py
```

The database is saved as:

```text
data/sakila.db
```

The notebook also checks for this file during setup and runs the download script automatically if the database is missing.

To inspect available tables:

```bash
python scripts/inspect_db.py
```

## Run The Notebook

Start Jupyter:

```bash
jupyter notebook
```

Then open:

```text
notebooks/sakila_analysis.ipynb
```

The notebook loads the SQL files from `queries/`, displays result tables, creates charts, and exports analysis outputs.

To execute the notebook from the command line:

```bash
jupyter nbconvert --to notebook --execute notebooks/sakila_analysis.ipynb --output-dir /tmp
```

## Export Outputs

Regenerate all CSV files and chart images with:

```bash
python scripts/export_outputs.py
```

CSV files are written to `outputs/`. Chart images are written to `outputs/img/` as PNG files.

CSV outputs are ignored by Git because they are generated artifacts. PNG charts are tracked for presentation and README use.

## Key KPIs

| KPI | Value |
| --- | ---: |
| Total revenue | 67,416.51 |
| Total payments | 16,049 |
| Unique customers | 599 |
| Average payment | 4.20 |

Additional highlights:

- Best month by revenue: `2005-07` with `28,373.89`.
- Top category by revenue: `Sports` with `5,314.21`.
- Top country by revenue: `India` with `6,628.28`.
- Top store by revenue: Store `2` with `33,927.04`.

## Business Insights Summary

- Revenue is concentrated in July and August 2005, suggesting strong seasonal demand in the dataset.
- India, China, and the United States are the strongest revenue markets.
- Sports, Sci-Fi, and Animation are the top categories by revenue.
- Store performance is balanced, with Store 2 slightly ahead of Store 1.
- Customer value is concentrated among a small group of high-spend customers.
- English is the only language with films and revenue in this Sakila SQLite dataset.

## Final Presentation

Final business presentation:

[Sakila Business Data Analysis](presentation/Sakila_Business_Data_Analysis.pdf)

## Tools Used

- SQL
- SQLite
- Python
- pandas
- matplotlib
- Jupyter Notebook
- Git / GitHub

## Author

Antonio Hopee

## Tags

`sql` `sqlite` `python` `pandas` `matplotlib` `jupyter` `business-analysis` `data-analysis` `sakila`
