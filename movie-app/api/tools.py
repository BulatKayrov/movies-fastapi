from fastapi import status

RESPONSES = {
    status.HTTP_204_NO_CONTENT: {
        "description": "No content",
        "content": {
            "application/json": {
                "example": "Success action",
            },
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Not found",
        "content": {
            "application/json": {
                "example": "Not found",
            },
        },
    },
}
