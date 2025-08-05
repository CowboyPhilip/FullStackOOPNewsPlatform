from fastapi import APIRouter
from typing import Protocol

class Route(Protocol):
    router: APIRouter
