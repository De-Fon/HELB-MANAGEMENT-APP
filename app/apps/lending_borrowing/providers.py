from fastapi import Depends
from app.apps.lending_borrowing.repository import LendingBorrowingRepository
from app.apps.lending_borrowing.service import LendingBorrowingService

def get_lending_borrowing_repository() -> LendingBorrowingRepository:
    return LendingBorrowingRepository()

def get_lending_borrowing_service(
    repo: LendingBorrowingRepository = Depends(get_lending_borrowing_repository)
) -> LendingBorrowingService:
    return LendingBorrowingService(repository=repo)
