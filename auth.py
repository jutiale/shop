from config import SECRET_KEY, ALGORITHM, EXPIRATION_TIME
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
import schemas
from sqlalchemy.orm import Session
from models import User
from typing_extensions import Annotated
from database import SessionLocal
from models import scopes_maker
from jose import JWTError, jwt
from pydantic import ValidationError



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        # "GoodsRead": "Read information about the goods.", 
            "GoodsUpdate": "Update information about the goods.",
            "GoodsDelete": "Delete information about the goods.",
            "GoodsCreate": "Create information about the goods.",
            # "BrandsRead": "Read information about the brands.", 
            "BrandsUpdate": "Update information about the brands.",
            "BrandsDelete": "Delete information about the brands.",
            "BrandsCreate": "Create information about the brands.",
            # "CategoriesRead": "Read information about the categories.", 
            "CategoriesUpdate": "Update information about the categories.",
            "CategpriesDelete": "Delete information about the categpries.",
            "CategoriesCreate": "Create information about the categories.",
            "UsersRead": "Read information about the users.", 
            "UsersUpdate": "Update information about the users.",
            "UsersDelete": "Delete information about the users.",
            "UsersCreate": "Create information about the users."})

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




def get_user_by_email(email, db):
    user = db.query(User).filter(User.email == email).first()
    return user


def authenticate_user(user, db: Session):
    db_user =  get_user_by_email(user.email, db)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password") 

    is_password_correct = pwd_context.verify(user.password, db_user.hashed_password)

    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    jwt_token = create_jwt_token({"sub": user.email, "scopes": scopes_maker(db_user)})
    print(jwt_token)
    return schemas.Token(access_token=jwt_token, token_type="bearer")


def create_jwt_token(data: dict):
    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({"exp": expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_jwt_token(token: str):
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.PyJWTError:
        return None
    
def get_current_user(db: Annotated[Session, Depends(get_db)], 
                     token: Annotated[str, Depends(oauth2_scheme)], security_scopes: SecurityScopes):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = schemas.TokenData(scopes=token_scopes, email=email)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user_by_email(email, db)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return schemas.User(email=user.email, id=user.id, name=user.name, role=user.role, hashed_password=user.hashed_password)
    # decoded_data = verify_jwt_token(token)
    # if not decoded_data:
    #     raise HTTPException(status_code=400, detail="Invalid token")
    # user = get_user_by_email(decoded_data["sub"], db)  # Получите пользователя из базы данных
    # if not user:
    #     raise HTTPException(status_code=400, detail="User not found")
    # return schemas.User(email=user.email, id=user.id, name=user.name, password=user.hashed_password)

