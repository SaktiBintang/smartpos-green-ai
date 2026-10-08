from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.transaction import TransactionCreate
from app.services.transaction_service import TransactionService


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.post("")
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
):
    # Sementara merchant_id diambil dari header.
    # Authentication/JWT akan menggantikan mekanisme ini
    # pada tahap Auth nanti.
    merchant_id_header = None

    if merchant_id_header is None:
        raise HTTPException(
            status_code=401,
            detail="Merchant authentication belum tersedia.",
        )

    try:
        transaction = TransactionService.create_transaction(
            db=db,
            merchant_id=UUID(merchant_id_header),
            transaction_number=payload.transaction_number,
            payment_method=payload.payment_method,
            customer_id=payload.customer_id,
            discount_amount=payload.discount_amount,
            tax_amount=payload.tax_amount,
            items=[
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "discount_amount": item.discount_amount,
                }
                for item in payload.items
            ],
        )

        return {
            "id": str(transaction.id),
            "transaction_number": transaction.transaction_number,
            "subtotal": transaction.subtotal,
            "discount_amount": transaction.discount_amount,
            "tax_amount": transaction.tax_amount,
            "total_amount": transaction.total_amount,
            "payment_method": transaction.payment_method,
            "payment_status": transaction.payment_status,
            "status": transaction.status,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
