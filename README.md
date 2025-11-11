# Chess Insights Pipeline

A **data processing and analytics pipeline** for chess games, built with a production-grade Python stack  
(**Pandas, Redis, MySQL, Docker, Poetry, Pytest, Mypy**).

This project is designed as a small but realistic example of how I would approach  
building a data/ML infrastructure for chess data — from game ingestion and transformation  
to analytics, caching, and persistent storage.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Tech Stack](#tech-stack)
4. [Features](#features)
5. [Project Structure](#project-structure)
6. [Getting Started](#getting-started)
7. [Usage](#usage)
8. [Testing & Quality](#testing--quality)
9. [Design Decisions](#design-decisions)
10. [Future Work](#future-work)

---

## Project Overview

**Goal**

`chess-insights` collects chess games (e.g., from the Lichess API or local PGN files),  
transforms them into a tabular format using **Pandas**, and computes key metrics such as:

- average game length
- win percentage by color
- most common openings
- statistical summary for a selected player

Results are stored in a **MySQL** database, while **Redis** acts as a cache layer  
for frequently accessed analytics results.

**Why this project?**

It was created to demonstrate:

- an **industry-level Python development approach** (type hints, static analysis, testing)
- practical experience in **data pipelines** (ingest → transform → store → cache)
- understanding of **software architecture and design patterns**
- combining **software engineering with chess data analytics**

---

## Architecture

The pipeline consists of five main stages:

1. **Ingestion** – Load chess games from a PGN file or API
2. **Transformation** – Parse and structure the data using `python-chess` and `Pandas`
3. **Analytics** – Compute metrics (win rate, draws, move count, openings, etc.)
4. **Storage & Caching** – Store analytics in MySQL and cache in Redis
5. **CLI / Script** – Command-line interface to run the entire pipeline

**Logical code layers:**

- `data/` – ingestion and transformation
- `core/` – analytics and business logic
- `storage/` – database and cache clients
- `cli/` – entry point for execution
- `tests/` – Pytest unit tests and quality checks

---

## Tech Stack

**Core**

- Python 3.11+
- Type hints + static analysis (`mypy`)
- Testing: `pytest`

**Data Processing**

- `pandas` – tabular data processing
- `python-chess` – PGN parsing

**Infrastructure**

- **MySQL** – persistent database
- **Redis** – caching layer
- **Docker & Docker Compose** – service orchestration
- **Poetry** – dependency management

**Other**

- **Git & GitHub** – version control
- **Unix shell / CLI** – script execution and automation

---

## Features

- [x] Load chess games from PGN files
- [x] Parse and transform games into structured data
- [x] Compute analytics:
  - total number of games
  - win/draw/loss rates
  - average number of moves
- [x] Store analytics results in MySQL
- [x] Cache frequent queries in Redis
- [x] Command-line interface for running the pipeline
- [x] Unit tests with Pytest and static type checking with Mypy

---

## Project Structure

```bash
chess-insights/
├── README.md
├── pyproject.toml          # Poetry configuration
├── docker-compose.yml
├── Dockerfile
├── .env.example            # environment variables example
└── src/
    └── insights/
        ├── __init__.py
        ├── cli/
        │   └── main.py
        ├── data/
        │   ├── ingest.py
        │   └── transform.py
        ├── core/
        │   └── analytics.py
        └── storage/
            ├── mysql_client.py
            └── redis_client.py
tests/
    ├── test_ingest.py
    ├── test_transform.py
    └── test_analytics.py
```

---

## Getting Started

**Prerequisites**

- Python 3.11
- Docker & Docker Compose
- Poetry (`pip install poetry`)

**1. Clone the repository**

```
git clone https://github.com/miksipiksic/chess-insights.git
cd chess-insights
```

**2. Install dependencies**

```bash
pip install poetry
```

**3. Configure environment variables**

```env
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_USER=chess
MYSQL_PASSWORD=chesspass
MYSQL_DB=chess_insights

REDIS_HOST=redis
REDIS_PORT=6379
```

**4. Start services (MySQL & Redis)**

```
docker compose up -d
```

**5. Activate Poetry shell**

```
poetry shell
```

---

## Usage

**1. Load and analyze PGN games**

```
python -m chess_insights.cli.main \
    --pgn-path data/sample_games.pgn \
    --player "Milena" \
    --store-in-mysql \
    --use-redis-cache
```

This will:

1. Load games from PGN

2. Parse and convert them to a Pandas DataFrame

3. Compute statistics for the selected player

4. Store results in MySQL

5. Cache analytics in Redis

**2. Run analytics only (with Redis cache)**

```
python -m chess_insights.cli.main \
    --player "Milena" \
    --only-analytics \
    --use-redis-cache
```

If the result exists in Redis, it will be loaded directly from cache.
Otherwise, it will be computed and stored for future use.

---

## Testing & Quality

Run tests:

```
pytest
```

Run static analysis:

```
mypy src/insights
```

All modules should pass without Mypy errors and include full type hints.

---

## Design Decisions

**Clear modular structure**

Each layer is responsible for a single concern:

- `data/` -> ingestion and transformation
- `core/` -> analytics
- `storage/` -> infrastructure (MySQL, Redis)
- `cli/` -> user interface

**Redis caching**

Expensive analytics queries are cached for performance.

**MySQL storage**

Normalized schema ensures persistence and flexibility for advanced querying.

**Type hints & Mypy**

Strict typing improves readability and reliability.

**Pytest coverage**

Key modules (parsing, analytics, transformation) are unit tested to ensure stability.

---

## Future Work

- Integration with Chess.com APIs

- Advanced analytics (performance by opening, time control, rating range)

- Machine learning component for result prediction

- REST API (FastAPI) for serving analytics

- Web dashboard for data visualization
