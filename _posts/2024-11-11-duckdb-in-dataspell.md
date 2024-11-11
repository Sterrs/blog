---
layout: post
title:  "Testing Jetbrains' DataSpell"
date:   2024-11-11 00:00:00 +0100
categories: data
---

## Intro

I've generally liked Jetbrains' products in the past, and now that I spend most of my day everyday doing data analysis,
I figured I should try one of their more recent products: DataSpell.

Having used Databricks for a long time at work, I'm looking for something which fills the same niche but for local
projects. I want to be able to manage my database, Python and SQL scripts, and notebooks with Python and SQL together,
all from the same place.

## What Alternatives Tend to Lack

Most existing Python/Database workflows are lacking one or more of the following abilities:

1. Use SQL query output in Python code
2. Query local dataframes as if they were database tables
3. Convert local dataframes to database tables with ease
4. Parametrise SQL using Python variables

DataSpell solves the first two of these comfortably, but doesn't yet do the last two - and this is where my sticking
point has been so far. I think adding these as features would make it close to a must-have for me for small data
projects, and maybe even for larger ones.

It uses DuckDB to enable querying local dataframes like tables, which is an awesome addition,
something DuckDB can do out of the box, but I've struggled to set up in VSCode myself.

## Existing Comparison Products

Databricks does all these things, but it actually doesn't even do them that well, combining SQL and Python code is a
total nightmare. It's also an expensive enterprise solution not needed for small projects.

The closest thing to this editor that I've tried before is Visual Studio Code with various plugins, although I
generally find that the SQL integration in VSCode is not great.

An alternative is always just using PySpark/DuckDB in a Jupyter Notebook and writing queries inside strings or avoiding
SQL altogether. I think this generally feels quite clunky, and slows me down when I just want to answer some basic
data questions quickly.

## First Thoughts

So far, my thoughts are mixed. The general first impressions are positive, particularly in terms of look and feel, and
ease of set-up. However, it falls at many of the same hurdles as the two competitors I'm comparing it to.

The editor looks amazing, Python and virtual environments work out of the box,
markdown editing is enjoyable (I'm using it to write this post). But PyCharm does all that, and is free.

SQL integration is really awesome for anyone who wants to talk to a database, which I find is personally desirable even
for small projects as it just gives you a way to structure your pipelines better, and allows you to run quick queries.

I'd like to test out the dbt integration too. dbt is something I'd generally like to look more closely at, and perhaps
write a post about in the future.

On the other hand, while the table view looks nice, and the summary stats can be useful, I hide them by default because
they take up so much space. Being able to see the number of missing values is perhaps the most
helpful of all.

![](/blog/assets/2024_11_11_DataSpell_Column_Statistic.png)

The ability to make visualisations in the editor would be useful if it wasn't so utterly
basic, and didn't force you to start from scratch every time you reload the data.

![](/blog/assets/2024_11_11_DataSpell_Visualisations.png)

## My Main Issue

The main issue I've been having is that the DuckDB integration is quite basic (despite the editor piggy-backing off
DuckDB for some of its features!). The main issue is that DuckDB places a lock on the database file, so you can't
have the editor database integration and also write Python code which creates a DuckDB connection.

Admittedly, this is more of a limitation of DuckDB than anything else, and if the editor was able to get around this,
for example by passing a DuckDB connection variable into the local context, it would be going above and beyond. I'm not
entirely sure if this is even practically possible, especially with multiple notebooks.

It basically leaves me in a situation where I can load data into DataSpell using SQL blocks, and manipulated data in
the database using SQL blocks/scripts, but I can't do data processing in Python and then write my output to the database
while the connection is still open. You can't do all data processing in DuckDB SQL, and I'd like to incorporate Python
into my pipelines.

A classic example of this is Pandas' wonderful `get_dummies()` method, the SQL equivalent of which is horrific:

```sql
SELECT 
    id,
    CASE WHEN category = 'A' THEN 1 ELSE 0 END AS category_A,
    CASE WHEN category = 'B' THEN 1 ELSE 0 END AS category_B,
    CASE WHEN category = 'C' THEN 1 ELSE 0 END AS category_C
FROM 
    my_table;
```

I'm going to try a MySQL database backend to see if this will fix my issue, and I can exploit concurrency to write
tables freely from the Python notebook process.

## Conclusion

I'm undecided on whether to keep using it, and whether it would be worth paying for. Probably by itself I'm not totally
sold, but as part of the All Products Pack, it forms a decent addition.
