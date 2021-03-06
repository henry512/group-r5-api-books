from fastapi import FastAPI
from src.controllers import router_books
from src.containers import Container
from fastapi.middleware.cors import CORSMiddleware

description = """
BooksApp Microservice Rest-http API. 🚀

Funcionalidades comunes:

* **Create books**.
* **Read books** .
* **Delete books** .
"""

app = FastAPI(
    title="BooksApp",
    description=description,
    version="1.0.0",
    terms_of_service="https://www.grupor5.com/terminos-y-condiciones",
    contact={
        "name": "Contact services grupo R5",
        "url": "https://www.grupor5.com/contactanos",
        "email": "soporte@grupor5.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
container = Container()
container.init_resources()
app.container = container
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router_books)
