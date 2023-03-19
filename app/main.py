import os
import time
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

load_dotenv()

dbname=os.getenv('DATABASE')
host=os.getenv('HOST')
user=os.getenv('USER')

#connect to DB
while True:
    try:
        conn = psycopg2.connect(f"dbname={dbname} user={user} host={host} port=5432", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful')
        break
    except Exception as error:
        print("Connecting to databse failed")
        print("Error: ", error)
        time.sleep(2)

app = FastAPI()

# define schema 
class Post(BaseModel):
    title: str
    content: str 
    published: bool = True
    # rating: int | None = None # optional so if not provided will be None

@app.get("/")
def root():
    return {"message": "Welcome to Rahuls Social Media Posts API"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM fastapi.posts;""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):    
    cursor.execute("""INSERT INTO fastapi.posts(title, content, published) VALUES (%s, %s, %s) RETURNING *;""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    
    return {"data": new_post}


# @app.get("/posts/latest") # this needs to go before id one as it goes top down
# def get_latest_posts():
#     return {"data": my_posts[-1]}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM fastapi.posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    cursor.execute("""DELETE FROM fastapi.posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    cursor.execute("""UPDATE fastapi.posts SET title = %s, content = %s, published = %s where id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return {"data": updated_post}
    
    
