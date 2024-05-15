from fastapi import FastAPI, Depends
from fastapi_pagination import Page, Params
import numpy as np
import psycopg2
import hashlib

app = FastAPI()
conn = psycopg2.connect(dbname="Magazine", user="root", password="NasSidAdmin789", host="109.238.83.39",
                        port="5665")

# conn.close()
name = "Time"

@app.get("/getHash/{password}/{salt}")
async def getHash(password: str, salt: str):
    passwd = password.encode()
    solt = salt.encode()
    dk = hashlib.pbkdf2_hmac('sha256', passwd, solt, 100000)
    return dk.hex()


@app.get("/")
async def root(
        params: Params = Depends()
):
    a = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM client_type")
    # print(cursor.fetchall())
    for i in cursor.fetchall():
        print(i[1])
        a.append({
            "value": i[0],
            "name": i[1]
        })
    return a


# --USERS---------------------------------------
@app.post("/register_user/{login}/{password}/{name}/{salt}")
async def register_user(login: str, password: str, name: str, salt: str):
    cursor = conn.cursor()

    passwd = password.encode()
    solt = salt.encode()
    dk = hashlib.pbkdf2_hmac('sha256', passwd, solt, 100000)

    user = (login, dk.hex(), name)
    cursor.execute(
        "INSERT INTO users (login, password, name, client_type_id, discount_id, visit_numbers, exist) VALUES (%s, %s, %s, 1, 1, 0, true)",
        user)

    conn.commit()
    print("Данные добавлены")
    cursor.close()
    return {"STATUS": "YES"}


@app.get("/auth/{login}/{password}/{salt}")
async def authorization_user(login: str, password: str, salt: str):
    cursor = conn.cursor()
    passwd = password.encode()
    solt = salt.encode()
    dk = hashlib.pbkdf2_hmac('sha256', passwd, solt, 100000)
    cursor.execute(f"SELECT password, name FROM users where login = \'{login}\' AND  password = \'{dk.hex()}\'")

    try:
        return {"user": cursor.fetchall()[0][1], "login": login}
    except IndexError:
        return {"STATUS": "NO"}


@app.get("/get_user/{login}")
async def get_user(login: str):
    cursor = conn.cursor()
    client_type = ""
    discount = ""
    a = []
    if login == "none":
        cursor.execute(f"SELECT * FROM users")
        for i in cursor.fetchall():
            a.append({
                "id_user": i[0],
                "login": i[1],
                "password": i[2],
                "name": i[3],
                "client_type_id": i[4],
                "discount_id": i[5],
                "visit_numbers": i[6],
                "exist": i[7]
            })
    else:
        cursor.execute(f"SELECT * FROM users where login = \'{login}\'")
        for i in cursor.fetchall():
            a.append({
                "id_user": i[0],
                "login": i[1],
                "password": i[2],
                "name": i[3],
                "client_type_id": i[4],
                "discount_id": i[5],
                "visit_numbers": i[6],
                "exist": i[7]
            })

        cursor.close()
    return a


@app.put("/update_user/{id}/{login}/{password}/{name}/{salt}/{client_type}/{discount_id}/{exist}")
async def update_user(id: str,login: str,  password: str, salt: str, name: str, client_type: int,
                      discount_id: int, exist: bool):
    cursor = conn.cursor()
    passwd = password.encode()
    solt = salt.encode()
    dk = hashlib.pbkdf2_hmac('sha256', passwd, solt, 100000)

    status = "YES"
    try:
        cursor.execute(
            f"UPDATE users SET login = \'{login}\', password = \'{dk.hex()}\', name = \'{name}\', client_type_id = \'{client_type}\', discount_id = \'{discount_id}\', exist = \'{exist}\' where id_user = \'{id}\'")
    except:
        status = "NO"
    conn.commit()
    cursor.close()

    return {"STATUS": status}


# --Client_type--discount_--time_--job_title


