from fastapi import Depends
from app.apps.mpesa_integration.repository import MpesaTransactionRepository
from app.apps.mpesa_integration.service import MpesaTransactionService

def get_mpesa_repository() -> MpesaTransactionRepository:
    return MpesaTransactionRepository()

def get_mpesa_service(
    repo: MpesaTransactionRepository = Depends(get_mpesa_repository)
) -> MpesaTransactionService:
    return MpesaTransactionService(repository=repo)
