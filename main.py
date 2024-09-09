from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas, crud

app = FastAPI()


@app.post("/contacts/", response_model=schemas.ContactResponse)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db=db, contact=contact)


@app.get("/contacts/", response_model=List[schemas.ContactResponse])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_contacts(db, skip=skip, limit=limit)


@app.get("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact_by_id(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@app.put("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def update_contact(
    contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)
):
    db_contact = crud.get_contact_by_id(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return crud.update_contact(db, contact_id, contact)


@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact_by_id(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    crud.delete_contact(db, contact_id)
    return {"message": "Contact deleted successfully"}
