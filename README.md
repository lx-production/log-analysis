# Python - Postgresql - Log Analysis

## Requirements

- Python 3 (Python 2 will work also, but the code is optimized for Python 3)
- Psycopg2
- Postgresql
- Vagrant

## How to run

1. Clone the files to where the "news" database is loaded

2. Create 2 views in the "news" database using the commands below. These views are used in the third query.

```sql
-- Create errors_in_days view to be used in bad_days function
create view errors_in_days as
select date(time), count (status) as errors from log
where status = '404 NOT FOUND'
group by date order by errors desc;

-- Create views_in_days to be used in bad_days function
create view views_in_days as
select date(time), count (*) as views from log
group by date order by views desc;
```

3. Run `python3 sql_queries.py`
