# Library API System

## About the project

This project is an API system of a library management.  
You can add books members and pass books between members.  
You can get reports with the updated status of the books and members.  

This project uses the following technologies:
- Python
- FastAPI
- MySql

To use the system you will send HTTP requests throw the Swagger or Postman.

---
&nbsp;

## Docker MySql

To start the docker mysql database you should run the following code in the terminal:/
*note:* Make sure your docker is running before you run the command.

```bash
docker run --name library-api -e MYSQL_ROOT_PASSWORD=secret -e MYSQL_DATABASE=library_db -p 3306:3306 -d mysql:8
```

Then run this command to confirm the docker container is running

```bash
docker ps
```

---
&nbsp;

## File Structure

```text
library-api/
│
│
├── main.py
├── database/
│   ├── db_connection.py
│   ├── book_db.py
│   └── member_db.py
├── routes/
│   ├── book_routes.py
│   ├── member_routes.py
│   └── report_routes.py
├── logs/
│   ├── app.log
|   └── logger.py
│
├── README.md
├── requirements.txt
└── .gitignore
```
---
&nbsp;

# Table Structure

&nbsp;

<div style="display: flex; justify-content: center; align-items: center; flex-direction: column; gap: 100px;">
<div>

| **Books** ||||
| :---: | :---: | :---: | :---: |
| **Property** | **Type** | **Definition** | **Specials** |
| book_id | INT | The book ID | Primary key |
| title | VARCHAR | The books title | Not null, Up to 50 characters |
| author | VARCHAR | The author of the book | Not null, Up to 50 characters |
| genre | VARCHAR | The genre of the book | ENUM values, Not null |
| is_available | BOOLEAN | If the book is available | Default True |
| borrowed_by_member_id | INT or NULL | ID of how is holding the book | Default null |

</div>
<div>

| **Members** ||||
| :---: | :---: | :---: | :---: |
| **Property** | **Type** | **Definition** | **Specials** |
| member_id | INT | The member's ID | Primary key |
| name | VARCHAR | The member's name | Not null, Up to 50 characters |
| email | VARCHAR | The member's email address | Unique, Not null |
| is_active | BOOLEAN | The member can len books | Default True |
| total_borrows | INT | The total number of books his holding now | Default 0 |

</div>
</div>

---
&nbsp;

# System Rules

- Every book is created with an `is_available` value of True and `borrowed_by` value of Null.
- The `genre` must be one of the following values:
    - `Fiction`
    - `Non-Fiction`
    - `Science`
    - `History`
    - `Other`
- Every new member starts with a value of True for `is_active` and 0 for `total_borrows`.
- The `email` property in the members table must be unique.
- A member with a False value for `is-active` can't borrow books.
- A member can't have have more then 3 books by him at once.
- You can return a book only if you are register as who took the book.

---
&nbsp;

# Endpoints

<div style="display: flex; justify-content: center; align-items: center; flex-direction: column; gap: 100px;">
<div>

| **Books** ||||
| :---: | :---: | :---: | :---: |
| **Function** | **Method** | **API** | **Definition** |
| create_book(data) | POST | `/books` | Inserts a book into the table |
| get_all_books() | GET | `/books` | Returns a list of all of the books |
| get_book_by_id(book_id) | GET | `/books/{book_id}` | Returns a book passed by ID |
| update_book(book_id, data) | PUT | `/books/{book_id}` | Updates data of an existing book |
| set_available(book_id, val, member_id) | PUT | `/books/{book_id}/return/{member_id}` <br> `/books/{book_id}/borrow/{member_id}` | Updates the book is available and decrease member borrowed books |

</div>
<div>

| **Members** ||||
| :---: | :---: | :---: | :---: |
| **Function** | **Method** | **API** | **Definition** |
| create_member(data) | POST | `/members` | Creates a new member |
| get_all_members() | GET | `/members` | Returns a list of all of the members |
| get_member_by_id(member_id) | GET | `/members/{member_id}` | Returns the member's data |
| update_member(member_id, data) | PUT | `/members/{member_id}` | Updates data of an existing member |
| deactivate_member(member_id) | PUT | `/members/{member_id}/deactivate` | Deactivates a member |
| activate_member(member_id) | PUT | `/members/{id}/activate` | Activates a member |
| increment_borrows(member_id) | PUT | `/books/{book_id}/borrow/{member_id}` | Increases a members books by 1 |

</div>
<div>

| **Reports** ||||
| :---: | :---: | :---: | :---: |
| **Function** | **Method** | **API** | **Definition** |
| count_total_books | GET | `/reports/summary` | Counts all of the books in the DB |
| count_available_books() | GET | `/reports/summary` | Counts the amount of books that are available |
| count_borrowed_books() | GET | `/reports/summary` | Counts the amount of books that are not available |
| count_by_genre(genre) | GET | `/reports/book-by-genre` | Counts the amount of books within a genre |
| count_active_borrows_by_member(member_id) | GET | `/books/{id}/borrow/{member_id}` | Counts the amount of books the member is holding |
| count_active_members() | GET | `/reports/summary` | Counts how many active members are they |
| get_top_member() | GET | `/reports/top-member` | Returns the member with to most borrows |

</div>
</div>

---
&nbsp;

# Workflow

<div style="display: flex; justify-content: center;">

![aaa](library-diagram.svg)

</div>

---
&nbsp;

# How to run

To run the project you should run the following code in the terminal to install the required libraries needed for the project.
**Note:** make sure you are in the project's folder.

```bash
pip install -r requirements.txt
```

Now run the project by running the following command in the terminal:

```bash
uvicorn main:app
```

Then go to the following page in your browser:

```text
https://127.0.0.1:8000/docs
```

Now you are all set.