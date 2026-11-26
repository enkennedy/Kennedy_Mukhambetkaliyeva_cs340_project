#Simplified Algorithm:

Final Simplified Algorithm - scheduleGenerator.py

Previous Iterations - ScheduleGeneratorV1.py, ScheduleGeneratorV2.py

To run simplified algorithm: sh run.sh constraints studentPreferences schedule

Test case data in solution_quality, 25 tests total

To run test cases: sh run_test.sh testNumber

#Extended Algorithm:

Extended Algorithm - ScheduleGeneratorExtended.py

Original Bryn Mawr data files in bmc_data_csv

Converted Bryn Mawr data files for algorithm in bmc_data

Mixed Haverford/BMC data in hav_data

To run Bryn Mawr tests: sh run_extended.sh SemesterYear

To run Hav/BMC test: python3 ScheduleGeneratorExtended.py hav_data/
constraints_HS2014.txt hav_data/prefs_HS2014.txt hav_data/schedule_HS2014.txt

#Additional Files/Scripts:

Time analysis test data in time_analysis

To run time analysis tests: sh run_time_test.sh #ofClasses/Students

is_valid_extended converts Hav/BMC csv files to input for extended algorithm

To convert CSV files to input for extended algorithm: python3 get_bmc_data.py constraints studentPrefs