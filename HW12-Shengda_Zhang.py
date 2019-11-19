from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/instructor_summary')
def instructors_database():
    dbpath = "810_startup.db"
    try:
        db = sqlite3.connect(dbpath)
    except sqlite3.OperationalError:
        return f"Error: unable to open database at {dbpath}"
    else:
        query = "select i.CWID, i.Name, i.Dept, g.Course, count(*) as Num_of_Students  \
                from instructors i left join grades g on i.CWID=g.InstructorCWID group by g.Course, i.CWID"

        data = [{"cwid": cwid, "name": name, "dept": dept, "course": course, "number_of_students": nums}
                for cwid, name, dept, course, nums in db.execute(query)]

        db.close()

        return render_template("parameters.html",
                               title= 'Instructors Summary',
                               table_title= 'Number of students by course and instructor',
                               instructors= data)

app.run(debug=True)