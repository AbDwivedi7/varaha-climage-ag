async def get_scope_list(
    user: dict,
    can_write: bool
):
    if user["role"] == "admin":
        scopes = [
            "admin:read",
            "admin:write",
            "guest:read"
        ]
    elif user["role"] == "user" and can_write:
        scopes = [
            "user:read",
            "guest:read",
            "user:write",
        ]
    else:
        scopes = [
            "user:read",
            "guest:read"
        ]
    return scopes