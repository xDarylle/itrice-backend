"""
The purpose of this to standardize the response format.
The response should consists of the status code, a message, and the data (if necessary)
"""

def Response(status: int, message=None, data=None):
    if message and data:
        return {
            "message": message,
            "data": data
        }, status
        
    if not message:
        return {
            "data": data
        }, status
    
    if not data:
        return {
            "message": message,
        }, status