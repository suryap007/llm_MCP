import sqlite3 as sq
import argparse
from fastmcp import FastMCP
# from mcp.server.fastmcp import FastMCP
import yfinance as yf
import pandas as pd
from datetime import datetime as t
import os 

mcp = FastMCP('mcp-server')

def init_db():
    conn = sq.connect("sample.db")

    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            profession TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn, cursor

@mcp.tool()
def add_data(query: str) -> bool:
    """Add new data to the people table using a SQL INSERT query.

    Args:
        query (str): SQL INSERT query following this format:
            INSERT INTO people (name, age, profession)
            VALUES ('John Doe', 30, 'Engineer')
        
    Schema:
        - name: Text field (required)
        - age: Integer field (required)
        - profession: Text field (required)
        Note: 'id' field is auto-generated
    
    Returns:
        bool: True if data was added successfully, False otherwise
    
    Example:
        >>> query = '''
        ... INSERT INTO people (name, age, profession)
        ... VALUES ('Alice Smith', 25, 'Developer')
        ... '''
        >>> add_data(query)
        True
    """
    conn, cursor = init_db()
    try:
        cursor.execute(query)
        conn.commit()
        return True
    except sq.Error as e:
        print(f"Error adding data: {e}")
        return False
    finally:
        conn.close()

@mcp.tool()
def read_data(query: str = "SELECT * FROM people") -> list:
    """Read data from the people table using a SQL SELECT query.

    Args:
        query (str, optional): SQL SELECT query. Defaults to "SELECT * FROM people".
            Examples:
            - "SELECT * FROM people"
            - "SELECT name, age FROM people WHERE age > 25"
            - "SELECT * FROM people ORDER BY age DESC"
    
    Returns:
        list: List of tuples containing the query results.
              For default query, tuple format is (id, name, age, profession)
    
    Example:
        >>> # Read all records
        >>> read_data()
        [(1, 'John Doe', 30, 'Engineer'), (2, 'Alice Smith', 25, 'Developer')]
        
        >>> # Read with custom query
        >>> read_data("SELECT name, profession FROM people WHERE age < 30")
        [('Alice Smith', 'Developer')]
    """
    conn, cursor = init_db()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sq.Error as e:
        print(f"Error reading data: {e}")
        return []
    finally:
        conn.close()

@mcp.tool()
def get_stockprice_symbol(symbol : str)->float:
    """ give the latest price or current price of stock by symbol. example (TCS.NS , itc.ns , TATASTEEL.ns) """
    
    stock = yf.Ticker(symbol)
    try:
        price = stock.fast_info['lastPrice']
        return price
    except KeyError:
        return 0.0
    
    
@mcp.tool()
def get_stockprice_name(name: str) -> float:
    """Get the current stock price by company name (e.g.  Wipro 'Syrma SGS Technology', 'TBO Tek', 'TVS Motor Company', 'TVS Supply Chain Solutions', 'Tanla Platforms', 'Tata Chemicals', 'Tata Communications', 'Tata Consultancy Services', 'Tata Consumer Products', 'Tata Elxs)."""
    stick = name.upper()

    # Load and clean dataset
    dataset = pd.read_csv("cleaned_dataset.csv")
    dataset['comp_name'] = dataset['comp_name'].str.upper()
    
    symbol = dataset.loc[dataset['comp_name'] == stick, 'yf_sym'].values[0]
    
    stock = yf.Ticker(symbol)
    try:
        price = stock.fast_info['lastPrice']
        return price
    except KeyError:
        return 0.0
        
@mcp.tool()
def get_all_symbol()-> list:
    """give all the company name available in my database or list all the company name in indian stock"""
    dataset = pd.read_csv("cleaned_dataset.csv")
    return dataset["comp_name"].to_list()

@mcp.tool()
def get_current_time() -> str:
    """print the current time or date"""
    time = str(t.now())
    return time


@mcp.tool()
def get_stock_news(name: str) -> list[dict[str, str]]:
    """Get the current stock news by company name (e.g.  Wipro 'Syrma SGS Technology', 'TBO Tek', 'TVS Motor Company', 'TVS Supply Chain Solutions', 'Tanla Platforms', 'Tata Chemicals', 'Tata Communications', 'Tata Consultancy Services', 'Tata Consumer Products', 'Tata Elxs)."""
    stick = name.upper()

    # Load and clean dataset
    dataset = pd.read_csv("cleaned_dataset.csv")
    dataset['comp_name'] = dataset['comp_name'].str.upper()
    
    symbol = dataset.loc[dataset['comp_name'] == stick, 'yf_sym'].values[0]
    
    stock = yf.Ticker(symbol)
    news_items = stock.news
    result = []

    for news_item in news_items:
        content = news_item.get('content', {})
        title = content.get('title', 'No Title Available')
        summary = content.get('summary', 'No Summary Available')
        pub_date = content.get('pubDate', 'No Date Available')

        result.append({
            'title': title,
            'summary': summary,
            'pubDate': pub_date
        })

    return result

app = mcp.http_app()

if __name__ == "__main__":
    mcp.run(transport="sse")

