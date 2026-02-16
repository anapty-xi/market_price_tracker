from typing import Protocol

class UserProtocol(Protocol):
    def delete_product(self, tg_id: str, product_url: str) -> bool:
        pass
    def add_product(self, tg_id: str, product_url: str) -> bool:
        pass
    def get_tracking_list(self, tg_id: str) -> list[str]:
        pass

    def is_user_exist(self, tg_id: str) -> bool:
        pass
    def create_if_not_exists(self, tg_id: str) -> None:
        pass