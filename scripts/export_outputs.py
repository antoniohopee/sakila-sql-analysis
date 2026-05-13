from pathlib import Path
import sqlite3

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "data" / "sakila.db"
QUERIES_DIR = ROOT_DIR / "queries"
OUTPUTS_DIR = ROOT_DIR / "outputs"
IMG_DIR = OUTPUTS_DIR / "img"

TEAL = "#18b7a6"
TEXT_COLOR = "#061832"
GRID_COLOR = "#c9c9c9"
BORDER_COLOR = "#e1e4ea"

QUERY_OUTPUTS = {
    "01_core_kpis.sql": "core_kpis.csv",
    "02_monthly_revenue.sql": "monthly_revenue.csv",
    "03_top_films_by_revenue.sql": "top_films_by_revenue.csv",
    "04_top_countries_by_revenue.sql": "top_countries_by_revenue.csv",
    "05_top_categories_world.sql": "top_categories_world.csv",
    "06_top_customers.sql": "top_customers.csv",
    "07_store_performance.sql": "store_performance.csv",
    "08_rating_distribution.sql": "rating_distribution.csv",
    "09_top_3_genres_per_country.sql": "top_3_genres_per_country.csv",
    "10_top_genre_per_country.sql": "top_genre_per_country.csv",
    "11_top_actors.sql": "top_actors.csv",
    "12_film_length_performance.sql": "film_length_performance.csv",
    "13_top_languages.sql": "top_languages.csv",
}


def format_euro(value: float) -> str:
    return f"EUR {value:,.0f}".replace(",", ".")


def create_chart_card(title: str, horizontal: bool = False):
    fig = plt.figure(figsize=(12, 7), dpi=150)
    fig.patch.set_facecolor("white")

    card = FancyBboxPatch(
        (0.03, 0.05),
        0.94,
        0.88,
        boxstyle="round,pad=0.02,rounding_size=0.07",
        transform=fig.transFigure,
        facecolor="white",
        edgecolor=BORDER_COLOR,
        linewidth=1.2,
        zorder=0,
    )
    fig.add_artist(card)
    fig.text(0.08, 0.85, title, fontsize=12, fontweight="bold", color=TEXT_COLOR)

    left = 0.34 if horizontal else 0.16
    ax = fig.add_axes([left, 0.17, 0.89 - left, 0.60], zorder=1)
    ax.set_facecolor("white")
    ax.grid(axis="x" if horizontal else "y", color=GRID_COLOR, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#9a9a9a")
    ax.tick_params(axis="both", length=0, labelsize=7)
    return fig, ax


def save_png(fig, filename: str) -> None:
    fig.savefig(IMG_DIR / filename, dpi=150)
    plt.close(fig)


def plot_vertical_bars(data, x, y, title, filename, currency=False):
    fig, ax = create_chart_card(title)
    ax.bar(data[x].astype(str), data[y], color=TEAL, width=0.5)
    if currency:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda value, _: format_euro(value)))
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    save_png(fig, filename)


def plot_horizontal_bars(data, x, y, title, filename, currency=False):
    chart_data = data.sort_values(y, ascending=True)
    fig, ax = create_chart_card(title, horizontal=True)
    ax.barh(chart_data[x], chart_data[y], color=TEAL, height=0.58)
    if currency:
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda value, _: format_euro(value)))
    ax.set_xlabel("")
    ax.set_ylabel("")
    save_png(fig, filename)


def plot_line(data, x, y, title, filename, currency=False):
    fig, ax = create_chart_card(title)
    ax.plot(data[x], data[y], color=TEAL, linewidth=2, marker="s", markersize=7)
    if currency:
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda value, _: format_euro(value)))
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    save_png(fig, filename)


