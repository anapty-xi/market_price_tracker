from usecases.user.user_protocol import UserProtocol

class UserDbGateway(UserProtocol):
    def delete_product(self, tg_id: str, product_url: str) -> None:
        pass
    def add_product(self, tg_id: str, product_url: str) -> None:
        pass
    def get_tracking_list(self, tg_id: str) -> list[str]:
        pass