import mysql.connector

db = mysql.connector.connect(
    host="localhost", 
    user="abhin",
    passwd="abhinaV*12",
    database="student_database"
)

mycursor = db.cursor()

#Clearing previous run
mycursor.execute("DROP TABLE StudentCourses")

mycursor.execute("DROP TABLE Students")

mycursor.execute("DROP TABLE Courses")

#Creating new instance
mycursor.execute("CREATE TABLE Students (name varchar(50), student_id int PRIMARY KEY AUTO_INCREMENT)")

mycursor.execute("CREATE TABLE Courses(name varchar(50), department varchar(50), open_seats int, course_id int PRIMARY KEY AUTO_INCREMENT)")


mycursor.execute("""CREATE TABLE StudentCourses(
                 student_id int,
                 course_id int,
                 PRIMARY KEY(student_id, course_id),
                 FOREIGN KEY (student_id) REFERENCES Students(student_id),
                 FOREIGN KEY (course_id) REFERENCES Courses(course_id)
                 
                 )""")

#Function start
#create new person

def personCreation(sName, cName):

    mycursor.execute("INSERT INTO Students (name) VALUES (%s)", (sName,))
    student_id = mycursor.lastrowid


    mycursor.execute("SELECT course_id FROM Courses WHERE name = %s", (cName,))
    course_id = mycursor.fetchone()[0]

    mycursor.execute("INSERT INTO StudentCourses (student_id, course_id) VALUES (%s, %s)", (student_id, course_id))
    db.commit()
# add courses to person
def addPersonCourses(sName, cName):
    mycursor.execute("SELECT student_id FROM Students WHERE name = %s", (sName,))
    student_id = mycursor.fetchone()[0]

    mycursor.execute("SELECT course_id FROM Courses WHERE name = %s", (cName,))
    course_id = mycursor.fetchone()[0]

    mycursor.execute("INSERT INTO StudentCourses (student_id, course_id) VALUES (%s, %s)", (student_id, course_id))
    db.commit()
#creates a new course
def courseCreation(name, department, open_seats):
    mycursor.execute("INSERT INTO Courses (name, department, open_seats) VALUES (%s, %s, %s)", (name, department, open_seats,))
    course_id = mycursor.lastrowid


#print statements

def printAll():
    print("DATABASE")
    mycursor.execute("SELECT * FROM Students")
    records = mycursor.fetchall()
    print(records)

    mycursor.execute("SELECT * FROM Courses")
    records = mycursor.fetchall()
    print(records)

    mycursor.execute("SELECT * FROM StudentCourses")
    records = mycursor.fetchall()
    print(records)

    #Final Print Statements
    print("STUDENT VALUES")

    mycursor.execute("SELECT c.course_id, c.name AS course_name, COUNT(sc.student_id) AS student_count,c.open_seats FROM StudentCourses sc JOIN Courses c ON sc.course_id = c.course_id GROUP BY sc.course_id")



    for x in mycursor:
        course_id = x[0]
        course_name= x[1]
        count = x[2]
        open_seats=x[3]

        print("\nCourse name: " + str(course_name)+"\nCount: "+str(count)+"\nOpen Seats: "+str(open_seats))
        if(count>open_seats):
            print("Shortage of: " + str(count-open_seats))
        elif(open_seats > count):
            print("Surplus of: " + str(open_seats - count))
        else:
            print("Needs are met for this class")


#Course populating

courseCreation("1212", "ITSC", 1)
courseCreation("1213", "ITSC", 3)
courseCreation("1600", "ITSC", 4)
courseCreation("2600", "ITSC", 2)
courseCreation("2175", "ITSC", 12)
courseCreation("2181", "ITSC", 6)
courseCreation("1103", "WRDS", 3)
courseCreation("1241", "MATH", 4)
courseCreation("1242", "MATH", 2)

#Populating Students
personCreation("Joe", "1212")
personCreation("Enrique", "1212")
personCreation("Johannes", "1213")
personCreation("Banana", "2600")
addPersonCourses("Banana", "1212")
personCreation("Brahms", "1212")
personCreation("PotatoMan", "1213")
personCreation("CheezWhiz", "2600")

#Main Method

leave = 0

while(leave == 0):
    inp = input("Enter option: ")


    match inp:
        #Create student
    
        case '1':
            sName = input("Student name: ")
            cName = input("Course name: ")
            personCreation(sName, cName)

        #Add course to student
        case '2':
            sName = input("Student name: ")
            cName = input("Course name: ")
            addPersonCourses(sName, cName)
        #Add courses
        case '3': 
            name = input("Name of course: ")
            department = input("Name of department: ")
            open_seats = int(input("Number of open seats: "))
            courseCreation(name, department, open_seats)
        #prints all
        case '4':
            printAll()
        case '0':
            leave = 1
            
exit()