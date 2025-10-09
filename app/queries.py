search_booking = "Select * from search_bookings(%s, %s);"
booking_details = "Select * from booking_details;"
facility_details = "Select * from facility_details;"
facilities = "Select * from facilities;"
facility_usage_hours = "select get_facility_usage_hours(%s);"
booking_summary = "Select get_facility_booking_summary(%s);"
members = "Select * from members"
member_name = "with alias1 as NOT MATERIALIZED (select get_member_name(mod(generate_series,50)) from generate_series(1,%s)) select count(1) from alias1;"
facilities_cost = "Select * from getfacilitiescost(%s);"
all_facilities = "Select * from fetchallfacilities(%s);"
check_discount = "Select * from check_discount_dynamic(%s);"
create_booking = "call createbooking(%s,%s,%s,%s)"
test_cases = {
    "Search Bookings": """
        DO $$
        BEGIN
            RAISE NOTICE 'Case1_Surname_smith';
            PERFORM * FROM search_bookings('Surname', 'smith');
            RAISE NOTICE 'Case2_Firstname_jane';
            PERFORM * FROM search_bookings('firstname', 'jane');
            RAISE NOTICE 'Case3_NoMatch';
            PERFORM * FROM search_bookings('Surname', 'xyz');
            RAISE NOTICE 'Case4_Uppercase_SMITH';
            PERFORM * FROM search_bookings('Surname', 'SMITH');
        END $$;
    """,
    "Booking Summary": """
                                        DO $$
                                    DECLARE
                                        func_return_type text;
                                        rec RECORD;
                                    BEGIN
                                        SELECT pg_get_function_result(p.oid)
                                        INTO func_return_type
                                        FROM pg_proc p
                                        JOIN pg_namespace n ON n.oid = p.pronamespace
                                        WHERE p.proname = 'get_facility_booking_summary'
                                        AND n.nspname = 'public'
                                        ORDER BY p.oid DESC
                                        LIMIT 1;
                                        IF func_return_type ILIKE '%refcursor%' THEN
                                            RAISE EXCEPTION 'TEST FAILED';
                                        ELSIF func_return_type ILIKE '%mem_name%' THEN
                                            BEGIN
                                                SELECT * INTO rec FROM get_facility_booking_summary(1) LIMIT 1;
                                                IF rec IS NULL THEN
                                                    RAISE EXCEPTION 'TEST FAILED';
                                                ELSE
                                                    RAISE NOTICE 'TEST PASSED';
                                                END IF;
                                            EXCEPTION WHEN OTHERS THEN
                                                RAISE EXCEPTION 'TEST FAILED';
                                            END;
                                        ELSE
                                            RAISE EXCEPTION 'TEST FAILED';
                                        END IF;
                                    END;
                                    $$;

    """,
    "Check Discounts": """
        DO $$
        DECLARE
            v_memid INT;
            v_expected BOOLEAN;
            v_actual   BOOLEAN;
        BEGIN
            FOR v_memid IN SELECT memid FROM members WHERE memid <= 5 LOOP
                SELECT (COUNT(*) >= 5)
                INTO v_expected
                FROM bookings
                WHERE bookings.memid = v_memid
                AND starttime >= now() - INTERVAL '24 month';
                v_actual := check_discount_dynamic(v_memid);
                IF v_actual = v_expected THEN
                    RAISE NOTICE 'PASS | memid=% | expected=% | actual=%', v_memid, v_expected, v_actual;
                ELSE
                    RAISE EXCEPTION 'FAIL | memid=% | expected=% | actual=%', v_memid, v_expected, v_actual;
                END IF;
            END LOOP;
        END $$;
    """,
    "Member Names": """
        DO $$
        DECLARE
            v_lang TEXT;
        BEGIN
            SELECT l.lanname
            INTO v_lang
            FROM pg_proc p
            JOIN pg_language l ON p.prolang = l.oid
            WHERE p.proname = 'get_member_name';
            IF v_lang = 'sql' THEN
                RAISE NOTICE 'Passed: get_member_name is written in SQL';
            ELSE
                RAISE EXCEPTION 'Failed: get_member_name is written in %, expected SQL', v_lang;
            END IF;
        END;
        $$;     
    """,
    "Select facility": """
        DO $$
        DECLARE
            start_time TIMESTAMP;
            end_time TIMESTAMP;
            exec_time INTERVAL;
            hours numeric;
        BEGIN
            start_time := clock_timestamp();
            hours := get_facility_usage_hours(1);
            end_time := clock_timestamp();
            exec_time := end_time - start_time;
            RAISE NOTICE 'Facility Usage Hours: %', hours;
            RAISE NOTICE 'Execution Time: % seconds', EXTRACT(EPOCH FROM exec_time);
            IF EXTRACT(EPOCH FROM exec_time) > 2 THEN
                RAISE EXCEPTION 'TEST CASE FAILED: Execution time exceeded 2 seconds';
            ELSE
                RAISE NOTICE 'PASSED';
            END IF;
        END $$;
    """,
    "Facilities Cost": """ 
        DO $$
        BEGIN
            RAISE NOTICE 'RUNNING - getfacilitiescost test cases';
            RAISE NOTICE 'Case1: facid = 1';
            PERFORM * FROM getfacilitiescost(1);
            RAISE NOTICE 'Case2: facid = 9999';
            PERFORM * FROM getfacilitiescost(9999);
            RAISE NOTICE 'TEST CASES EXECUTED';
        END $$;
    """,
    "Fetch All Facilities": """
                                    DO $$
DECLARE
    arr text[];
BEGIN
    SELECT array_agg(f) INTO arr FROM fetchallfacilities(3) f;
    IF arr IS NULL OR array_length(arr,1) < 2 THEN
        RAISE EXCEPTION ' TEST FAILED: Insufficient output.';
    END IF;
    IF arr[array_length(arr,1)] = concat('Last Facility - ', arr[array_length(arr,1)-1]) THEN
        RAISE NOTICE 'TEST PASSED';
    ELSE
        RAISE EXCEPTION 'TEST FAILED';
    END IF;
END;
$$;
    """,
    "Create Booking": """
        DO $$
        BEGIN
            RAISE NOTICE 'RUNNING - createbooking test cases';
            RAISE NOTICE 'Case1: Insert valid booking';
            CALL createbooking(1, 3, now()::timestamp, 1);
        EXCEPTION 
            WHEN others THEN
                raise notice '%', SQLSTATE;
                if SQLERRM ilike '%booking overlaps%' then 
                    null;
                elseif SQLERRM ilike '%invalid transaction termination%' then 
                    RAISE EXCEPTION 'Code Validation Failed:' ;
                end if;
        END $$;
    """
}








