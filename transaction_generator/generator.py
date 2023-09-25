import psycopg2
from typing import List, Dict, Tuple, Union
import pandas as pd
import numpy as np
import datetime
import time
import random
import sys

class TransactionGenerator:

    def __init__(self, mean_interval=15, duration=100000) -> None:
        self.mean_interval = mean_interval
        self.duration = duration

    def connect_to_postgres(self, host='192.168.1.193', port = 5432, 
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
        

    def load_data(self) -> pd.DataFrame:
        """
        Return payment and rental data as Pandas DatFrame
        Export data as CSV
        """
        conn, cur = self.connect_to_postgres()

        # Query payment data
        query = '''
        select 
            p.*,
            r.inventory_id
        from payment as p
        join rental as r on
            p.rental_id = r.rental_id
        ''' 
        cur.execute(query)
        payment_data = cur.fetchall()

        # Generate dataframe
        df = pd.DataFrame(payment_data, columns=['payment_id', 'customer_id', 'staff_id', 'rental_id', 'amount', 'payment_date', 'inventory_id'])
        df['payment_date'] = pd.to_datetime(df['payment_date'])
        df['payment_date'] = df['payment_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
 
        return df, conn, cur 
        

    def _generate_transaction(self, df: pd.DataFrame) -> Dict:
        
        payment_row = {}
        rental_row = {}

        # Generate payment id
        payment_id = df.payment_id.max() + 1
        payment_row['payment_id'] = payment_id

        # customer id
        customer_id = np.random.randint(low=df.customer_id.min(), high=df.customer_id.max())
        payment_row['customer_id'] = customer_id
        rental_row['customer_id'] = customer_id

        # staff id
        staff_id = np.random.randint(low=df.staff_id.min(), high=df.staff_id.max())
        payment_row['staff_id'] = staff_id
        rental_row['staff_id'] = staff_id

        # rental id
        rental_id = df.rental_id.max() + 1
        payment_row['rental_id'] = rental_id
        rental_row['rental_id'] = rental_id

        # payment date-current date: format:2007-02-15 22:25:46.996577
        payment_date = datetime.datetime.now()
        payment_row['payment_date'] = payment_date.strftime('%Y-%m-%d %H:%M:%S')

        # rental date
        rental_date = payment_date - datetime.timedelta(days=1)
        rental_row['rental_date'] = rental_date.strftime('%Y-%m-%d %H:%M:%S')

        # return date
        return_date = datetime.datetime.now()
        rental_row['return_date'] = return_date.strftime('%Y-%m-%d %H:%M:%S')

        # last update
        last_update = payment_date
        rental_row['last_update'] = last_update.strftime('%Y-%m-%d %H:%M:%S')

        # amount
        amount = np.random.randint(low=1, high=10)
        ## add some radom noise to price to simulate real-world data
        amount = amount + abs(random.normalvariate(mu=1, sigma=amount/3) * 10)
        payment_row['amount'] = amount

        # invenory
        inventory_id = np.random.randint(low=df.inventory_id.min(), high=df.inventory_id.max())
        rental_row['inventory_id'] = inventory_id

        return payment_row, rental_row
        
    def insert_transactions(self) -> None:

        df, conn, cur = self.load_data()

        # Generate transaction
        payment_row, rental_row = self._generate_transaction(df)
        
    
        # insert payment row postgres
        query_payment = f'''
        insert into payment (payment_id, customer_id, staff_id, rental_id, amount, payment_date)
        values ({payment_row['payment_id']}, {payment_row['customer_id']}, {payment_row['staff_id']}, {payment_row['rental_id']}, {payment_row['amount']}, '{payment_row['payment_date']}')
        '''

        # insert rental row postgres
        query_rental = f'''
        insert into rental (rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update)
        values ({rental_row['rental_id']}, '{rental_row['rental_date']}', {rental_row['inventory_id']}, {rental_row['customer_id']}, '{rental_row['return_date']}', {rental_row['staff_id']}, '{rental_row['last_update']}')
        '''

        try:
            cur.execute(query_rental)
            cur.execute(query_payment)
            conn.commit()
            print("Insert Succesful")
        except Exception as e:
            print(e)
            raise Exception("Insert Failed")
        finally:           
            cur.close()
            conn.close()

        
    def start_simulation(self) -> None:
        """
        Simulate transactions in real-time 
        Insert a transaction to postgres every random time interval
        """
        total_transactions = 0
        duration = self.duration
        print(f"Simulating business activity for {duration/60:.02f} minutes({duration/3600:.02f} hours)")
        while duration > 0:

            # sleep for random time interval
            time_interval = abs(random.normalvariate(mu=self.mean_interval, sigma=self.mean_interval/3))
            time.sleep(time_interval)

            # insert transaction
            self.insert_transactions()
            total_transactions += 1
            duration -= time_interval
            print(f"Remaining duration: {duration/60:.02f} minutes")

        # print total transactions simulated
        print(f"Total transactions simulated: {total_transactions}")



if __name__ == "__main__":
    generator = TransactionGenerator()
    generator.start_simulation()