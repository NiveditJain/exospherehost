from pymongo.errors import DuplicateKeyError
from starlette.responses import JSONResponse

from ..models.create_user_request import CreateUserRequest
from ..models.create_user_response import CreateUserResponse
from ..models.user_database_model import User

from app.singletons.logs_manager import LogsManager

logger = LogsManager().get_logger()


async def create_user(request: CreateUserRequest, x_exosphere_request_id: str) -> CreateUserResponse:
    try: 
        logger.info("Creating user", x_exosphere_request_id=x_exosphere_request_id)

        new_user = User.create_new_user(
            name=request.name,
            type=request.type,
            identifier=request.identifier,
            credential=request.credential
        )
        await new_user.insert()
        logger.info("User created", x_exosphere_request_id=x_exosphere_request_id)

        return CreateUserResponse(
            id=str(new_user.id),
            name=new_user.name,
            type=new_user.type,
            identifier=new_user.identifier,
            verification_status=new_user.verification_status,
            status=new_user.status,
            created_at=new_user.created_at,
            updated_at=new_user.updated_at
        )
    
    except DuplicateKeyError as e:
        logger.error("Error creating user", error=e, x_exosphere_request_id=x_exosphere_request_id)
        return JSONResponse(status_code=400, content={"success": False, "detail": "User already exists"})
    
    except Exception as e:
        logger.error("Error creating user", error=e, x_exosphere_request_id=x_exosphere_request_id)
        raise e