"""
The purpose of this to standardize the response format.
The response should consists of the status code, a message, and the data (if necessary)
"""


def Response(status: int, message=None, data=None, maxPage=None):
    if message and data and maxPage:
        return {
            "message": message,
            "data": data,
            "maxPage": maxPage
        }, status

    if message and data:
        return {
            "message": message,
            "data": data
        }, status

    if not message:
        if maxPage:
            return {
                "data": data,
                "maxPage": maxPage
            }

        return {
            "data": data
        }, status

    if not data:
        return {
            "message": message,
        }, status
