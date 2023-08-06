import requests

from drf_payments.constants import PaymentStatus

from ..core import BasicProvider

RESPONSE_STATUS = {
    "1": PaymentStatus.CONFIRMED,
    "2": PaymentStatus.REJECTED,
}


class AuthorizeNetProvider(BasicProvider):
    """Payment provider for Authorize.Net.

    This backend implements payments using the Advanced Integration Method (AIM) from
    `Authorize.Net <https://www.authorize.net/>`_.
    Due to test environment not create actual transaction currently can't implement refund method
    """

    def __init__(self, login_id, transaction_key, endpoint="https://test.authorize.net/gateway/transact.dll", **kwargs):
        self.login_id = login_id
        self.transaction_key = transaction_key
        self.endpoint = endpoint

    def process_payment(self, payment):
        """Due to official SDK don't support python 3.10 onwards  manual implementation required"""
        data = {
            "x_amount": payment.total,
            "x_refId": payment.id,
            "x_currency_code": payment.currency,
            "x_description": payment.description,
            "x_first_name": payment.billing_first_name,
            "x_last_name": payment.billing_last_name,
            "x_address": f"{payment.billing_address_1}, {payment.billing_address_2}",
            "x_city": payment.billing_city,
            "x_zip": payment.billing_postcode,
            "x_country": payment.billing_country_area,
            "x_customer_ip": payment.customer_ip_address,
            "x_login": self.login_id,
            "x_tran_key": self.transaction_key,
            "x_delim_data": True,
            "x_delim_char": "|",
            "x_method": "CC",
            "x_type": "AUTH_CAPTURE",
        }
        # *  Append card data to payload
        data.update(payment.extra_data["card"])
        resp = requests.post(self.endpoint, data=data)
        data = resp.text.split("|")
        message = data[3]
        status = "error"
        if resp.ok and RESPONSE_STATUS.get(data[0], False):
            status = RESPONSE_STATUS.get(data[0], status)
            payment.transaction_id = data[6]
            payment.status = status.name
            payment.save(update_fields=["transaction_id", "status"])
        else:
            payment.status = PaymentStatus.ERROR.name
            payment.extra_data["errors"] = [message]
            payment.save(update_fields=["status", "extra_data"])