@app.get("/get/{table}/{id}")
async def getFourTable(table: str, id: int):
    cursor = conn.cursor()
    tabl_id = ""
    if table == "client_type":
        tabl_id = "id_client_type"

    elif table == "discount_":
        tabl_id = "id_discount"

    elif table == "time_":
        tabl_id = "id_time"

    elif table == "job_title":
        tabl_id = "id_job_title"

    if id > 500:
        cursor.execute(f"SELECT * FROM {table}")
    else:
        cursor.execute(f"SELECT * FROM {table} where {tabl_id} = \'{id}\'")
    a = []
    for i in cursor.fetchall():
        a.append(i)
    cursor.close()

    b = []

    for j in a:
        if table == "client_type":
            b.append({
                "id_client_type": j[0],
                "name": j[1]
            })


        elif table == "discount_":
            b.append({
                "id_discount": j[0],
                "value": j[1]
            })

        elif table == "time_":
            b.append({
                "id_time": j[0],
                "time": j[1]
            })

        elif table == "job_title":
            b.append({
                "id_job_title": j[0],
                "name": j[1]
            })

    return b


@app.post("/add/{table}/{input_text}")
async def addFourTable(table: str, input_text: str):
    cursor = conn.cursor()
    tabl_id = ""
    if table == "client_type":
        tabl_id = "name"

    elif table == "discount_":
        tabl_id = "value"
        cursor.execute(f"INSERT INTO {table} ({tabl_id}) VALUES ({input_text})")
        conn.commit()
        cursor.close()
        return {"status": "YES"}

    elif table == "time_":
        tabl_id = "time"

    elif table == "job_title":
        tabl_id = "name"

    cursor.execute(f"INSERT INTO {table} ({tabl_id}) VALUES (\'{input_text}\')")
    conn.commit()
    cursor.close()
    return {"status": "YES"}


@app.delete("/dell/{table}/{id}")
async def delFourTable(table: str, id: str):
    cursor = conn.cursor()
    tabl_id = ""
    if table == "client_type":
        tabl_id = "id_client_type"

    elif table == "discount_":
        tabl_id = "id_discount"

    elif table == "time_":
        tabl_id = "id_time"

    elif table == "job_title":
        tabl_id = "id_job_title"

    cursor.execute(f"DELETE FROM {table} {tabl_id} WHERE {tabl_id} = {id}")
    conn.commit()
    cursor.close()
    return {"status": "YES"}


@app.put("/update/{table}/{id}/{value}")
async def updateFourTable(table: str, id: str, value: str):
    cursor = conn.cursor()
    tabl_id = ""
    tabl_value = ""
    if table == "client_type":
        tabl_id = "id_client_type"
        tabl_value = "name"

    elif table == "discount_":
        tabl_id = "id_discount"
        tabl_value = "value"
        cursor.execute(f"UPDATE {table} SET {tabl_value} = {value} WHERE {tabl_id} = {id}")
        conn.commit()
        cursor.close()
        return {"status": "YES"}

    elif table == "time_":
        tabl_id = "id_time"
        tabl_value = "time"

    elif table == "job_title":
        tabl_id = "id_job_title"
        tabl_value = "name"

    cursor.execute(f"UPDATE {table} SET {tabl_value} = \'{value}\' WHERE {tabl_id} = {id}")
    conn.commit()
    cursor.close()
    return {"status": "YES"}


# --record_--employee_--

