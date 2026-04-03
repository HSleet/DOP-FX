# DOP-FX

A unified pipeline for collecting and normalizing multi-source FX rates for DOP, enabling analysis of spreads, volatility, and market discrepancies.

> **Status**: Phase 1 - Historical data ingestion and daily rate tracking

## Features

- 📊 **Historical Rate Tracking** – Load and maintain historical exchange rate data from the Central Bank
- 🔄 **Daily Updates** – Automated daily rate parsing and database updates
- 🔍 **Historical Queries** – Query exchange rates for any currency on any specific date
- 📈 **Analytics Ready** – Normalized data structure supports analytics workflows
- 💾 **Lightweight** – SQLite database for simple, efficient storage

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Data Models](#data-models)
- [Tech Stack](#tech-stack)
- [Roadmap](#roadmap)

## Project Overview

This project aims to provide a simple, reliable tool for tracking foreign exchange rates against the Dominican Peso. Current capabilities include:

- **Data Source**: Central Bank of the Dominican Republic ([Banco Central](https://www.bancentral.gov.do/a/d/2538)) - provides time series data for multiple rates
- **Query Examples**: "What was the EUR/DOP rate on March 15th?" or "Show me all DOP rates for 2025"
- **Use Cases**: Personal analytics, rate trend observation, historical reference

## Architecture

- **Ingestion Layer** – Fetches and parses FX data from external sources
- **Normalization Layer** – Transforms raw data into structured format
- **Storage Layer** – Persists cleaned data into SQLite

## Data Models

### Source Data Format

The Central Bank provides raw data in a denormalized format with the following columns:

| Año | Mes | Día | DOLAR AUSTRALIANO | REAL BRASILENO | DOLAR CANADIENSE | FRANCO SUIZO | YUAN CHINO | DERECHO ESPECIAL DE GIRO | CORONA DANESA | EURO | LIBRA ESTERLINA | YEN JAPONES | CORONA NORUEGA | LIBRA ESCOCESA | CORONA SUECA | DOLAR ESTADOUNIDENSE |
|-----|-----|-----|--------------------|-----------------|------------------|---------------|-----------|--------------------------|---------------|------|-----------------|--------------|-----------------|-----------------|--------------|------------------------|

### Database Schema

To optimize for analytics, data is normalized into:

- **Dates Table** – Store unique date/time combinations with associated IDs
- **Currencies Table** – Reference table for currency codes and metadata
- **Source** – Store financial entity where the data was extracted from
- **Rates Table** – Main fact table containing:
  - `datetime_id` (foreign key to Dates)
  - `currency_id` (foreign key to Currencies)
  - `source_id` (Foreign key to source)
  - `rate_value` (exchange rate value)
  - `rate_type` (Buy/sell)

This normalized structure enables efficient queries and analytics workflows.

## Tech Stack

- **Language**: Python
- **Database**: SQLite
- **Data Source**: Central Bank (Banco Central)
- **Scheduling**: Daily automated execution
