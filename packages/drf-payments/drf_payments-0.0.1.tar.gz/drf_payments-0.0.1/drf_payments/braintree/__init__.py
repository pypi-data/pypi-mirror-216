import braintree

from drf_payments.constants import PaymentError, PaymentStatus
from drf_payments.core import BasicProvider


class BraintreeProvider(BasicProvider):
    def __init__(self, merchant_id, public_key, private_key, sandbox, **kwargs):
        super().__init__(**kwargs)

        if sandbox:
            self.service = braintree.BraintreeGateway(
                braintree.Configuration(
                    braintree.Environment.Sandbox,
                    merchant_id=merchant_id,
                    public_key=public_key,
                    private_key=private_key,
                ),
            )
        else:
            self.service = braintree.BraintreeGateway(
                braintree.Configuration(
                    braintree.Environment.Production,
                    merchant_id=merchant_id,
                    public_key=public_key,
                    private_key=private_key,
                ),
            )

    def process_payment(self, payment):
        payment_method = payment.transaction_id
        try:
            result = self.service.transaction.sale(
                {
                    "amount": str(float(payment.total)),
                    "payment_method_nonce": payment_method,
                    "options": {"submit_for_settlement": True},
                },
            )
        except Exception as e:
            raise PaymentError("Can't process payment") from e

        data = self._serialize(result.transaction.__dict__)
        payment.transaction_id = result.transaction.id
        payment.extra_data["transaction"] = data
        payment.save(update_fields=["extra_data", "transaction_id"])

    def refund(self, payment, amount=None):
        if payment.status == PaymentStatus.CONFIRMED.name:
            try:
                result = self.service.transaction.refund(payment.transaction_id)
                if isinstance(result, braintree.ErrorResult):
                    raise PaymentError(f"Can't process refund: {result.message}")
                payment.status = PaymentStatus.REFUNDED.name
                payment.save(update_fields=["status"])
                return
            except Exception as e:
                raise PaymentError("Can't process refund") from e
        raise PaymentError("Only Confirmed payments can be refunded")

    @staticmethod
    def _serialize(data) -> dict:
        """Helper method to serialize transaction data"""
        skip_fields = [
            "_setattrs",
            "disbursement_details",
            "descriptor",
            "status_history",
            "gateway",
            "billing_details",
            "credit_card_details",
            "shipping_details",
            "subscription_details",
            "customer_details",
        ]
        result = {key: item for key, item in data.items() if key not in skip_fields}
        result["amount"] = str(result["amount"])
        result["created_at"] = str(result["created_at"])
        result["updated_at"] = str(result["updated_at"])
        result["authorization_expires_at"] = str(result["authorization_expires_at"])
        return result

    def get_client_token(self):
        try:
            token = self.service.client_token.generate()
        except Exception:
            return None
        return token
