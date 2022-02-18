-- Keep a log of any SQL queries you execute as you solve the mystery.

--find the crime report
SELECT description FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28;

    --USEFUL RESULTS: Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
        --Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.

    -- Money laundering took place at 20:30. No known witnesses.


--GET witness accounts from bakery robbery
SELECT transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;

    --USEFUL RESULTS:

    --Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
    --If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

    --I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery,
    --I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

    --As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest
    --flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

    --I'm the bakery owner, and someone came in, suspiciously whispering into a phone for about half an hour. They never bought anything.



--LOOK AT SECUIRTY LOGS (THEFT OCCURED @ 10:15AM, DB IS IN 24 HR CLOCK, NOTE THAT MAN IS IN BAKERY FOR 30 MINS LIKELY MANY PRIOR)
SELECT activity,license_plate,hour,minute FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND (hour = 9 OR hour = 10);
    --USEFUL RESULTS:

    --only plate that fits the timeframe given with anput 30 mins of chatter before 10:15 and leaving around 10 mins after 10:15 is
    --G412CB7

    --FIND PEOPLE WITH THIS LISCENSE PLATE
    SELECT name FROM people WHERE liscense_plate = "G412CB7";

