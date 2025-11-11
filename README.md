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

`chess-insights-pipeline` collects chess games (e.g., from the Lichess API or local PGN files),  
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
chess-insights-pipeline/
├── README.md
├── pyproject.toml          # Poetry configuration
├── docker-compose.yml
├── Dockerfile
├── .env.example            # environment variables example
└── src/
    └── chess_insights/
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
