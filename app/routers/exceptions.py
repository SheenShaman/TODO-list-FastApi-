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


class UserUnauthorized(UsersException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User Unauthorized"


class TasksException(HTTPException):
    status_code = 400
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class TasksNotFoundException(TasksException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Task not found"
