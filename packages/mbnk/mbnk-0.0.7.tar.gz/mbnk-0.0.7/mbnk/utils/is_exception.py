from requests import Response


def is_exception(response: Response) -> bool:
    if response.status_code != 200:
        return True

    return False
