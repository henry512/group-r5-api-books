from fastapi import FastAPI, APIRouter
from .controllers import router_books


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

# Adding router controllers
api_router = APIRouter()
api_router.include_router(router_books, prefix="/books", tags=["Books"])

app.include_router(api_router)
