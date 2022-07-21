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
                    currency=self.currency_id.with_context(lang='en_US').name,
                ),
            )
        else:
            return "%s" % num2words.num2words(
                self.amount_total,
                False,
                locale_code,
                "currency",
                currency=self.currency_id.with_context(lang='en_US').name,
            )


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    def _get_computed_name_with_context(self):
        self.ensure_one()

        if not self.product_id:
            return ''

        product = self.product_id

        values = []
        if product.partner_ref:
            values.append(product.name)
        if self.journal_id.type == 'sale':
            if product.description_sale:
                values.append(product.description_sale)
        elif self.journal_id.type == 'purchase':
            if product.description_purchase:
                values.append(product.description_purchase)
        return '\n'.join(values)