def plot_kpi_cards(data, filename):
    row = data.iloc[0]
    metrics = [
        ("Fatturato", format_euro(row["total_revenue"])),
        ("Pagamenti", f"{row['total_payments']:,.0f}".replace(",", ".")),
        ("Clienti", f"{row['unique_customers']:,.0f}".replace(",", ".")),
        ("Ticket", f"EUR {row['avg_payment']:.2f}"),
    ]

    fig = plt.figure(figsize=(12, 7), dpi=150)
    fig.patch.set_facecolor("white")
    card = FancyBboxPatch(
        (0.03, 0.05),
        0.94,
        0.88,
        boxstyle="round,pad=0.02,rounding_size=0.07",
        transform=fig.transFigure,
        facecolor="white",
        edgecolor=BORDER_COLOR,
        linewidth=1.2,
    )
    fig.add_artist(card)
    fig.text(0.08, 0.85, "KPI principali", fontsize=12, fontweight="bold", color=TEXT_COLOR)

    for index, (label, value) in enumerate(metrics):
        x_pos = 0.10 + (index % 2) * 0.42
        y_pos = 0.52 - (index // 2) * 0.26
        metric_box = FancyBboxPatch(
            (x_pos, y_pos),
            0.32,
            0.16,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            transform=fig.transFigure,
            facecolor=TEAL,
            edgecolor=TEAL,
        )
        fig.add_artist(metric_box)
        fig.text(x_pos + 0.16, y_pos + 0.10, value, ha="center", fontsize=10, fontweight="bold", color="white")
        fig.text(x_pos + 0.16, y_pos + 0.04, label, ha="center", fontsize=8, color="white")

    save_png(fig, filename)


def export_dataframes() -> dict[str, pd.DataFrame]:
    OUTPUTS_DIR.mkdir(exist_ok=True)
    IMG_DIR.mkdir(exist_ok=True)

    dataframes = {}
    with sqlite3.connect(DB_PATH) as conn:
        for query_file, output_file in QUERY_OUTPUTS.items():
            dataframe = pd.read_sql_query((QUERIES_DIR / query_file).read_text(), conn)
            dataframe.to_csv(OUTPUTS_DIR / output_file, index=False)
            dataframes[output_file.removesuffix(".csv")] = dataframe

    return dataframes


def export_images(dataframes: dict[str, pd.DataFrame]) -> None:
    table_counts = pd.DataFrame(
        {
            "table_name": ["payment", "rental", "inventory", "film", "customer", "actor", "store"],
            "rows": [16049, 16044, 4581, 1000, 599, 200, 2],
        }
    )
    plot_horizontal_bars(
        table_counts,
        "table_name",
        "rows",
        "Righe per tabella",
        "table_counts.png",
    )
    plot_kpi_cards(dataframes["core_kpis"], "core_kpis.png")
    plot_line(
        dataframes["monthly_revenue"],
        "month",
        "revenue",
        "Fatturato per mese",
        "monthly_revenue.png",
        currency=True,
    )
    plot_horizontal_bars(
        dataframes["top_films_by_revenue"],
        "film",
        "revenue",
        "Top film per fatturato",
        "top_films_by_revenue.png",
        currency=True,
    )
    plot_horizontal_bars(
        dataframes["top_countries_by_revenue"],
        "country",
        "revenue",
        "Top paesi per fatturato",
        "top_countries_by_revenue.png",
        currency=True,
    )
    plot_horizontal_bars(
        dataframes["top_categories_world"].head(10),
        "category",
        "revenue",
        "Top categorie per fatturato",
        "top_categories_world.png",
        currency=True,
    )
    plot_horizontal_bars(
        dataframes["top_customers"],
        "customer",
        "amount_spent",
        "Top clienti per spesa",
        "top_customers.png",
        currency=True,
    )
    plot_vertical_bars(
        dataframes["store_performance"],
        "store_id",
        "revenue",
        "Fatturato per store",
        "store_performance.png",
        currency=True,
    )
    plot_vertical_bars(
        dataframes["rating_distribution"],
        "rating",
        "pct_films",
        "Distribuzione rating",
        "rating_distribution.png",
    )

    top_3_category_totals = (
        dataframes["top_3_genres_per_country"]
        .groupby("category", as_index=False)["rentals"]
        .sum()
        .sort_values("rentals", ascending=False)
        .head(10)
    )
    plot_horizontal_bars(
        top_3_category_totals,
        "category",
        "rentals",
        "Categorie top 3",
        "top_3_genres_per_country.png",
    )

    top_genre_counts = (
        dataframes["top_genre_per_country"]
        .groupby("top_category", as_index=False)["country"]
        .count()
        .rename(columns={"country": "countries"})
        .sort_values("countries", ascending=False)
    )
    plot_horizontal_bars(
        top_genre_counts.head(10),
        "top_category",
        "countries",
        "Categorie leader",
        "top_genre_per_country.png",
    )
    plot_horizontal_bars(
        dataframes["top_actors"],
        "actor",
        "rentals",
        "Top attori per noleggi",
        "top_actors.png",
    )
    plot_horizontal_bars(
        dataframes["film_length_performance"],
        "film",
        "rentals",
        "Film piu noleggiati",
        "film_length_performance.png",
    )
    plot_vertical_bars(
        dataframes["top_languages"],
        "language",
        "revenue",
        "Fatturato per lingua",
        "top_languages.png",
        currency=True,
    )


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}. Run scripts/download_db.py first.")

    dataframes = export_dataframes()
    export_images(dataframes)
    print(f"Exported {len(QUERY_OUTPUTS)} CSV files to {OUTPUTS_DIR}")
    print(f"Exported PNG charts to {IMG_DIR}")


if __name__ == "__main__":
    main()
