import requests
from typing import Any, Union, Dict
from .exceptions import ApiError

DOWELL_GEOMETRICAL_LAYOUT_URL = "http://100071.pythonanywhere.com/api/"


class GeometricalLayoutApi(object):
    """A client for the Dowell Geometrical Layout of Big Data API.
    'https://github.com/DoWellUXLab/DoWell-Geometrical-layout-of-Big-Data
    The API provides a set of endpoints to help users calculate the optimal
    arrangement of non-overlaping circles within a given canvas. By specifying
    the radius, length, and width, users can determine the number of circles
    that can be arranged in a triangular packaging, minimizing wastage of space.
    The coordinates of the circle can also be determine.

    {
        "radius":0.5,
        "length":10,
        "width":10
    }

    geometrical_layout = GeometricalLayoutApi()
    geometrical_layout = geometrical_layout.post_object(radius, length, width)
    print(geometrical_layout)

    You can obtain an access token via Dowell website
    OAuth access token is not require for now
    """

    def __init__(self, access_token: Any = None):
        self.requests = requests
        self.access_token = access_token

    def post_object(self, radius: Union[int, float], length: int, width: int) -> Dict:
        """
        Parameters, 'radius, length, width' to the Api. You get back number of cycles and coordinate

        radius : int or float
        length : int
        width : int

        Returns : Dictionary
            Dictionary containing number of circles and coordinates
        """
        
        payload = {
            "radius": radius,
            "length": length,
            "width": width
        }
        try:
            response = self.requests.post(
                DOWELL_GEOMETRICAL_LAYOUT_URL, json=payload)
            return response.json()
        except Exception as e:
            raise ApiError(e)

    def __str__(self) -> str:
        return "Geometrical Layout"
