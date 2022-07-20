from odoo import models, api
from babel.dates import format_date
import num2words


class AccountMove(models.Model):

    _inherit = "account.move"

    def _get_locale_invoice_date(self, locale_code):
        return format_date(self.invoice_date, "d MMMM Y", locale_code)

    def _formatted(self, number):
        return "{:.2f}".format(number)

    def _get_total_in_words(self, locale_code, with_numbers):
        if with_numbers:
            return "%s (%s)" % (
                self._formatted(self.amount_total),
                num2words.num2words(
                    self.amount_total,
                    False,
                    locale_code,
                    "currency",
                    currency=self.currency_id.name,
                ),
            )
        else:
            return "%s" % num2words.num2words(
                self.amount_total,
                False,
                locale_code,
                "currency",
                currency=self.currency_id.name,
            )

