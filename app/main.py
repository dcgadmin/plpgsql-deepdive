import streamlit as st
from executor import get_default_data, get_facilities_list, get_facility_usage_hours
import time


def logo():
    dcg_logo = "https://static.wixstatic.com/media/5b8722_05a065ee3bee45428038293a3d45e92e~mv2.png/v1/fill/w_478,h_66,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/dcg_logo.png"
    st.logo(dcg_logo)



def side_navbar():
    pg = st.navigation([st.Page(r"pages/home.py", title="Home"),
                        st.Page(r"pages/booking_summary.py", title="Booking Summary"),
                        st.Page(r"pages/search_bookings.py", title="Search Bookings"),
                        st.Page(r"pages/member_name.py", title="Member Names"),
                        st.Page(r"pages/facilities_cost.py", title="Facilities Cost"),
                        st.Page(r"pages/all_facilities.py", title="Fetch All Facilities"),
                        st.Page(r"pages/check_discount.py", title="Check Discounts"),
                        ])

    pg.run()

    facilities_list = get_facilities_list()
    if facilities_list is not None:
        selected_facility = st.sidebar.selectbox("Select facility:", facilities_list, index=None, placeholder="Select facility name...")
        if selected_facility is not None:
            start_time = time.time()
            usage_hours = get_facility_usage_hours(selected_facility)
            end_time = time.time()  
            execution_time = round(end_time - start_time, 2)
            st.sidebar.write(f"Facility usage hours for {selected_facility} :", usage_hours)
            st.sidebar.write(f"Execution time : {execution_time} seconds")
    else:
        st.sidebar.write("No data for facilities list")


logo()
side_navbar()


