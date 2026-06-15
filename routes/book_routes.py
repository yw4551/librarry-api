from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, Optional
from database.book_db import book_db
from database.member_db import member_db
from logs.logger import logger


router = APIRouter()


class CreateBook(BaseModel):
    title: str = Field(..., max_length=50)
    author: str = Field(..., max_length=50)
    genre: Literal["Fiction", "Non-Fiction", "Science", "History", "Other"]


class UpdateBook(BaseModel):
    title: Optional[str] = Field(None, max_length=50)
    author: Optional[str] = Field(None, max_length=50)
    genre: Optional[Literal["Fiction", "Non-Fiction", "Science", "History", "Other"]]


@router.post("/books", status_code=201)
def create_book(data: CreateBook):
    logger.info(f"POST /books called")
    try:
        book_db.create_book(data.model_dump(mode="json"))
        logger.info("Book created successfully.")
        return {"message": "Book created successfully."}
    except ValueError:
        logger.warning("Missing some data.")
        raise HTTPException(status_code=400, detail="Error: Missing some values.")


@router.get("/books")
def get_all_books():
    logger.info(f"GET /books called")
    return book_db.get_books()


@router.get("/books/{book_id}")
def get_book_by_id(book_id: int):
    logger.info(f"GET /books/{book_id} called")
    book = book_db.get_book(book_id)
    if not book:
        logger.warning(f"Book with ID {book_id} not found.")
        raise HTTPException(status_code=404, detail="Error: Book not found.")
    return book


@router.patch("/books/{book_id}")
def update_book(book_id: int, data: UpdateBook):
    logger.info(f"PATCH /books/{book_id} called")
    updated_data = data.model_dump(exclude_unset=True)
    if not updated_data:
        logger.warning("No changes to update were found.")
        raise HTTPException(status_code=400, detail="Error: No fields to update.")

    if book_db.get_book(book_id) is None:
        logger.warning(f"Book with ID {book_id} not found.")
        raise HTTPException(status_code=404, detail="Error: Book not found.")

    updated = book_db.update(book_id, updated_data)
    if not updated:
        logger.warning("No changes to update were found.")
        raise HTTPException(status_code=400, detail="Error: No fields to update.")

    logger.info("Changes were updated successfully.")
    return {"Message": "Book updated successfully."}


@router.patch("/books/{book_id}/borrow/{member_id}")
def borrow_book(book_id: int, member_id: int):
    logger.info(f"PATCH /books/{book_id}/borrow/{member_id} called")
    book = book_db.get_book(book_id)
    if not book:
        logger.warning(f"Book with ID {book_id} not found.")
        raise HTTPException(status_code=404, detail="Book not found.")

    if not book[4]:
        logger.warning(f"Book with ID {book_id} is already borrowed.")
        raise HTTPException(status_code=400, detail="Book is already borrowed.")

    member = member_db.get_member(member_id)
    if not member:
        logger.warning(f"Member with ID {member_id} not found.")
        raise HTTPException(status_code=404, detail="Member not found.")

    if not member[3]:
        logger.warning(f"Member with ID {member_id} is inactive.")
        raise HTTPException(status_code=400, detail="Member is inactive.")

    borrows = book_db.count_active_borrows_by_member(member_id)
    if borrows >= 3:
        logger.warning(f"Member with ID {member_id} has reached maximum borrows.")
        raise HTTPException(status_code=400, detail="Member has reached maximum borrows")

    result = book_db.set_availability(book_id, False, member_id)
    if not result:
        logger.warning(f"Book with ID {book_id} or member with ID {member_id} not found.")
        raise HTTPException(status_code=404, detail="Member or book not found.")

    member_db.increment_borrows(member_id)
    logger.info("Borrow completed successfully.")
    return {"message": "Borrow completed successfully."}


@router.patch("/books/{book_id}/return/{member_id}")
def return_book(book_id: int, member_id: int):
    logger.info(f"PATCH /books/{book_id}/return/{member_id} called")
    book = book_db.get_book(book_id)
    if not book:
        logger.warning(f"Book with ID {book_id} not found.")
        raise HTTPException(status_code=404, detail="Book not found.")

    if book[4]:
        logger.warning("The book is already available in the library.")
        raise HTTPException(status_code=400, detail="Book is not borrowed")

    if book[5] != member_id:
        logger.warning("This book was not borrowed by the member.")
        raise HTTPException(status_code=400, detail="Book is not borrowed by this member")

    result = book_db.set_availability(book_id, True, None)
    if not result:
        logger.error(f"Book with ID {book_id} or member with ID {member_id} not found.")
        raise HTTPException(status_code=404, detail="Member or book not found.")

    logger.info(f"Book ID {book_id} returned successfully.")
    return {"message": "Return completed successfully."}
