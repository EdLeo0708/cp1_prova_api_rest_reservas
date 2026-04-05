from fastapi import APIRouter, HTTPException, status, Request
from app.schemas.schemas import LoginRequest, TokenResponse
from app.security import authenticate_user, create_access_token
from app.errors import error_response

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Autenticar usuário",
    description="Realiza login e retorna um token JWT para autenticação nas rotas protegidas.",
)
def login(request: Request, body: LoginRequest):
    user = authenticate_user(body.username, body.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )
    token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return TokenResponse(access_token=token)
