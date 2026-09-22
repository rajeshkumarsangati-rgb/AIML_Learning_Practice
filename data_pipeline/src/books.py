import os
import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
folder = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(folder, "books.db")


base_url = "http://books.toscrape.com/"
response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")
#print(soup.prettify()[:30000])

book_categories = soup.find("div", class_="side_categories").find_all("a")
book_main=[]
for category in book_categories[1:5]:
    category_name = category.text.strip()
    category_url = category["href"]
    book_main.append({"category_name": category_name, "category_url": category_url})
   # print(f"Category: {category_name}, URL: {category_url}")

all_books = []
for book_cat in book_main[:3]:
    category_name = book_cat["category_name"]
    category_url = book_cat["category_url"]
    next_page = base_url + category_url
    #print(next_page)
    while next_page:
        response = requests.get(next_page)
        # print(response.url)
        books_data = BeautifulSoup(response.text, "html.parser")
        books = books_data.find_all("article", class_="product_pod")
        for book in books:
            try:
                title = book.find("h3").find("a")["title"]
            except Exception:
                title = None
            try:
                price = float(book.find("p", class_="price_color").text.strip().replace("Â£", ""))
            except Exception:
                price = None
            try:
                in_stock = book.find("p", class_="instock availability").text.strip()
            except Exception:
                in_stock = None
            try:
                rating = book.find("p", class_="star-rating")
                rating = rating["class"][1]
                rating_map = {
                                "One": 1,
                                "Two": 2,
                                "Three": 3,
                                "Four": 4,
                                "Five": 5
                            }

                rating = rating_map[rating]
            except Exception:
                rating = None            
            all_books.append({
                "category": category_name,
                "title": title,
                "price": price,
                "in_stock": in_stock,
                "rating": rating
            })
        next_button = books_data.find("li", class_="next")
        # print(next_button)
        if next_button:
            next_page = base_url + category_url.rsplit('/', 1)[0] + '/' + next_button.find("a")["href"]
        else:
            next_page = None

df = pd.DataFrame(all_books)
# df["price_gbp"] = df["price"].str.replace("Â£", "").astype(float)
if "price_gbp" in df:
    df["price_gbp"] = pd.to_numeric(df["price_gbp"], errors="coerce")
    df["price_gbp"].fillna(df["price_gbp"].median(), inplace=True)
else:
    # create with a default or raise a clear error
    df["price_gbp"] = 0.0
#df["price_inr"]=df["price_gbp"].fillna(df["price_gbp"].median())
df["in_stock"]=df["in_stock"].astype(bool)
df["rating"]=df["rating"].fillna(df["rating"].median())

print(len(all_books))

conversion_rate = 105.50

df["price_inr"] = df["price_gbp"] * conversion_rate

print(df.head())

# ensure `category_name` exists (some scrapers use `category`)
if "category_name" not in df.columns and "category" in df.columns:
    df["category_name"] = df["category"]
if "category_name" not in df.columns:
    raise KeyError("DataFrame missing 'category_name' column")

categories_df = df[["category_name"]].drop_duplicates()

categories_df["category_id"] = range(1, len(categories_df) + 1)

print(categories_df.head())

df = df.merge(categories_df, on="category_name", how="left")

print(df.dtypes)

connection = sqlite3.connect(db_path)

cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories(
    category_id INTEGER PRIMARY KEY,
    category_name TEXT UNIQUE)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    in_stock INTEGER,
    category_id INTEGER,
    FOREIGN KEY(category_id) REFERENCES categories(category_id)
)
""")

# Ensure tables exist before attempting to delete rows
cursor.execute("DELETE FROM books")
cursor.execute("DELETE FROM categories")

for _,row in categories_df.iterrows():
    cursor.execute(

        """
        INSERT INTO categories(category_id, category_name)
        VALUES (?,?)
        """,
        (row["category_id"], row["category_name"])

    )

for _, row in df.iterrows():
     cursor.execute(
        """
        INSERT INTO books(
            title,
            price_gbp,
            price_inr,
            rating,
            in_stock,
            category_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            row["title"],
            row["price_gbp"],
            row["price_inr"],
            row["rating"],
            row["in_stock"],
            row["category_id"]
        )
    )


connection.commit()


query1 = """ SELECT title , price_gbp

FROM books
 
WHERE in_stock = 1; """


query2 = """ SELECT title , rating

FROM books
 
ORDER BY rating DESC; """


query3 = """ SELECT title , rating

FROM books
 
ORDER BY rating DESC

LIMIT 10; """

query4 = """ SELECT DISTINCT category_name
FROM categories; """

query5 = """ SELECT title , price_gbp

FROM books
 
WHERE price_gbp BETWEEN 40 AND 50; """


query6 = """ SELECT books.title , books.price_inr , books.rating , categories.category_name

FROM books

JOIN categories ON books.category_id = categories.category_id; """


queries = {
    "query1_select_where": query1,
    "query2_order_by": query2,
    "query3_limit": query3,
    "query4_distinct": query4,
    "query5_between": query5,
    "query6_join": query6
}


results = {}

for name, query in queries.items():
    output = pd.read_sql_query(

        query,connection
    )

    results[name] = output

for name, output in results.items():
    output_path = os.path.join(folder, f"{name}.csv")
    output.to_csv(output_path,index=False)


sql_Q1 = pd.read_sql(query1, connection)
sql_Q6 = pd.read_sql(query6, connection)

pandas_join = df.merge(categories_df,on="category_name",how="inner")

pandas_join = pandas_join[

    [
        "title",
        "price_inr",
        "rating",
        "category_name"

    ]
]

print(pandas_join)

print(sql_Q6)

pandas_join = pandas_join.sort_values("title",ignore_index=False)

sql_Q6 = sql_Q6.sort_values("title",ignore_index=False)

pandas_join.equals(sql_Q6)
