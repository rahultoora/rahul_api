from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favourite foods", "content": "I like pizza", "id": 2}]

# define schema 
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

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):    
    post_dict= post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": post_dict}


# @app.get("/posts/latest") # this needs to go before id one as it goes top down
# def get_latest_posts():
#     return {"data": my_posts[-1]}

@app.get("/posts/{id}")
async def get_post(id: int):
    post = next((post for post in my_posts if post['id'] == id), None)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    
    post = next((post for post in my_posts if post['id'] == id), None)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    
    index = next((index for index, post in enumerate(my_posts) if post['id'] == id), None)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
    
    
