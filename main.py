from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange

app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favourite foods", "content": "I like pizza", "id": 2}]

class Post(BaseModel):
    title: str
    content: str 
    published: bool = True
    rating: int | None = None # optinal so if not provided will be None

@app.get("/")
def root():
    return {"message": "Welcome to Rahuls Social Media Posts API"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):    
    post_dict= post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
async def get_posts(id: int):
    post = next(post for post in my_posts if post['id'] == id)
    return {"data": post}
