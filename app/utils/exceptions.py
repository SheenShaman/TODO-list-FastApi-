from fastapi import HTTPException, status


class UsersException(HTTPException):
    status_code = 400
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(UsersException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class UserNotFoundException(UsersException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"


class UserUnauthorizedException(UsersException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User Unauthorized"


class UserNotAdminException(UsersException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "You are not admin"


class IncorrectEmailOrPasswordException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Incorrect email or password"


class TokenExpiredException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token is expired"


class TokenAbsentException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token is absent"

class IncorrectTokenFormatException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token is incorrect"


class TasksException(HTTPException):
    status_code = 400
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class TasksNotFoundException(TasksException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Task not found"
