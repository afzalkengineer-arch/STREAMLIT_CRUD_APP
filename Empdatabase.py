import sqlite3
import pandas as pd

#create db connection
def get_connection():
    conn=sqlite3.connect(
        'employee.db',
        check_same_thread=False
    )
    return conn

#create employee table
def create_emp_table():
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
         Email TEXT NOT NULL UNIQUE,
         Department TEXT NOT NULL,
        Salary DEC(10,2) NOT NULL)
    """)

    conn.commit()
    conn.close()

#add employee to the employee table
def add_employee(Name,Email,Department,Salary):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
    INSERT INTO Employees(Name,Email,Department,Salary)
    VALUES(?,?,?,?)""",(Name,Email,Department,Salary)
    )
    conn.commit()
    conn.close()


 #get employees
def get_employees():
      conn=get_connection()
      query="""
      SELECT * FROM EMPLOYEES ORDER BY id
      """
      df=pd.read_sql_query(
        query,conn
        )  
      conn.close()
      return df

#gete specifice/single employees
def get_single_employee(emp_id):
     conn=get_connection()
     cursor=conn.cursor()
     cursor.execute

     ("""
       SELECT * FROM EMPLOYEES WHERE id=?
       """, (emp_id,))
     emp=cursor.fetchone()
     conn.close()
     return emp

#Update Employee data
def update_employee(emp_id, Name, Email, Department, Salary):
     conn=get_connection()
     cursor=conn.cursor()
     cursor.execute("""
     UPDATE EMPLOYEES SET
     Name=?,
     Email=?,
     Department=?,
     Salary=?,
     WHERE id=?""", (Name,Email,Department,Salary,emp_id))
     conn.commit()
     conn.close()
     return("msg: Employee data updated successfully""")


#delte employee data
def delete_employee_data(emp_id):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
    DELETE FROM EMPLOYEES WHERE id=?
    """,(emp_id,))
    conn.commit()
    conn.close()
    return("msg: Employee data deleted successfully")