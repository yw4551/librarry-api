from fastapi import FastAPI
from routes import book_routes, member_routes, report_routes


app = FastAPI()


app.include_router(book_routes.router)
app.include_router(member_routes.router)
app.include_router(report_routes.router)
