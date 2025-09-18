from dotenv import load_dotenv
from datetime import datetime
from executor import get_connection

conn = get_connection()

def run_task(name: str, block: str):
    """Run a DO block inside a transaction and rollback"""
    cur = conn.cursor()
    result = {}
    try:
        cur.execute(block)
        result = {"status": True, "last_run": datetime.now().isoformat()}
    except Exception as e:
        result = {"status": False, "last_run": datetime.now().isoformat(), "error": str(e)}
    finally:
        cur.close()
        conn.rollback()
    return name, result


def run_all_tests():
    """Run all task test cases and save to JSON"""
    tests = {
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
                                    c1 refcursor;
                                    c2 refcursor;
                                    BEGIN
                                        RAISE NOTICE 'RUNNING - get_facility_booking_summary validation';
                                        RAISE NOTICE 'Case1: facid = 1';
                                        FOR c1 IN SELECT * FROM get_facility_booking_summary(1) LOOP
                                        RAISE NOTICE 'Returned cursor: %', c1;
                                        END LOOP;
                                        RAISE NOTICE 'Case2: facid = 9999';
                                        FOR c2 IN SELECT * FROM get_facility_booking_summary(9999) LOOP
                                            RAISE NOTICE 'Returned cursor: %', c2;
                                        END LOOP;
                                    END $$;
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
                                        BEGIN
                                            RAISE NOTICE 'RUNNING - fetchallfacilities test cases';
                                            RAISE NOTICE 'Case1: limit = 1';
                                            PERFORM * FROM fetchallfacilities(1);
                                
                                            RAISE NOTICE 'Case2: limit = 3';
                                            PERFORM * FROM fetchallfacilities(3);

                                            RAISE NOTICE 'TEST CASES EXECUTED';
                                        END $$;

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

    results = {}
    for name, block in tests.items():
        task_name, result = run_task(name, block)
        results[task_name] = result
    return results 



