import streamlit as st
import pandas as pd
import sqlite3
from Empdatabase import(
    create_emp_table,
    add_employee,
    get_employees,
    get_single_employee,
    update_employee,    
    delete_employee_data,
    )

#set page config
st.set_page_config(
    page_title="Employee Management system App",
    layout='wide',page_icon=":material/directions_boat:"
)

#create table
create_emp_table()
st.title("EMPLOYEE MANAGEMENT SYSTEM FORM ")
st.write("Employee Management System with complete CRUD operation using Streamlit and SQLite3" 
"")
st.write("""Welcome""")
menu=st.sidebar.selectbox(
    "Select Your Operation",
    ["Create Employee",
     "View Employee",
     "Update Employee",
     "Delete Employee"
    ""]
)

if menu=="Create Employee":
    st.header ("+ Add New Employee Here...")
    with st.form("Create Employee Form"):
        name=st.text_input("Enter your Name",placeholder="Employee Name")
        email=st.text_input ("Enter Employee Email Addresse",placeholder="Employee email address")
        department=st.selectbox("Department",[""
        "Fixture Design","Simulation","HR","Product Design","Sales"],placeholder="Department")
        Salary=st.number_input(
            "Salary",min_value=0,max_value=10000000,placeholder="Employe Salary")
        
        submit=st.form_submit_button("Add Employee")

        if submit:
            if not name or not email:
                st.error("Name and Emal are reuirred")
            else:
                try:
                    add_employee(
                        name,
                        email,
                        department,
                        Salary
                    )
                    st.success("Employee added")
                except sqlite3.IntegrityError:
                    st.error("Email already Exists...")

elif menu=="View Employee":
    st.header("All Employee Listed here")
    c=get_employees()
    if c.empty:
        st.warning(
            "No Employee available"
        )
    else:
        search=st.text_input('Search emp')
        if search:
            search_lower=search.lower()
            c=c[
                c['name'].str.lower().str.contains(search_lower,na=False)
                |
                c['department'].str.lower().str.contains(search_lower,na=False)
            ]

       #metrix
        col1, col2, col3 = st.columns(3)
        col1.metric(
                        "Total Emloyee", len(c)
                    )
        col2.metric(
                        "Average Salary", f"{c['salary'].mean():.2f}"
                    )
        col3.metric(
                        "Total Salary", f"{c['salary'].sum():.2f}"
                    )
        st.divider()
                # display data
        st.dataframe(c, width='stretch')

elif menu=="Update Employee":
    st.header('Update Employee Page')
    df=get_employees()

    if df.empty:
        st.warning('No employee')
    else:
        emp_ids=df['id'].tolist()
        emp_id=st.selectbox("select Employee Id",emp_ids)

        if emp_id:
            employee= get_single_employee(emp_id)

            if employee:
                employee_id=employee[0]
                employee_name=employee[1]
                employee_email=employee[2]
                employee_department=employee[3]
                employee_salary=employee[4]

            #st.write(employew)
                        
                departments = [
                        "CSE",
                        "EEC",
                        "Banking",
                        "Engineering",
                        "Data Science",
                        "Sales",
                        "HR",
                        "HOD"
                    ]
                current_index = departments.index(employee_department) 

                with st.form('update employee form'):
                    name = st.text_input("emp Name", value=employee_name)
                    email = st.text_input("emp Email", value=employee_email)
                    department = st.selectbox("Select Dept", departments, index=current_index)
                    salary = st.number_input("emp Salary", min_value=0.0, value=float(employee_salary), step=1000.0)
                    update_submit = (
                        st.form_submit_button("Update employee")
                    ) 

                    if update_submit:
                        try:
                            update_employee(
                                employee_id, name, email, department, salary
                            )
                            st.success("Updated..")
                        except sqlite3.InternalError:
                            st.error("Email Already Exist")    