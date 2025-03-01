import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import queries
import streamlit as st
import plotly.graph_objects  as go
import time

load_dotenv() 

PG_HOST = os.getenv("PG_HOST", None)
PG_PORT = os.getenv("PG_PORT", None)
PG_USER = os.getenv("PG_USER", None)
PG_PASSWORD = os.getenv("PG_PASSWORD", None)
PG_DBNAME = os.getenv("PG_DBNAME", None)


if not PG_HOST and not PG_PORT and not PG_USER and not PG_PASSWORD and not PG_DBNAME:
    raise ValueError("Database credentials are not set in the environment variables. Please set them and try again.")

def get_connection():
    try:
        connection = psycopg2.connect(
                                      host=PG_HOST,
                                      port=PG_PORT,
                                      user=PG_USER,
                                      password=PG_PASSWORD,
                                      dbname=PG_DBNAME,
                                      )
        return connection  

    except psycopg2.OperationalError as e:
        print(f"Database connection failed : {e}")
        print("Error : Unable to connect to the database. Check credentials & availability.")
        return None  
    
def get_booking_details(cursor):
    try:
        cursor.execute(queries.booking_details)  
        data = cursor.fetchall() 
        column_names = [desc[0] for desc in cursor.description]  
        df = pd.DataFrame(data, columns=column_names)
        return df.reset_index(drop=True)
    except psycopg2.Error as e:
        print(f"Query execution failed : {e}")
        return None
    
def get_facility_details(cursor):
    try:
        cursor.execute(queries.facility_details)  
        data = cursor.fetchall() 
        column_names = [desc[0] for desc in cursor.description]  
        df = pd.DataFrame(data, columns=column_names)
        return df.reset_index(drop=True)
    except psycopg2.Error as e:
        print(f"Query execution failed : {e}")
        return None

def get_individual_bookings(name, surname):
    try:
        connection = get_connection()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(queries.search_booking, (name, surname))  
                    data = cursor.fetchall()
                    column_names = [desc[0] for desc in cursor.description]  
                    df = pd.DataFrame(data, columns=column_names)
                    return df

    except psycopg2.Error as e:
        return (f"Query execution failed : {e}")
    

def get_default_data():
    connection = get_connection()
    if connection:
        with connection:
            with connection.cursor() as cursor:
                booking_details_df = get_booking_details(cursor)
                facility_details_df = get_facility_details(cursor)
                if booking_details_df is not None and facility_details_df is not None:
                    return booking_details_df, facility_details_df
    return None

def get_facilities_list():
    try:
        connection = get_connection()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(queries.facilities)  
                    data = cursor.fetchall() 
                    column_names = [desc[0] for desc in cursor.description]  
                    df = pd.DataFrame(data, columns=column_names)
                    facilities_list = df["name"].tolist()
                    return facilities_list
        return None
    except psycopg2.Error as e:
        print(f"Query execution failed : {e}")
        return None
    
def get_facility_id(selected_facility):
    try:
        connection = get_connection()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(queries.facilities)  
                    data = cursor.fetchall() 
                    column_names = [desc[0] for desc in cursor.description]  
                    df = pd.DataFrame(data, columns=column_names)
                    filtered_df = df[df["name"] == selected_facility]
                    facid_value = str(filtered_df["facid"].values[0])
                    return facid_value
        return None
    except psycopg2.Error as e:
        print(f"Query execution failed : {e}")
        return None
     
def get_facility_usage_hours(selected_facility):
    try:
        facid_value = get_facility_id(selected_facility)
        connection = get_connection()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(queries.facility_usage_hours, (facid_value))  
                    usage_hours = cursor.fetchall()[0][0]
                    return usage_hours
        return None
    except psycopg2.Error as e:
        print(f"Query execution failed : {e}")
        return None
    
