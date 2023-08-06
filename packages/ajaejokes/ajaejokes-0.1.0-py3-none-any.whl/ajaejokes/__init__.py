import requests 
import logging

API_URL = "https://icanhazdadjoke.com/" 

logger = logging.getLogger("dadjoke")


class JokeNotAvailableException(Exception): pass 


def joke() -> str:
    f"""Come up with a dad joke from {API_URL}
    """
    headers = {
      'Accept': 'application/json',
    }

    res = requests.get(API_URL, headers=headers)

    if res.status_code != 200:
        logger.error(f"Failed to fetch requests with status code {res.status_code}")
        raise JokeNotAvailableException()
    
    data = res.json()
    joke = data.get("joke", "")

    return joke


__all__ = ["joke", "JokeNotAvailableException"]
