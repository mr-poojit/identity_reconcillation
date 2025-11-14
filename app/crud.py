from typing import List, Set, Dict
from sqlmodel import Session, select
from datetime import datetime
from .models import Contact


def build_components(session: Session) -> Dict[int, Set[int]]:
    contacts = session.exec(select(Contact)).all()

    email_map = {}
    phone_map = {}

    for c in contacts:
        if c.email:
            email_map.setdefault(c.email, []).append(c.id)
        if c.phoneNumber:
            phone_map.setdefault(c.phoneNumber, []).append(c.id)

    adj = {c.id: set() for c in contacts}

    # connect by email
    for ids in email_map.values():
        for i in ids:
            for j in ids:
                if i != j:
                    adj[i].add(j)

    # connect by phone
    for ids in phone_map.values():
        for i in ids:
            for j in ids:
                if i != j:
                    adj[i].add(j)

    return adj


def component_for_ids(adj: Dict[int, Set[int]], start_ids: Set[int]) -> Set[int]:
    seen = set()
    stack = list(start_ids)

    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)

        for nb in adj.get(cur, []):
            if nb not in seen:
                stack.append(nb)

    return seen


def fetch_contact_group(session: Session, matched_ids: Set[int]) -> List[Contact]:
    if not matched_ids:
        return []

    adj = build_components(session)
    component_ids = component_for_ids(adj, matched_ids)

    contacts = session.exec(
        select(Contact).where(Contact.id.in_(component_ids))
    ).all()

    return contacts


def create_contact(
    session: Session,
    email: str | None,
    phone: str | None,
    linkPrecedence: str = "primary",
    linkedId: int | None = None
) -> Contact:

    now = datetime.utcnow()

    c = Contact(
        email=email,
        phoneNumber=phone,
        linkedId=linkedId,
        linkPrecedence=linkPrecedence,
        createdAt=now,
        updatedAt=now
    )

    session.add(c)
    session.commit()
    session.refresh(c)

    return c


def ensure_primary_and_update(session: Session, contacts: List[Contact]) -> Contact:
    contacts_sorted = sorted(contacts, key=lambda c: c.createdAt)

    primary = contacts_sorted[0]
    changed = False

    # Make all others secondary
    for c in contacts_sorted[1:]:
        if c.linkPrecedence != "secondary" or c.linkedId != primary.id:
            c.linkPrecedence = "secondary"
            c.linkedId = primary.id
            c.updatedAt = datetime.utcnow()
            session.add(c)
            changed = True

    # Fix primary if previously marked secondary
    if primary.linkPrecedence != "primary":
        primary.linkPrecedence = "primary"
        primary.linkedId = None
        primary.updatedAt = datetime.utcnow()
        session.add(primary)
        changed = True

    if changed:
        session.commit()
        for c in contacts:
            session.refresh(c)

    return primary
