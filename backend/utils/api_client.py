import time

import requests


RETRY_STATUS_CODES = {429, 500, 502, 503, 504}


def request_json(
    method: str,
    url: str,
    *,
    service_name: str = "API",
    retry_attempts: int = 3,
    backoff_factor: float = 0.5,
    **kwargs
):
    if retry_attempts < 1:
        raise ValueError("retry_attempts must be at least 1")

    for attempt in range(retry_attempts):
        try:
            response = requests.request(method, url, **kwargs)
            print(
                f"{service_name} {method} {url} "
                f"- Status code: {response.status_code}"
            )

            if (
                response.status_code in RETRY_STATUS_CODES
                and attempt < retry_attempts - 1
            ):
                print(
                    f"Retrying {service_name} {method} {url} "
                    f"(attempt {attempt + 2}/{retry_attempts})"
                )
                time.sleep(backoff_factor * (2 ** attempt))
                continue

            response.raise_for_status()
            return response.json()

        except requests.exceptions.JSONDecodeError:
            raise
        except requests.exceptions.HTTPError as error:
            status_code = error.response.status_code if error.response else None
            if status_code not in RETRY_STATUS_CODES or attempt == retry_attempts - 1:
                raise
            print(
                f"Retrying {service_name} {method} {url} "
                f"(attempt {attempt + 2}/{retry_attempts})"
            )
        except requests.exceptions.RequestException:
            if attempt == retry_attempts - 1:
                raise
            print(
                f"Retrying {service_name} {method} {url} "
                f"(attempt {attempt + 2}/{retry_attempts})"
            )

        time.sleep(backoff_factor * (2 ** attempt))