@app.get("/get_record_or_eployee/{table}/{id}")
async def get_record_or_eployee(table: str, id: int):
    cursor = conn.cursor()
    cursor_service = conn.cursor()
    cursor_user = conn.cursor()
    cursor_employe = conn.cursor()
    cursor_time = conn.cursor()
    cursor_job_title = conn.cursor()
    tabl_id = ""
    a = []
    if table == "record_":
        tabl_id = "id_record"

    elif table == "employee_":
        tabl_id = "id_employee"
    if id > 500:
        cursor.execute(f"SELECT * FROM {table}")
    else:
        cursor.execute(f"SELECT * FROM {table} where {tabl_id} = \'{id}\'")

    if table == "record_":
        cursor_service.execute(f"SELECT * FROM services_")
        cursor_user.execute(f"SELECT * FROM users")
        cursor_employe.execute(f"SELECT * FROM employee_")
        cursor_time.execute(f"SELECT * FROM time_")
        service_id = ""
        user_id = ""
        employee_id = ""
        time_id = ""

        cursor_service_ft = cursor_service.fetchall()
        cursor_user_ft = cursor_user.fetchall()
        cursor_employe_ft = cursor_employe.fetchall()
        cursor_time_ft = cursor_time.fetchall()

        for i in cursor.fetchall():
            for j in cursor_service_ft:
                if j[0] == i[1]:
                    service_id = j[1]

            for k in cursor_user_ft:
                if k[0] == i[2]:
                    user_id = k[1]

            for m in cursor_employe_ft:
                if m[0] == i[3]:
                    employee_id = m[1]

            for t in cursor_time_ft:
                if t[0] == i[4]:
                    time_id = t[1]

            a.append({"id_record": i[0],
                      "service_id": i[1],
                      "user_id": i[2],
                      "employee_id": i[3],
                      "time_id": i[4],
                      "date_record": i[5]})

    elif table == "employee_":
        cursor_job_title.execute(f"SELECT * FROM job_title")
        job_id = ""
        cursor_job_title_ft = cursor_job_title.fetchall()
        for i in cursor.fetchall():
            for j in cursor_job_title_ft:
                if j[0] == i[4]:
                    job_id = j[1]

            a.append({"id_employee": i[0],
                      "login": i[1],
                      "password": i[2],
                      "name": i[3],
                      "job_title_id": i[4],
                      "exist": i[5]})
    cursor.close()
    cursor_service.close()
    cursor_user.close()
    cursor_employe.close()
    cursor_time.close()
    cursor_job_title.close()
    return a


@app.post(
    "/add_record_or_eployee/{table}/{service_id_or_login}/{user_id_or_password}/{employee_id_or_name}/{time_id_or_job_title_id}/{date_record_or_exist}/{salt}")
async def add_record_or_eployee(table: str, service_id_or_login: str, user_id_or_password: str,
                                employee_id_or_name: str, time_id_or_job_title_id: str, date_record_or_exist: str,
                                salt: str):
    cursor = conn.cursor()
    tabl_id = ""

    if table == "record_":
        tabl_id = "id_record"
        rec = (
        service_id_or_login, user_id_or_password, employee_id_or_name, time_id_or_job_title_id, date_record_or_exist)
        cursor.execute(
            f"INSERT INTO {table} (service_id, user_id, employee_id, time_id, date_record) VALUES (%s, %s, %s, %s, %s)",
            rec)


    elif table == "employee_":
        tabl_id = "id_employee"
        passwd = user_id_or_password.encode()
        solt = salt.encode()
        dk = hashlib.pbkdf2_hmac('sha256', passwd, solt, 100000)
        empl = (service_id_or_login, dk.hex(), employee_id_or_name, time_id_or_job_title_id, date_record_or_exist)
        cursor.execute(
            f"INSERT INTO {table} (login, password, name, job_title_id, exist) VALUES (%s, %s, %s, %s, %s)",
            empl)
    conn.commit()
    cursor.close()

    return {"STATUS": "YES"}


@app.put(
    "/update_record_or_eployee/{table}/{id}/{service_id_or_login}/{user_id_or_password}/{employee_id_or_name}/{time_id_or_job_title_id}/{date_record_or_exist}/{salt}")
async def update_record_or_eployee(table: str, id: str, service_id_or_login: str, user_id_or_password: str,
                                   employee_id_or_name: str, time_id_or_job_title_id: str, date_record_or_exist: str,
                                   salt: str):
    cursor = conn.cursor()
    tabl_id = ""

    if table == "record_":
        tabl_id = "id_record"
        cursor.execute(
            f"UPDATE {table} SET service_id = {service_id_or_login}, user_id = {user_id_or_password}, employee_id = {employee_id_or_name}, time_id = {time_id_or_job_title_id}, date_record = \'{date_record_or_exist}\' WHERE {tabl_id} = {id}")


    elif table == "employee_":
        tabl_id = "id_employee"
        passwd = user_id_or_password.encode()
        solt = salt.encode()
        dk = hashlib.pbkdf2_hmac('sha256', passwd, solt, 100000)
        cursor.execute(
            f"UPDATE {table} SET login = \'{service_id_or_login}\', password = \'{dk.hex()}\', name = \'{employee_id_or_name}\', job_title_id = {time_id_or_job_title_id}, exist = {date_record_or_exist} WHERE {tabl_id} = {id}")

    conn.commit()
    cursor.close()

    return {"STATUS": "YES"}


