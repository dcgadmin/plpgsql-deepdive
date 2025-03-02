search_booking = "Select * from search_bookings(%s, %s);"
booking_details = "Select * from booking_details;"
facility_details = "Select * from facility_details;"
facilities = "Select * from facilities;"
facility_usage_hours = "select get_facility_usage_hours(%s);"
booking_summary = "Select get_facility_booking_summary(%s);"
members = "Select * from members"
member_name = "with alias1 as NOT MATERIALIZED (select get_member_name(mod(generate_series,100)) from generate_series(1,%s)) select count(1) from alias1;"
facilities_cost = "Select * from getfacilitiescost(%s);"
all_facilities = "Select * from fetchallfacilities(%s);"
check_discount = "Select * from check_discount_dynamic(%s);"
create_booking = "call createbooking(%s,%s,%s,%s)"