def get_facility_booking_summary(selected_facility):
    try:
        facid_value = get_facility_id(selected_facility)
        connection = get_connection()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    # cursor.execute("BEGIN;") 
                    cursor.execute(queries.booking_summary, (facid_value,))  
                    cursor_names = cursor.fetchall()  
                    cursor_name1 = cursor_names[0][0]
                    cursor_name2 = cursor_names[1][0]
                    # cursor.execute("commit;")
                    cursor.execute(f'fetch all in "{cursor_name1}";')
                    data = cursor.fetchall()
                    column_names = [desc[0] for desc in cursor.description]  
                    df1 = pd.DataFrame(data, columns=column_names)

                    cursor.execute(f'fetch all in "{cursor_name2}";')
                    data = cursor.fetchall()
                    column_names = [desc[0] for desc in cursor.description]  
                    df2 = pd.DataFrame(data, columns=column_names)
                    return df1, df2

    except psycopg2.Error as e:
        return(f"Query execution failed : {e}")
    
def get_member_name(limit):
    try:
        connection = get_connection()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    start_time = time.time()
                    cursor.execute(queries.member_name, (limit,))  
                    data = cursor.fetchall()
                    column_names = [desc[0] for desc in cursor.description]  
                    # df = pd.DataFrame(data, columns=column_names)
                    end_time = time.time()  
                    execution_time = round(end_time - start_time, 2)
                    return execution_time

    except psycopg2.Error as e:
        print(f"Query execution failed : {e}")
        return None

def get_facilities_cost(selected_facility):
    facid_value = get_facility_id(selected_facility)
    try:
        connection = get_connection()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(queries.facilities_cost, (facid_value,))  
                    data = cursor.fetchall()
                    column_names = [desc[0] for desc in cursor.description]  
                    df = pd.DataFrame(data, columns=column_names)
                    return df

    except psycopg2.Error as e:
        return (f"Query execution failed : {e}")

def get_all_facilities(limit):
    try:
        connection = get_connection()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(queries.all_facilities, (limit,))  
                    data = cursor.fetchall()
                    column_names = [desc[0] for desc in cursor.description]  
                    df = pd.DataFrame(data, columns=column_names)
                    return df

    except psycopg2.Error as e:
        print(f"Query execution failed : {e}")
        return None 
    
def get_members_list():
    try:
        connection = get_connection()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(queries.members)
                    data = cursor.fetchall()
                    column_names = [desc[0] for desc in cursor.description]  
                    df = pd.DataFrame(data, columns=column_names)
                    member_mapping = dict(zip(df['firstname'] + ' ' + df['Surname'], df['memid']))
                    members_list = list(member_mapping.keys())
                    return member_mapping, members_list

    except psycopg2.Error as e:
        print(f"Query execution failed : {e}")
        return None  
    
def get_member_id(selected_member):
    try:
        connection = get_connection()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    
                    cursor.execute(queries.members)  
                    data = cursor.fetchall()
                    column_names = [desc[0] for desc in cursor.description]  
                    df = pd.DataFrame(data, columns=column_names)
                    first_name = selected_member.split()[0]
                    member_id = str(df.loc[df["firstname"] == first_name, "memid"].values[0])
                    return member_id

    except psycopg2.Error as e:
        print(f"Query execution failed : {e}")
        return None 
    
def get_discounts(selected_member):
    try:
        connection = get_connection()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    member_id = get_member_id(selected_member)
                    cursor.execute(queries.check_discount, (member_id,))  
                    data = cursor.fetchall()
                    column_names = [desc[0] for desc in cursor.description]  
                    df = pd.DataFrame(data, columns=column_names)

                    return df

    except psycopg2.Error as e:
        print(f"Query execution failed : {e}")
        return None  

def get_create_booking(selected_facility,selected_member,starttime,slots):
    facility_id = get_facility_id(selected_facility)
    member_id = get_member_id(selected_member)
    try:
        connection = get_connection()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(queries.create_booking, (facility_id,member_id,starttime,slots))  
                    data = cursor.fetchall()
                    column_names = [desc[0] for desc in cursor.description]  
                    df = pd.DataFrame(data, columns=column_names)
                    return df

    except psycopg2.Error as e:
        return(f"Query execution failed : {e}")

def booking_details_chart(booking_details_df):
    explode_values = [0.1] * len(booking_details_df["facility_name"].unique())
    fig = go.Figure(
                    data=[go.Pie(
                                labels=booking_details_df["facility_name"],
                                values=booking_details_df["BookingCount"],
                                hole=0.4,  
                                # pull=explode_values,  
                                )]
                    )

    st.plotly_chart(fig, key=f"chart_{time.time()}") 