@app.put("/delete_record_or_eployee/{table}/{id}/{dopparam}")
async def delete_record_or_eployee(table: str, id: str, dopparam: str):
    cursor = conn.cursor()
    tabl_id = ""

    if table == "record_":
        tabl_id = "id_record"
        cursor.execute(f"DELETE FROM {table} {tabl_id} WHERE {tabl_id} = {id}")

    elif table == "employee_":
        tabl_id = "id_employee"
        if (dopparam == "1"):
            cursor.execute(f"DELETE FROM {table} {tabl_id} WHERE {tabl_id} = {id}")
        else:
            cursor.execute(
                f"UPDATE {table} SET exist = false WHERE {tabl_id} = {id}")

    conn.commit()
    cursor.close()

    return {"STATUS": "YES"}


#--services_

@app.get("/getServices")
async def getServices(params: Params = Depends()):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM services_")
    a = []
    for i in cursor.fetchall():
        a.append(i)

    chunks = [a[i:i + params.size] for i in range(0, len(a), params.size)]
    cursor.close()

    b = []
    for j in chunks[params.page - 1]:
        b.append({
            "id_service": j[0],
            "name": j[1],
            "coast": j[2]
        })
    return b


@app.get("/getServices_id/{id}")
async def getServicesId(id: int):
    cursor = conn.cursor()
    if id > 500:
        cursor.execute("SELECT * FROM services_")
    else:
        cursor.execute(f"SELECT * FROM services_ where id_service = {id}")
    a = []
    for i in cursor.fetchall():
        a.append({
            "id_service": i[0],
            "name": i[1],
            "coast": i[2]
        })
    cursor.close()
    return a



@app.post("/addServices/{name}/{coast}")
async def addServicesId(name: str, coast: str):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO services_ (name, coast) values (\'{name}\', \'{coast}\')")
    conn.commit()
    cursor.close()
    return {"STATUS": "YES"}


@app.put("/updateServices/{id}/{name}/{coast}")
async def updateServicesId(id: str, name: str, coast: str):
    cursor = conn.cursor()
    cursor.execute(f"UPDATE services_ set name = \'{name}\', coast = \'{coast}\' where id_service = {id}")
    conn.commit()
    cursor.close()
    return {"STATUS": "YES"}


@app.delete("/deleteServices/{id}")
async def deleteServicesId(id: str):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM services_ WHERE  id_service = {id}")
    conn.commit()
    cursor.close()
    return {"STATUS": "YES"}


#--check_----

@app.get("/get_check/{id}")
async def getcheck(id: str):
    cursor = conn.cursor()
    if id == "-1":
        cursor.execute(f"SELECT * FROM check_")
    else:
        cursor.execute(f"SELECT * FROM check_ where id_check = {id}")

    a = []
    for i in cursor.fetchall():
        a.append({
            "id_check": i[0],
            "record_id": i[1],
            "coast": i[2],
            "payment": i[3]
        })
    cursor.close()
    return a


@app.post("/add_check/{record_id}/{coast}/{payment}")
async def add_check(record_id: str, coast: str, payment: str):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO check_ (record_id, coast, payment) values ({record_id}, {coast}, \'{payment}\')")
    conn.commit()
    cursor.close()
    return {"STATUS": "YES"}


@app.put("/update_check/{id}/{record_id}/{coast}/{payment}")
async def update_check(id: str, record_id: str, coast: str, payment: str):
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE check_ set record_id = {record_id}, coast = {coast}, payment = \'{payment}\' where id_check = {id}")
    conn.commit()
    cursor.close()
    return {"STATUS": "YES"}


@app.put("/delete_check/{id}")
async def delete_check(id: str):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM check_ WHERE  id_check = {id}")
    conn.commit()
    cursor.close()
    return {"STATUS": "YES"}
