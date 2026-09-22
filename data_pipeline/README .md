# Data Pipeline

This module implements a small end-to-end web-scraping and ETL workflow for the Books to Scrape dataset.

It does three main jobs:

- scrapes book metadata from the public site
- cleans and normalizes the scraped values
- loads the curated data into a SQLite database and exports SQL result CSVs

## Project files

- `src/books.py` — the main scraper, cleaning logic, and SQLite loader
- `src/books.db` — SQLite database created by the script
- `src/query1_select_where.csv` — output for query 1
- `src/query2_order_by.csv` — output for query 2
- `src/query3_limit.csv` — output for query 3
- `src/query4_distinct.csv` — output for query 4
- `src/query5_between.csv` — output for query 5
- `src/query6_join.csv` — output for query 6

## Install and run

From the project root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python data_pipeline/src/books.py
```

The script creates the SQLite database at `data_pipeline/src/books.db` and exports each SQL result as a CSV under the same folder.

## Scraping, cleaning, and database-loading flow

The script in `data_pipeline/src/books.py` does the following:

1. Loads the Books to Scrape homepage and discovers category links.
2. Iterates through the first selected catalog categories and follows pagination.
3. Extracts each book's title, displayed price, stock status, and rating.
4. Normalizes values:
   - converts the price string to a numeric `price_gbp`
   - fills missing ratings with the median rating in the dataset
   - calculates `price_inr = price_gbp * 105.50`
   - stores `in_stock` as a boolean-like numeric value for SQLite
5. Creates two SQLite tables:
   - `categories(category_id, category_name)`
   - `books(book_id, title, price_gbp, price_inr, rating, in_stock, category_id)`
6. Inserts category rows and related book rows with a foreign key relation.
7. Executes the required SQL queries and saves the results as CSV files in `data_pipeline/src/`.

## Exact database recreation script

The SQLite database is recreated by the single script below:

```bash
python data_pipeline/src/books.py
```

This script is the authoritative recreation path for the database and query exports. If the database file is deleted, rerunning the script rebuilds it.

## Executed SQL queries and output

The script runs these queries against SQLite and saves the corresponding CSVs.

### Query 1: SELECT with WHERE

```sql
SELECT title, price_gbp
FROM books
WHERE in_stock = 1;
```

Sample output:

```text
title,price_gbp
It's Only the Himalayas,45.17
Full Moon over Noahâs Ark: An Odyssey to Mount Ararat and Beyond,49.43
See America: A Celebration of Our National Parks & Treasured Sites,48.87
A Summer In Europe,44.34
Sharp Objects,47.82
The Murder of Roger Ackroyd (Hercule Poirot #4),44.1
A Time of Torment (Charlie Parker #14),48.35
The Exiled,43.45
Glory over Everything: Beyond The Kitchen House,45.84
The Guernsey Literary and Potato Peel Pie Society,49.53
```

### Query 2: ORDER BY

```sql
SELECT title, rating
FROM books
ORDER BY rating DESC;
```

Sample output:

```text
title,rating
"1,000 Places to See Before You Die",5
A Time of Torment (Charlie Parker #14),5
What Happened on Beale Street (Secrets of the South Mysteries #2),5
The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1),5
The Silkworm (Cormoran Strike #2),5
The Girl You Lost,5
A Flight of Arrows (The Pathfinders #2),5
Mrs. Houdini,5
The Passion of Dolssa,5
Voyager (Outlander #3),5
```

### Query 3: LIMIT

```sql
SELECT title, rating
FROM books
ORDER BY rating DESC
LIMIT 10;
```

Sample output:

```text
title,rating
"1,000 Places to See Before You Die",5
A Time of Torment (Charlie Parker #14),5
What Happened on Beale Street (Secrets of the South Mysteries #2),5
The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1),5
The Silkworm (Cormoran Strike #2),5
The Girl You Lost,5
A Flight of Arrows (The Pathfinders #2),5
Mrs. Houdini,5
The Passion of Dolssa,5
Voyager (Outlander #3),5
```

### Query 4: DISTINCT

```sql
SELECT DISTINCT category_name
FROM categories;
```

Output:

```text
category_name
Historical Fiction
Mystery
Travel
```

### Query 5: BETWEEN

```sql
SELECT title, price_gbp
FROM books
WHERE price_gbp BETWEEN 40 AND 50;
```

Sample output:

```text
title,price_gbp
It's Only the Himalayas,45.17
Full Moon over Noahâs Ark: An Odyssey to Mount Ararat and Beyond,49.43
See America: A Celebration of Our National Parks & Treasured Sites,48.87
A Summer In Europe,44.34
Sharp Objects,47.82
The Murder of Roger Ackroyd (Hercule Poirot #4),44.1
A Time of Torment (Charlie Parker #14),48.35
The Exiled,43.45
Glory over Everything: Beyond The Kitchen House,45.84
The Guernsey Literary and Potato Peel Pie Society,49.53
```

### Query 6: JOIN

```sql
SELECT books.title, books.price_inr, books.rating, categories.category_name
FROM books
JOIN categories ON books.category_id = categories.category_id;
```

Sample output:

```text
title,price_inr,rating,category_name
It's Only the Himalayas,4765.435,2,Travel
Full Moon over Noahâs Ark: An Odyssey to Mount Ararat and Beyond,5214.865,4,Travel
See America: A Celebration of Our National Parks & Treasured Sites,5155.785,3,Travel
Vagabonding: An Uncommon Guide to the Art of Long-Term World Travel,3897.1699999999996,2,Travel
Under the Tuscan Sun,3938.3149999999996,3,Travel
A Summer In Europe,4677.870000000001,2,Travel
The Great Railway Bazaar,3221.97,1,Travel
A Year in Provence (Provence #1),6000.84,4,Travel
The Road to Little Dribbling: Adventures of an American in Britain (Notes From a Small Island #2),2448.655,1,Travel
Neither Here nor There: Travels in Europe,4109.225,3,Travel
```

## Design decisions

- The scraper keeps the ETL simple and deterministic by scraping a fixed set of categories and following pagination within those pages.
- Data cleaning is intentionally lightweight: missing values are filled with sensible defaults, and prices are normalized before database insertion.
- A two-table SQLite design keeps the data normalized and enables joins between `books` and `categories`.
- Query results are exported to CSV for easy inspection and later use in analytics or reporting.
- The project keeps all generated artifacts in `data_pipeline/src/` so the database and SQL outputs are reproducible from the script alone.

## Notes

This implementation is a small demonstration pipeline rather than a production crawler. It is intended to be easy to run and easy to inspect, with the database and query outputs stored alongside the source script for transparency.
