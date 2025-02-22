from random import randrange

from fastapi import Body, FastAPI
from pydantic import BaseModel
from fastapi import Response, status


app = FastAPI()


#This is the model from pydantic which helps ue to validate the input what user is providing
class Post(BaseModel): 
    title : str
    content : str
    published : bool = True

@app.get("/posts")
def sample():
    return empty_list


#it will get the body from the uer input and save that as dictionary
@app.post("/create_post")
def create_post(info : dict = Body()):
    return(info)

empty_list = [{'title': 'about a man', 'content': 'Thiru is a good boy', 'published': False, 'id': 79},{'title': 'man_1', 'content': 'Thiru is a good boy', 'published': False, 'id': 77}]

#WE called the class called Post adn saved to variable adn asking them to print and return it will validate for us
@app.post("/using_pydantic")
def create_post(value: Post):
    # print(value)
    # print(value.content)
    value = value.dict()
    value['id']= randrange(0, 100000)
    empty_list.append(value)
    print(empty_list)
    return(value)

def find_post(id):
    for i in empty_list:
        print(i)
        if i['id'] == id:
            print(i)
            return i

@app.get("/get_specific_post/{id}")
def get_specific_post(id : int, response : Response):
    print(id)
    retreived_post = find_post(id)
    if not retreived_post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"this {id} is not found"}
    return retreived_post
