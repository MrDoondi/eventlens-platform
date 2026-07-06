from typing import Any


def success_response(data: Any):
    return {
        "success": True,
        "data": data,
    }