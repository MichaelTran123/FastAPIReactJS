import services as _services, schemas as _schemas

import fastapi as _fastapi
import fastapi.security as _security

import sqlalchemy.orm as _orm

app = _fastapi.FastAPI()

@app.post("/api/users")
async def create_user(
    user: _schemas.UserCreate,
    db: _orm.session = _fastapi.Depends(_services.get_db)):
    db_user =await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail=f"Email already in user")
    return await _services.create_user(user, db)

@app.post("api/token")
async def genarate_token(
            form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
            db: _orm.Session = _fastapi.Depends(_services.get_db)):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credenticals")
    return await _services.create_token(user)