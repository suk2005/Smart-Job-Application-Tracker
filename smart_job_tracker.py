#SMART JOB APPLICATION TRACKER

import mysql.connector

#Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="suk@2005",
    database="smart_job_tracker"
)
cursor = db.cursor()


#Add a new application
def add_application():
    company = input("Enter company name: ")
    role = input("Enter job role: ")
    follow_up = input("Enter follow-up date (YYYY-MM-DD): ")

    #Company and role empty not allowed 
    if company == "" or role == "":
        print("Company and role are required.")
        return

    #An empty date is saved as NULL
    if follow_up == "":
        follow_up = None

    cursor.execute(
        "INSERT INTO job_applications (company, role, status, follow_up) VALUES (%s, %s, %s, %s)",
        (company, role, "Applied", follow_up)
    )
    db.commit()
    print("Application added successfully!")


#View all applications
def view_applications():
    cursor.execute("SELECT * FROM job_applications")
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No applications found.")
        return

    #Each data row by row 
    for row in rows:
        print("\nApplication ID:", row[0])
        print("Company:", row[1])
        print("Role:", row[2])
        print("Status:", row[3])
        print("Follow-up:", row[4])


#Search an application by company name
def search_application():
    name = input("Enter company name to search: ")

    cursor.execute(
        "SELECT * FROM job_applications WHERE company = %s",
        (name,)
    )
    row = cursor.fetchone()

    if row is None:
        print("Application not found.")
        return

    #Display only the searched application
    print("\nApplication ID:", row[0])
    print("Company:", row[1])
    print("Role:", row[2])
    print("Status:", row[3])
    print("Follow-up:", row[4])


#Update the status of an application
def update_status():
    view_applications()

    app_id = input("Enter application ID: ")

    if app_id.isdigit() == False:
        print("Please enter a number.")
        return

    #Check that this ID exists in the database
    cursor.execute("SELECT * FROM job_applications WHERE application_id = %s", (app_id,))
    if cursor.fetchone() is None:
        print("Invalid application ID.")
        return

    print("1. Applied")
    print("2. Interview")
    print("3. Selected")
    print("4. Rejected")
    choice = input("Choose new status: ")

    if choice == "1":
        status = "Applied"
    elif choice == "2":
        status = "Interview"
    elif choice == "3":
        status = "Selected"
    elif choice == "4":
        status = "Rejected"
    else:
        print("Invalid choice.")
        return

    cursor.execute("UPDATE job_applications SET status = %s WHERE application_id = %s", (status, app_id))
    db.commit()
    print("Status updated successfully!")


#Change the follow-up date of an application
def update_follow_up():
    view_applications()

    app_id = input("Enter application ID: ")

    if app_id.isdigit() == False:
        print("Please enter a number.")
        return

    cursor.execute("SELECT * FROM job_applications WHERE application_id = %s", (app_id,))
    if cursor.fetchone() is None:
        print("Invalid application ID.")
        return

    date = input("Enter new follow-up date (YYYY-MM-DD): ")
    cursor.execute("UPDATE job_applications SET follow_up = %s WHERE application_id = %s", (date, app_id))
    db.commit()
    print("Follow-up date updated!")


#Update application IDs after deleting a record
def reset_application_ids():
    cursor.execute(
        "SELECT application_id FROM job_applications ORDER BY application_id"
    )
    rows = cursor.fetchall()
    ids = [row[0] for row in rows]

    if len(ids) == 0:
        cursor.execute("ALTER TABLE job_applications AUTO_INCREMENT = 1")
        return

    offset = max(ids) + len(ids) + 1

    for app_id in ids:
        cursor.execute(
            "UPDATE job_applications SET application_id = %s WHERE application_id = %s",
            (app_id + offset, app_id)
        )

    #Renumber the remaining applications from 1
    for new_id, old_id in enumerate(ids, start=1):
        cursor.execute(
            "UPDATE job_applications SET application_id = %s WHERE application_id = %s",
            (new_id, old_id + offset)
        )

    db.commit()

    #Set the next automatically generated ID
    cursor.execute(
        "ALTER TABLE job_applications AUTO_INCREMENT = " + str(len(ids) + 1)
    )


#Delete a job application
def delete_application():
    view_applications()

    app_id = input("Enter application ID to delete: ")

    if app_id.isdigit() == False:
        print("Please enter a number.")
        return

    #Check that this ID exists in the database
    cursor.execute(
        "SELECT * FROM job_applications WHERE application_id = %s",
        (app_id,)
    )

    if cursor.fetchone() is None:
        print("Invalid application ID.")
        return

    #Delete the selected application
    cursor.execute(
        "DELETE FROM job_applications WHERE application_id = %s",
        (app_id,)
    )
    db.commit()

    #Update IDs of the remaining applications
    reset_application_ids()

    print("Application deleted successfully!")
    print("Remaining application IDs have been updated.")


#Show a summary of all applications
def show_summary():
    applied = 0
    interview = 0
    selected = 0
    rejected = 0

    cursor.execute("SELECT status FROM job_applications")
    rows = cursor.fetchall()

    for row in rows:
        if row[0] == "Applied":
            applied = applied + 1
        elif row[0] == "Interview":
            interview = interview + 1
        elif row[0] == "Selected":
            selected = selected + 1
        elif row[0] == "Rejected":
            rejected = rejected + 1

    print("\n===== APPLICATION SUMMARY =====")
    print("Total applications:", len(rows))
    print("Applied:", applied)
    print("Interview:", interview)
    print("Selected:", selected)
    print("Rejected:", rejected)


#Main menu 
while True:
    print("\n===== SMART JOB APPLICATION TRACKER =====")
    print("1. Add application")
    print("2. View applications")
    print("3. Search application")
    print("4. Update status")
    print("5. Update follow-up date")
    print("6. Application summary")
    print("7. Delete application")
    print("8. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_application()
    elif choice == "2":
        view_applications()
    elif choice == "3":
        search_application()
    elif choice == "4":
        update_status()
    elif choice == "5":
        update_follow_up()
    elif choice == "6":
        show_summary()
    elif choice == "7":
        delete_application()
    elif choice == "8":
        print("Thank you for using Smart Job Application Tracker!")
        break
    else:
        print("Please choose from 1 to 8.")

# Close the database connection when the program ends
cursor.close()
db.close()
