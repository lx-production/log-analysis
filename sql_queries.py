#! /usr/bin/env python3
import psycopg2
# from decimal import *

# Joining 2 tables: aticles and log
pop_3posts_sql = """
select title, count(path) as views
from articles, log where '/article/' || articles.slug = log.path
group by title order by views desc limit 3;
"""

# Joining all 3 tables and then calculate the sum of views using Subquery
pop_authors_sql = """
select name, sum(views) as views
from (select articles.title, authors.name, count(log.path) as views
    from articles, authors, log
    where '/article/' || articles.slug = log.path
    and articles.author = authors.id
    group by authors.name, articles.title) as all_posts
group by name order by views desc;
"""

# Joining 2 views: views_in_days and errors_in_days
bad_days_sql = """
select views_in_days.date, views, errors
from views_in_days join errors_in_days
on views_in_days.date = errors_in_days.date
order by errors desc;
"""

db_name = 'news'


def connect():
    try:
        db = psycopg2.connect(dbname=db_name)
        cursor = db.cursor()
        return db, cursor
    except:
        print("Can't connect to database")


def pop_3posts_all():
    """Return the most popular three articles of all time."""
    db, cursor = connect()
    cursor.execute(pop_3posts_sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    for a in result:
        print (a[0], '{:>10}{}'.format(a[1], " views"))

print ("Three most popular articles of all time")
print (pop_3posts_all())


def pop_authors_all():
    """Return the most popular article authors of all time."""
    db, cursor = connect()
    cursor.execute(pop_authors_sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    for a in result:
        print ('{:>25}{}{}{}'.format(a[0], "    ", a[1], " views"))

print ("Most poppular authors of all time")
print (pop_authors_all())


def bad_days():
    """Return days more than 1 percent of requests lead to errors."""
    db, cursor = connect()
    cursor.execute(bad_days_sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    for a in result:
        if float(a[2])/float(a[1])*100 > 1:
            print (a[0], "    ", float(a[2])/float(a[1])*100, "%")
        else:
            pass

print ("Which days more than 1% of requests lead to errors?")
print (bad_days())
