from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urljoin

from request.services import PydanticApiService
from schemas.responses import UserResponse
from utils import make_random_password


@dataclass
class UserService(PydanticApiService):
    url_path = "profiles/"

    def get_user(self, **kwargs) -> UserResponse | None:
        r = self.get_users(**kwargs)
        return r[0] if r and len(r) > 0 else None

    def get_users(self, **kwargs) -> UserResponse | list[UserResponse]:
        return self.get(UserResponse, self.url_path, params=kwargs)

    def create_user(self, **kwargs) -> UserResponse:
        if "username" not in kwargs and "telegram_login" in kwargs:
            kwargs["username"] = kwargs["telegram_login"]
        if "password" not in kwargs:
            kwargs["password"] = make_random_password(8)
        if "date_joined" not in kwargs:
            kwargs["date_joined"] = str(datetime.now())
        return self.post(UserResponse, self.url_path, data=kwargs)

    def update_user(self, user_id: int, **kwargs) -> UserResponse:
        return self.patch(UserResponse, urljoin(self.url_path, f"{user_id}/"), data=kwargs)
