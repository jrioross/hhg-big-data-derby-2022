# hhg-big-data-derby-2022

## Data Tables & Schemas

**nyra_start_table.csv**

    - track_id - 3 character id for the track the race took place at. AQU -Aqueduct, BEL - Belmont, SAR - Saratoga.
    - race_date - date the race took place. YYYY-MM-DD.
    - race_number - Number of the race. Passed as 3 characters but can be cast or converted to int for this data set.
    - program_number - Program number of the horse in the race passed as 3 characters. Should remain 3 characters as it isn't limited to just numbers. Is essentially the unique identifier of the horse in the race.
    - weight_carried - An integer of the weight carried by the horse in the race.
    - jockey - Name of the jockey on the horse in the race. 50 character max.
    - odds - Odds to win the race passed as an integer. Divide by 100 to derive the odds to 1. Example - 1280 would be 12.8-1.

**nyra_race_table.csv**

    - track_id - 3 character id for the track the race took place at. AQU -Aqueduct, BEL - Belmont, SAR - Saratoga.
    - race_date - date the race took place. YYYY-MM-DD.
    - race_number - Number of the race. Passed as 3 characters but can be cast or converted to int for this data set.
    - distance_id - Distance of the race in furlongs passed as an integer. Example - 600 would be 6 furlongs.
    - course_type - The course the race was run over passed as one character. M - Hurdle, D - Dirt, O - Outer turf, I - Inner turf, T - turf.
    - track_condition - The condition of the course the race was run on passed as three characters. YL - Yielding, FM - Firm, SY - Sloppy, GD - Good, FT - Fast, MY - Muddy, SF - Soft.
    - run_up_distance - Distance in feet of the gate to the start of the race passed as an integer.
    - race_type - The classification of the race passed as as five characters. STK - Stakes, WCL - Waiver Claiming, WMC - Waiver Maiden - Claiming, SST - Starter Stakes, SHP - Starter Handicap, CLM - Claiming, STR - Starter Allowance, AOC - Allowance Optionl Claimer, SOC - Starter Optional Claimer, MCL - Maiden Claiming, ALW - Allowance, MSW - Maiden Special Weight.
    - purse - Purse in US dollars of the race passed as an money with two decimal places.
    - post_time - Time of day the race began passed as 5 character. Example - 01220 would be 12:20.

**nyra_tracking_table.csv**

    - track_id - 3 character id for the track the race took place at. AQU -Aqueduct, BEL - Belmont, SAR - Saratoga.
    - race_date - date the race took place. YYYY-MM-DD.
    - race_number - Number of the race. Passed as 3 characters but can be cast or converted to int for this data set.
    - program_number - Program number of the horse in the race passed as 3 characters. Should remain 3 characters as it isn't limited to just numbers. Is essentially the unique identifier of the horse in the race.
    - trakus_index - The common collection of point of the lat / long of the horse in the race passed as an integer. From what we can tell, it's collected every 0.25 seconds.
    - latitude - The latitude of the horse in the race passed as a float.
    - longitude - The longitude of the horse in the race passed as a float.

**nyra_2019_complete.csv** - This file is the combined 3 files into one table. The keys to join them trakus with race - track_id, race_date, race_number. To join trakus with start - track_id, race_date, race_number, program_number.

    - track_id - char(3)
    - race_date - date
    - race_number - char(3)
    - program_number - char(3)
    - trakus_index - int
    - latitude - float
    - longitude - float
    - distance_id - int
    - course_type - char(1)
    - track_condition - char(3)
    - run_up_distance - int
    - race_type - char(5)
    - post_time - char(5)
    - weight_carried - int
    - jockey - char(50)
    - odds - int
