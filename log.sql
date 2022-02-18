--find the crime report
SELECT description FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28;

    --USEFUL RESULTS: Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
        --Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.

    -- Money laundering took place at 20:30. No known witnesses.


--GET witness accounts from bakery robbery
SELECT transcript, name FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;

    --USEFUL RESULTS:

    --Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
    --If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

    --I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery,
    --I was walking by the ATM on Leggett Street and saw the thief there WITHDRAWING some money.

    --As the thief was leaving the bakery, THEY CALLED someone who talked to them for LESS THAN A MINUTE. In the call, I heard the thief say that they were planning to take the EARLIEST
    --FLIGHT out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

    --I'm the bakery owner, and someone came in, suspiciously whispering into a phone for about half an hour. They never bought anything. (WEAK, could have been anyone)



--LOOK AT SECUIRTY LOGS (THEFT OCCURED @ 10:15AM, DB IS IN 24 HR CLOCK, NOTE THAT MAN IS IN BAKERY FOR 30 MINS LIKELY MANY PRIOR)
SELECT activity,license_plate,hour,minute FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND (hour = 9 OR hour = 10);
    --USEFUL RESULTS:

    --only plate that fits the timeframe given with anput 30 mins of chatter before 10:15 and leaving around 10 mins after 10:15 is
    --G412CB7

    --FIND PEOPLE WITH THIS LISCENSE PLATE
    SELECT name FROM people WHERE license_plate = "G412CB7";
    --NAME = SOFIA

    --SOFIA HAS BEEN FOUND INNOCENT DUE TO THE ATM LOGS, WE MUST NOW CROSS REFERENCE (LMAOMAOMAOMAMMAOMAOM) THE ATM QUERY WITH THE NAMES OF ALL LICENSE PLATES FROM HOUR 9-10 C:
    SELECT name FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND (hour = 9 OR hour = 10));

    --PEOPLE WHO WENT TO ATM AND BAKERY
        Iman
        Taylor
        Luca
        Diana
        Bruce

     --AFTER FINDING FINAL SUSPECTS ADN THEIR DATA, FIND OUT WHO LEFT WITHIN 10 MINS OF 10:15 AM
     SELECT activity,license_plate,hour,minute FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 and activity = "exit";

     !!!!!TAYLOR LEAVES AT 10:35, BRUCE AND DIANA LEAVE WITHIN THE TIMEFRAME OF CRIME (IS SHE STILL AMOGUS???)



--CHECK ATM LOGS, SEE IF DATA CONNECTS BACK TO SOFIA
--GET NAMES OF EVERYONE, WHO USED THE ATM
SELECT name FROM people JOIN bank_accounts ON people.id = bank_accounts.person_id WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE atm_location = "Leggett Street" AND year = 2021 AND month = 7 AND day = 28);
    --SOFIA DOES NOT APPEAR --INNOCENT RETURN TO PREVIOUS SEARCH




--CHECK PHONE LOGS (Thief called)
SELECT name, duration FROM people JOIN phone_calls ON people.phone_number = phone_calls.caller WHERE year = 2021 AND month = 7 AND day = 28 AND duration <= 60;

    --referencing this table to our other 2 our final suspects are
    SELECT phone_number, passport_number, license_plate,name FROM people WHERE name IN ("Bruce","Taylor","Diana");
    Bruce --PASSPORT = 1988161715 ; PHONE = (367) 555-5533 ; PLATE = 94KL13X
    Taylor --PASSPORT = 5773159633 ; PHONE = (286) 555-6063 ; PLATE = 1106N58
    Diana--PASSPORT =  3592750733  ; PHONE =  (770) 555-1861 ; PLATE = 322W7JE




--FIND EARLIEST FLIGHT OUT OF FIFTYVILLE AND PASSENGERS
SELECT day, hour, minute, flights.id FROM flights JOIN airports ON flights.origin_airport_id = airports.id WHERE city = "Fiftyville" AND day = 29 ORDER BY hour;
    --Earliest flight out the next day:
        --hour = 8
        --min = 20
        --id = 36

        --Get all people from flight 36
        SELECT name FROM people JOIN passengers ON people.passport_number = passengers.passport_number WHERE flight_id = 36;

        --Notable passengers
            Taylor --Pseudo Innocent since she left bakery @ 10:35
            Bruce
            --DIANA OFF HOOK!!!! :OOOOOO

            --WE CAN CONCLUDE WITH RELATIVE CERTAINTY THAT BRUCE IS THE MOFO THAT STOLE A DUCK :C

        --get destination = NYC
        SELECT city FROM airports JOIN flights ON airports.id = flights.destination_airport_id WHERE flights.id = 36;
        --NYC

--GET ACCOMPLICE BY FINDING OUT WHO CALLED BRUCE FOR LESS THAN 1 MIN
SELECT name FROM people JOIN phone_calls ON people.phone_number = phone_calls.receiver WHERE year = 2021 AND month = 7 AND day = 28 AND duration <= 60 AND phone_calls.caller = "(367) 555-5533"; --Bruce phone
--ROBIN YOU SLIMY @#*&



----GOT YOU MFKZ!!!!!