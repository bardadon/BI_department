from google.cloud import bigquery
import os
import psycopg2
import pandas as pd
import datetime

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/opt/airflow/config/service_account.json'

def _connect_to_postgres(host='192.168.1.193', port = 5432, 
                            user='postgres', password='1365', database='bi_department_dvd_rental'):

    """
    Connect to Postgres(the compapny's production database) 
    """
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=password, database=database)
        cur = conn.cursor()
        print("Connection Succesful")
        return conn, cur
    except Exception as e:
        print(e)
        raise Exception("Connection Failed")

def _export_fact_table():
    """
    Improve this.
    instead of extracting everything, append the latest batch 
    """
    bigquery_client = bigquery.Client()
     
    # extract fact table from BigQuery(data only from 2023-01-01)
    query = "select * from `bi-department-399912.bi_department.fact_table` order by payment_id desc"
    query_job = bigquery_client.query(query)
    df = query_job.result().to_dataframe()
    df = df[df['payment_date'] > '2023-01-01']

    # Export dataframe as CSV
    df.to_csv(f"/opt/airflow/data/data.csv")

def _load_to_fact_table():

    # Extract latest date from data warehouse
    bigquery_client = bigquery.Client()

    query = "SELECT max(payment_date) FROM `bi-department-399912.bi_department.fact_table`"
    query_job = bigquery_client.query(query)
    result = query_job.result()

    for row in result:
        latest_date = row[0]

    # Extract data from postgres according to latest date
    conn, cur = _connect_to_postgres()

    query = f'''
    select 
        p.payment_id,
        p.customer_id,
        p.staff_id,
        p.rental_id,
        p.payment_date,
        r.rental_date,
        r.return_date,
        m.title,
        m.description,
        m.release_year,
        m.rating,
        c3.name as category,
        p.amount::float as price,
        c.first_name,
        c.last_name,
        c.email,
        c.address_id,
        a.address,
        c1.city,
        c2.country
    from payment as p
    join rental as r on
        p.rental_id = r.rental_id
    join customer as c on
        c.customer_id = p.customer_id
    join address as a on 
        a.address_id = c.address_id
    join city as c1 on
        c1.city_id = a.city_id
    join country as c2 on
        c2.country_id = c1.country_id
    join inventory as i on
        i.inventory_id = r.inventory_id
    join film as m on 
        m.film_id = i.film_id
    join film_category as f1 on
        f1.film_id = m.film_id
    join category as c3 on
        c3.category_id = f1.category_id
    where
        payment_date > '{latest_date}'
    order by 
        payment_id desc
    '''

    cur.execute(query)
    result = cur.fetchall()

    results_df = pd.DataFrame(result, columns=['payment_id', 'customer_id', 'staff_id', 'rental_id', 'payment_date', 'rental_date', 'return_date', 'title', 'description', 'release_year', 'rating', 'category', 'price', 'first_name', 'last_name', 'email', 'address_id', 'address', 'city', 'country'])

    # Load data to BigQuery
    bigquery_client.load_table_from_dataframe(
        dataframe=results_df,
        destination='bi-department-399912.bi_department.fact_table',
        project='bi-department-399912',
        job_config=bigquery.LoadJobConfig(
            write_disposition='WRITE_APPEND'
        )
    )

    print(f"Loaded {len(results_df)} rows to BigQuery")

    # Export as CSV
    ## if file exists, append to it, else create a new file with all the data
    os.chdir('/opt/airflow/data')
    if os.path.exists(f"data.csv"):
        results_df.to_csv(f"/opt/airflow/data/data.csv", mode ='a',header=False)
    else:
        _export_fact_table()


    # Close connection
    conn.close()
    cur.close()
    bigquery_client.close()





if __name__ == "__main__":
        _export_fact_table()