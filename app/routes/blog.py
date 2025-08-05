from app.interfaces.main import Route as RouteInstance
from fastapi import APIRouter, Query, HTTPException, File, Form, UploadFile, status
from typing import Annotated
from app.schemas.main import FilterParams, Item


class Route(RouteInstance):

    def __init__(self):
        self.router = APIRouter(prefix="/blogs", tags=["blogs"])
        self.setup_routes()
        self.blogs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        self.items = {
            "foo": {"name": "Foo", "price": 50.2},
            "bar": {
                "name": "Bar",
                "description": "The bartenders",
                "price": 62,
                "tax": 20.2,
            },
            "baz": {
                "name": "Baz",
                "description": None,
                "price": 50.2,
                "tax": 10.5,
                "tags": [],
            },
        }

    def setup_routes(self):

        @self.router.post(
            "/create",
            status_code=status.HTTP_201_CREATED,
            summary="should return create blog",
        )
        def createBlog(item: Annotated[Item, Form()]):
            result = self.items.get(item.name)
            if result:
                raise HTTPException(400, detail="duplicate found")
            else:
                self.items.update(
                    {
                        item.name: {
                            "name": item.name,
                            "description": item.description,
                            "price": item.price,
                            "tax": item.tax,
                            "tags": item.tags,
                        }
                    }
                )

            return {"message": "item added successfully", "item": item}

        @self.router.post("/upload")
        async def uploadFiles(files: Annotated[list[UploadFile], File()]):
            arrays: list[str | None] = []

            for file in files:
                for fil in arrays:
                    if fil == file.filename:
                        raise HTTPException(400, detail="file duplicate")
                arrays.append(file.filename)

            return {"filenames": [file for file in arrays]}

        @self.router.get("/")
        def getSpecificBlogs(item: Annotated[str, Query()]):
            result = self.items.get(item)
            if result:
                return {"item": f"{self.items[item]}"}
            else:
                raise HTTPException(404, detail="item not found")

        @self.router.get("/{id}/comments")
        def getComments(id, filter_query: Annotated[FilterParams, Query()]):
            limit = len(self.blogs) - filter_query.limit
            blogs = []

            if limit < -1:
                raise HTTPException(400, detail="the limit exceeds the number of blogs")
            for blog in range(0, len(self.blogs) - limit):
                blogs.append(blog)
            return blogs

        @self.router.delete("/delete")
        def deleteItem(item: Annotated[str, Query()]):
            result = self.items.get(item)

            if not result:
                raise HTTPException(404, detail="item not found")
            else:
                self.items.pop(item)
                return {
                    "message": "item deleted successfully",
                    "item": f"{self.items.get(item)}",
                }

        @self.router.put("/update")
        def updateItem(item: Annotated[str, Query()], update: Annotated[Item,Form()]):
            result = self.items.get(item)

            if not result:
                raise HTTPException(404, detail="item not found")
            else:
                self.items.update(
                    {
                        update.name: {
                            "name": update.name,
                            "description": update.description,
                            "price": update.price,
                            "tax": update.tax,
                        }
                    }
                )
                return {
                    "message": "item updated successfully",
                    "item": f"{self.items.get(update.name)}",
                }
