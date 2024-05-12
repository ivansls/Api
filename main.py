from fastapi import FastAPI, Depends
from fastapi_pagination import Page, Params

import psycopg2
import hashlib

app = FastAPI()
conn = psycopg2.connect(dbname="Magazine", user="root", password="NasSidAdmin789", host="109.238.83.39",
                        port="5665")

# conn.close()
name = "Time"


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


# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}

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
    return {"message": f"Hello {name}"}


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
        return {"user": "NO", "login": "NO"}


@app.get("/get_user/{login}")
async def get_user(login: str):
    cursor = conn.cursor()
    cursor_client_type = conn.cursor()
    cursor_discount = conn.cursor()
    client_type = ""
    discount = ""

    cursor.execute(f"SELECT * FROM users where login = \'{login}\'")
    a = cursor.fetchall()

    cursor_client_type.execute(f"SELECT name FROM client_type where id_client_type = \'{a[0][4]}\'")
    client_type = cursor_client_type.fetchall()[0][0]

    cursor_discount.execute(f"SELECT value FROM discount_ where id_discount = \'{a[0][5]}\'")
    discount = cursor_discount.fetchall()[0][0]

    cursor.close()
    cursor_discount.close()
    cursor_client_type.close()
    return {
        "id": a[0][0],
        "login": a[0][1],
        "password": a[0][2],
        "name": a[0][3],
        "client_type": [client_type, a[0][4]],
        "discount": [discount, a[0][5]],
        "visit_number": a[0][6],
        "exist": a[0][7]
    }


@app.put("/update_user/{login}/{login_new}/{password}/{name}/{salt}/{client_type}/{discount_id}/{exist}")
async def update_user(login: str, login_new: str, password: str, salt: str, name: str, client_type: int,
                      discount_id: int, exist: bool):
    cursor = conn.cursor()
    passwd = password.encode()
    solt = salt.encode()
    dk = hashlib.pbkdf2_hmac('sha256', passwd, solt, 100000)

    status = "YES"
    try:
        cursor.execute(
            f"UPDATE users SET login = \'{login_new}\', password = \'{dk.hex()}\', name = \'{name}\', client_type_id = \'{client_type}\', discount_id = \'{discount_id}\', exist = \'{exist}\' where login = \'{login}\'")
    except:
        status = "NO"
    conn.commit()
    cursor.close()

    return {"STATUS": status}


# @app.delete("/delete_user/{login}")
# async def delete_user(login : str):
#     cursor = conn.cursor()
#
#     status = "YES"
#     # try:
#     #     cursor.execute(f"DELETE FROM users WHERE login = \'{login}\'")
#     # except:
#     #     status = "NO"
#
#     cursor.execute(f"DELETE FROM users WHERE login = \'{login}\'")
#     conn.commit()
#     cursor.close()
#
#     return {"STATUS": status}


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
        a.append({tabl_id: i[1::][0]})
    cursor.close()
    return a


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


@app.put("/update/{table}/{id}/value")
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
                      "service_id": [i[1], service_id],
                      "user_id": [i[2], user_id],
                      "employee_id": [i[3], employee_id],
                      "time_id": [i[4], time_id],
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
                      "job_title_id": [i[4], job_id],
                      "exist": i[5]})
    return a


@app.post("/add_record_or_eployee/{table}/{")
async def add_record_or_eployee(table: str):
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

    return a
