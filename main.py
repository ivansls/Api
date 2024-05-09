from fastapi import FastAPI
import psycopg2
import hashlib

app = FastAPI()
conn = psycopg2.connect(dbname="Magazine", user="root", password="NasSidAdmin789", host="109.238.83.39",
                            port="5665")

# conn.close()
name = "Time"
@app.get("/")
async def root():
    a = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM client_type")
    # print(cursor.fetchall())
    for i in cursor.fetchall():
        print(i[1])
        a.append({
            "value" : i[0],
            "name" : i[1]
        })
    return a


# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}


@app.post("/auth/{login}/{password}/{name}/{salt}")
async def register_user(login: str, password:str, name:str, salt:str):
    cursor = conn.cursor()

    passwd = password.encode()
    solt = salt.encode()
    dk = hashlib.pbkdf2_hmac('sha256', passwd, solt, 100000)

    user = (login, dk.hex(), name)
    cursor.execute("INSERT INTO users (login, password, name, client_type_id, discount_id, visit_numbers, exist) VALUES (%s, %s, %s, 1, 1, 0, true)", user)

    conn.commit()
    print("Данные добавлены")
    cursor.close()
    return {"message": f"Hello {name}"}
