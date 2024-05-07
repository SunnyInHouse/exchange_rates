from fastapi import HTTPException, status


class CustomHTTPException(HTTPException):
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.message)


class AccessTokenUncorrect(CustomHTTPException):
    message = "Token uncorrect"
    status_code = status.HTTP_403_FORBIDDEN


class AccessTokenExpired(CustomHTTPException):
    message = "Token expired"
    status_code = status.HTTP_403_FORBIDDEN


class AuthenticationFailed(CustomHTTPException):
    message = "Authentication data not correct - user not found"
    status_code = status.HTTP_401_UNAUTHORIZED


class JWTValidateExceptions(CustomHTTPException):
    message = "Could not validate credentials"
    status_code = status.HTTP_401_UNAUTHORIZED
    headers = {"WWW-Authenticate": "Bearer"}


class UserNotFound(CustomHTTPException):
    message = "User not found"
    status_code = status.HTTP_404_NOT_FOUND


class IncorrectUser(UserNotFound):
    message = "Incorrect email or password"


class InActiveUser(CustomHTTPException):
    message = "Inactive user"
    status_code = status.HTTP_403_FORBIDDEN


class UserAlreadyExists(CustomHTTPException):
    message = "User already exists"
    status_code = status.HTTP_409_CONFLICT
