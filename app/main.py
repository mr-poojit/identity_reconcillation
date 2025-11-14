from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from .database import init_db, get_session
from .schemas import IdentifyRequest
from .models import Contact
from .crud import (
    fetch_contact_group,
    create_contact,
    ensure_primary_and_update
)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/identify")
def identify(payload: IdentifyRequest, session: Session = Depends(get_session)):

    email = payload.email
    phone = payload.phoneNumber

    if email is None and phone is None:
        raise HTTPException(
            status_code=400,
            detail="email or phoneNumber required"
        )

    # convert phone to string
    if phone is not None:
        phone = str(phone)

    # Fetch direct matches
    q = select(Contact).where(
        (Contact.email == email) | (Contact.phoneNumber == phone)
    )
    matched = session.exec(q).all()
    matched_ids = {c.id for c in matched}

    # No match → create NEW PRIMARY
    if not matched:
        new_primary = create_contact(
            session,
            email=email,
            phone=phone,
            linkPrecedence="primary",
            linkedId=None
        )

        return {
            "contact": {
                "primaryContatctId": new_primary.id,
                "emails": [new_primary.email] if new_primary.email else [],
                "phoneNumbers": [new_primary.phoneNumber] if new_primary.phoneNumber else [],
                "secondaryContactIds": []
            }
        }

    # Get entire connected group
    group = fetch_contact_group(session, matched_ids)

    # Ensure correct primary (oldest)
    primary = ensure_primary_and_update(session, group)

    # --- Detect NEW information ---
    group_emails = {c.email for c in group if c.email}
    group_phones = {c.phoneNumber for c in group if c.phoneNumber}

    new_info = False
    if email and email not in group_emails:
        new_info = True
    if phone and phone not in group_phones:
        new_info = True

    # New info → create secondary contact
    if new_info:
        new_secondary = create_contact(
            session,
            email=email,
            phone=phone,
            linkPrecedence="secondary",
            linkedId=primary.id
        )
        group.append(new_secondary)

    # Build final response
    emails = []
    phones = []
    secondary_ids = []

    # Primary first
    if primary.email:
        emails.append(primary.email)
    if primary.phoneNumber:
        phones.append(primary.phoneNumber)

    # Others
    for c in group:
        if c.id == primary.id:
            continue

        if c.email and c.email not in emails:
            emails.append(c.email)

        if c.phoneNumber and c.phoneNumber not in phones:
            phones.append(c.phoneNumber)

        if c.linkPrecedence == "secondary":
            secondary_ids.append(c.id)

    return {
        "contact": {
            "primaryContatctId": primary.id,
            "emails": emails,
            "phoneNumbers": phones,
            "secondaryContactIds": secondary_ids
        }
    }
