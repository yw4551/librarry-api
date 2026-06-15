from fastapi import APIRouter
from database.member_db import member_db
from database.book_db import book_db
from logs.logger import logger


router = APIRouter()


@router.get("/reports/summary")
def get_summary():
    logger.info(f"GET /reports/summary called")
    logger.info("Getting summary.")
    total_books = book_db.count_total_books()
    available_books = book_db.count_available_books()
    borrowed_books = book_db.count_borrowed_books()
    active_members = member_db.count_actives()

    logger.info("Showing summary.")
    return {
        "total_books": total_books,
        "available_books": available_books,
        "currently_borrowed": borrowed_books,
        "active_members": active_members
    }


@router.get("/reports/books-by-genre")
def get_books_by_genre_count():
    logger.info(f"GET /reports/books-by-genre called")
    logger.info("Showing books by genre.")
    rows = book_db.count_by_genre()
    return [{"Genre": row[0], "COUNT": row[1]} for row in rows]


@router.get("/reports/top-member")
def get_top_member():
    logger.info(f"GET /reports/top-member called")
    logger.info("Showing top member.")
    top_member = member_db.get_top_member()

    if not top_member:
        return {}
    
    return {"member_id": top_member[0], "borrowed": top_member[4]}
