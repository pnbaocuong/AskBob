from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..dependencies import get_db_session
from ...infrastructure.db.models import User, Tenant
from ...infrastructure.security.password import hash_password, verify_password
from ...infrastructure.security.jwt import create_access_token

router = APIRouter()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    tenant_name: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=TokenResponse)
async def register(req: RegisterRequest, session: Annotated[AsyncSession, Depends(get_db_session)]):
    # Check existing user
    exists = await session.execute(select(User).where(User.email == req.email))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    tenant = Tenant(name=req.tenant_name)
    session.add(tenant)
    await session.flush()

    user = User(email=req.email, hashed_password=hash_password(req.password), tenant_id=tenant.id)
    session.add(user)
    await session.commit()

    token = create_access_token({"user_id": str(user.id), "tenant_id": str(user.tenant_id)})
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[AsyncSession, Depends(get_db_session)]):
    result = await session.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    token = create_access_token({"user_id": str(user.id), "tenant_id": str(user.tenant_id)})
    return TokenResponse(access_token=token)
