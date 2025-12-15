def set_cookie(response, name, value, expires=24 * 60 * 60):
    response.set_cookie(
        name,
        value=value,
        path="/",
        domain=None,
        secure=True,
        httponly=True,
        expires=expires
    )

    return response
