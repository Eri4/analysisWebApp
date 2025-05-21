from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from server.app.db.database import get_db