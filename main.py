from random import randrange

from fastapi import Body, FastAPI
from pydantic import BaseModel
from fastapi import Response, status, HTTPException


app = FastAPI()

empty_list = [{'title': 'about a man', 'content': 'Thiru is a good boy', 'published': False, 'id': 79},{'title': 'man_1', 'content': 'Thiru is a good boy', 'published': False, 'id': 77}]
#This is the model from pydantic which helps ue to validate the input what user is providing
class Post(BaseModel): 
    title : str
    content : str
    published : bool = True

@app.get("/posts", status_code = status.HTTP_200_OK)
def sample():
    return empty_list


#it will get the body from the uer input and save that as dictionary
# @app.post("/create_post")
# def create_post(info : dict = Body()):
#     return(info)



#WE called the class called Post adn saved to variable adn asking them to print and return it will validate for us
@app.post("/create_post")
def create_post(value: Post): # type: ignore
    # print(value)
    # print(value.content)
    value = value.dict()
    value['id']= randrange(0, 100000)
    output = empty_list.append(value)
    print(output)
    return(output)

def find_post(id):
    for i in empty_list:
        print(i)
        if i['id'] == id:
            print(i)
            return i


def finding_index(id):
    for index, i in enumerate(empty_list):
        if i['id'] == id:
            return index



@app.get("/get_specific_post/{id}")
def get_specific_post(id : int, response : Response):
    print(id)
    retreived_post = find_post(id)
    if not retreived_post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"this {id} is not found"}
    return retreived_post

@app.delete("/delete_post/{id}")
def delete_post(id : int):
    print(id)
    index = finding_index(id)
    if index == None:
        return Response(status_code=status.HTTP_404_NOT_FOUND, detail ="The given {id} is not available")
    
    empty_list.pop(index)
    return Response(status_code=status.HTTP_200_OK)

@app.put("/update_post/{id}")
def update_post(id: int, update_post : Post):
    print("this is the update function")
    index = finding_index(id)
    print(index)
    # if index == None:
    #     return Response(status_code=status.HTTP_404_NOT_FOUND, detail ="The given {id} is not available")
    

    post_dict = update_post.dict()
    post_dict['id'] = id
    empty_list[index] = post_dict 
    return {"mesg": " this is update func"}