from typing import Union, Optional
from mbnk.decorators import (
    async_get_request,
    async_post_request,
    async_delete_request
)
from mbnk.enums import MonoPayApiUrls


class Monobank:
    pass


class Merchant:

    __base_url__ = None
    __headers__ = {}

    def __init__(
            self,
            base_url: str,
            headers: dict
    ):
        self.__base_url__ = base_url
        self.__headers__ = headers

    @async_get_request(url=MonoPayApiUrls.merchant_details)
    def details(self, **kwargs):
        return kwargs["response_data"]

    @async_get_request(url=MonoPayApiUrls.merchant_statement)
    def statement(self, **kwargs):
        return kwargs["response_data"]

    @async_get_request(url=MonoPayApiUrls.merchant_pubkey)
    def pubkey(self, **kwargs):
        return kwargs["response_data"]


class Invoice:

    __base_url__ = None
    __headers__ = {}

    def __init__(
            self,
            base_url: str,
            headers: dict
    ):
        self.__base_url__ = base_url
        self.__headers__ = headers

    @async_post_request(url=MonoPayApiUrls.invoice_create)
    def create(
            self,
            amount: int,
            ccy: Optional[int] = None,
            merchant_paym_info: Optional = None,
            redirect_url: Optional[str] = None,
            web_hook_url: Optional[str] = None,
            validity: Optional[int] = None,
            payment_type: Optional[str] = None,
            qr_id: Optional = None,
            save_card_data: Optional = None,
            **kwargs
    ):
        """
        :param amount:
        :param ccy:
        :param merchant_paym_info:
        :param redirect_url:
        :param web_hook_url:
        :param validity:
        :param payment_type:
        :param qr_id:
        :param save_card_data:
        :return:
        """

        return kwargs["response_data"]

    @async_post_request(url=MonoPayApiUrls.invoice_split)
    def split(
            self,
            invoice_id: str,
            **kwargs
    ):
        return kwargs["response_data"]

    @async_post_request(url=MonoPayApiUrls.invoice_cancel)
    def cancel(
            self,
            invoice_id: str,
            ext_ref: str = None,
            amount: int = None,
            items=None,
            **kwargs
    ):
        return kwargs["response_data"]

    async def status(
            self,
            invoice_id: str,
            **kwargs
    ):
        return kwargs["response_data"]

    @async_post_request(url=MonoPayApiUrls.invoice_invalidation)
    async def invalidation(
            self,
            invoice_id: str,
            **kwargs
    ):
        return kwargs['response_data']

    async def info(
            self,
            invoice_id: str,
            **kwargs
    ):
        return kwargs['response_data']

    async def finalize(
            self,
            invoice_id: str,
            amount: int,
            **kwargs
    ):
        return kwargs['response_data']


class Qr:

    __base_url__ = None
    __headers__ = {}

    def __init__(
            self,
            base_url: str,
            headers: dict
    ):
        self.__base_url__ = base_url
        self.__headers__ = headers

    @async_get_request(url=MonoPayApiUrls.qr_list)
    def list(self, **kwargs):
        return kwargs["response_data"]

    @async_post_request(url=MonoPayApiUrls.qr_details)
    def details(
            self,
            qr_id: str,
            **kwargs
    ):
        """

        :param qr_id:
        :return:
        """
        return kwargs["response_data"]

    @async_post_request(url=MonoPayApiUrls.qr_reset_amount)
    def reset_amount(
            self,
            qr_id: str,
            **kwargs
    ):
        """

        :param qr_id:
        :return:
        """
        return kwargs["response_data"]


class Wallet:

    __base_url__ = None
    __headers__ = {}

    def __init__(
            self,
            base_url: str,
            headers: dict
    ):
        self.__base_url__ = base_url
        self.__headers__ = headers

    @async_get_request(url=MonoPayApiUrls.wallet_cards)
    async def cards(
            self,
            wallet_id: str,
            **kwargs
    ):
        return kwargs["response_data"]

    async def payment(self):
        pass

    @async_delete_request(url=MonoPayApiUrls.wallet_delete_card)
    async def delete_card(
            self,
            card_token: str,
            **kwargs
    ):
        return kwargs["response_data"]


class AsyncMonoPay:

    __base_url__ = "https://api.monobank.ua"
    __api_token__ = None
    __headers__ = {}

    def __init__(self, api_token: str):
        self.__api_token__ = api_token
        self.__headers__["X-Token"] = self.__api_token__

        self.merchant: Merchant = Merchant(
            base_url=self.__base_url__,
            headers=self.__headers__
        )

        self.invoice: Invoice = Invoice(
            base_url=self.__base_url__,
            headers=self.__headers__
        )

        self.qr: Qr = Qr(
            base_url=self.__base_url__,
            headers=self.__headers__
        )

        self.wallet: Wallet = Wallet(
            base_url=self.__base_url__,
            headers=self.__headers__
        )

    def get_api_token(self):
        return self.__api_token__
