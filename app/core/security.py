from fastapi import Depends, HTTPException, status

FAKE_USERS_DB = {
    "harry": {"role": "AUROR"},
    "dumbledore": {"role": "AUROR"},
    "severus": {"role": "AUROR"},
    "ron": {"role": "APPRENTICE"},
    "hermione": {"role": "APPRENTICE"},
    "dobie": {"role": "APPRENTICE"}
}

def get_current_user(user_id: str = "harry"):
    if user_id not in FAKE_USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales mágicas inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id

def check_role_auror(user_id: str = Depends(get_current_user)):
    user_data = FAKE_USERS_DB.get(user_id)
    if user_data is None or user_data["role"] != "AUROR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permiso denegado. Se requiere el rol AUROR para acceder a hechizos sensibles. (Usuario: {user_id})",
        )
    return user_id

