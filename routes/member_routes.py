from fastapi import APIRouter
from database.member_db import member_db
from pydantic import BaseModel, Field
from fastapi import HTTPException
from typing import Optional
from logs.logger import logger
import mysql.connector


router = APIRouter()


class CreateMember(BaseModel):
    name: str = Field(..., max_length=50)
    email: str = Field(...)


class UpdateMember(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None)


@router.post("/members")
def create_member(data: CreateMember):
    logger.info(f"POST /members called")
    try:
        member_db.create(data.model_dump(mode="json"))
        logger.info(f"Member created successfully.")
        return {"message": "Member created successfully."}
    except ValueError:
        logger.warning("Some data is missing.")
        raise HTTPException(status_code=400, detail="Error: Missing some values.")
    except mysql.connector.IntegrityError:
        logger.warning("Email is in use already.")
        raise HTTPException(status_code=409, detail="Email in use.")


@router.get("/members")
def get_all_members():
    logger.info(f"GET /members called")
    return member_db.get_members()


@router.get("/members/{member_id}")
def get_member_by_id(member_id: int):
    logger.info(f"GET /members/{member_id} called")
    member = member_db.get_member(member_id)
    if not member:
        logger.warning(f"Member with ID {member_id} not found.")
        raise HTTPException(status_code=404, detail="Error: Member not found.")

    return member


@router.patch("/members/{member_id}")
def update_member(member_id: int, data: UpdateMember):
    logger.info(f"PATCH /members/{member_id} called")
    updated_data = data.model_dump(exclude_unset=True)
    if not updated_data:
        logger.warning("No fields to update.")
        raise HTTPException(status_code=400, detail="Error: No fields to update.")

    if member_db.get_member(member_id) is None:
        logger.warning(f"Member with ID {member_id} not found.")
        raise HTTPException(status_code=404, detail="Error: Member not found.")

    updated = member_db.update(member_id, updated_data)
    if not updated:
        logger.warning("No fields to update.")
        raise HTTPException(status_code=400, detail="Error: No fields to update.")

    logger.info(f"Member with ID {member_id} was updated successfully.")
    return {"Message": "Member updated successfully."}


@router.patch("/members/{member_id}/deactivate")
def deactivate_member(member_id: int):
    logger.info(f"PATCH /members/{member_id}/deactivate called")
    result = member_db.deactivate(member_id)
    if not result:
        logger.warning(f"Member with ID {member_id} not found.")
        raise HTTPException(status_code=404, detail="Member not found.")
    logger.info(f"Member {member_id} deactivated successfully.")
    return {"message": "Member deactivated successfully."}


@router.patch("/members/{member_id}/activate")
def activate_member(member_id: int):
    logger.info(f"PATCH /members/{member_id}/activate called")
    result = member_db.activate(member_id)
    if not result:
        logger.warning(f"Member with ID {member_id} not found.")
        raise HTTPException(status_code=404, detail="Member not found.")
    logger.info(f"Member {member_id} activated successfully.")
    return {"message": "Member activated successfully."}
