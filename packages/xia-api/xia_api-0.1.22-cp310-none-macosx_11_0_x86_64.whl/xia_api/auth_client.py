import requests


class AuthClient:
    # api_root = "https://xia-app-auth-wwkkhmzugq-ew.a.run.app/api/"

    def __init__(self, api_root: str = "https://auth.x-i-a.com/api/", app_name: str = "xia-auth"):
        self.app_name = app_name
        self.api_root = api_root
        self.user_root = api_root + ("user" if api_root.endswith("/") else "/user")
        self.role_root = api_root + ("role" if api_root.endswith("/") else "/role")
        self.matrix_root = api_root + ("matrix" if api_root.endswith("/") else "/matrix")

    def get_api_acl(self, api_key: str, api_id: str = ""):
        """Get Access Control List of API

        Args:
            api_key: API Key
            api_id: API ID

        Returns:
            API Detail or Error Message
        """
        r = requests.post(self.role_root + f"/_/get_api_acl", json={"api_key": api_key, "app_name": self.app_name})
        try:
            result = r.json()
        except Exception as e:
            return {"message": e.args[0], "trace": r.content.decode()}, r.status_code
        if r.status_code == 200 and api_id and result["id"] != api_id:
            # An extra check for the API ID if API ID is provided
            return {"message": f"API ID {api_id} and {result['id']} don't match"}, 401
        if r.status_code >= 300 and "message" not in result:
            # It is not a standard XIA error
            return {"message": f"API Endpoint returns code {r.status_code}", "trace": r.content.decode()}, r.status_code
        # Everything seems to be good
        return r.json(), r.status_code

