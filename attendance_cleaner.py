"""
Attendance Cleaner
------------------
Reads attendance.txt, cleans the names, finds the unique students with a set
and saves the sorted list to attendance_clean.csv.
Run with:  python attendance_cleaner.py
"""

import csv


def main():
    # 1. Read the file (one name per line)
    try:
        with open("attendance.txt", encoding="utf-8-sig") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: attendance.txt was not found. Put it in the same folder.")
        return
    except UnicodeDecodeError:
        print("Error: attendance.txt must be saved as a UTF-8 text file.")
        return

    # 2. Clean every name: remove extra spaces, make each word start with a capital.
    #    Blank lines are skipped.
    names = [" ".join(line.strip().split()).title()
             for line in lines if line.strip() != ""]
    print("Original number of records:", len(names))

    if len(names) == 0:
        print("No names found. Nothing to clean.")
        return

    # 3. A set keeps each name only once
    unique_students = set(names)
    print("Unique students:", len(unique_students))

    # 4. Sort A to Z
    sorted_names = sorted(unique_students)

    # 5. Save to attendance_clean.csv
    try:
        with open("attendance_clean.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["name"])
            for name in sorted_names:
                writer.writerow([name])
    except PermissionError:
        print("Could not save. Close attendance_clean.csv if it is open elsewhere.")
        return

    # 6. Show the cleaned list
    print("\nCleaned attendance list (saved to attendance_clean.csv):")
    for name in sorted_names:
        print(" -", name)


if __name__ == "__main__":
    main()
