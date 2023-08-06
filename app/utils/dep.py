from fastapi import Depends
# from fastapi import Header
from fastapi.security import OAuth2PasswordBearer

from app.core.configs import token_manager


oauth_scheme = OAuth2PasswordBearer(
    tokenUrl="http://localhost:8000/auth/token/refresh"
)


# make token_manager dependable
async def get_token_content(token=Depends(oauth_scheme)):
    return token_manager.get_content(token)


# async def identify_api_request(authorization: str = Header()):
#     if authorization:
#         if authorization.startswith('Bearer '):
#             token = authorization.split(' ')[1]
#             return api_token_manager.get_content(token)
