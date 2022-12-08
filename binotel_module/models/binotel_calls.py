# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import json
import hashlib
import time
import pytz
from datetime import date, datetime

import requests

import odoo.osv.expression
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class BinotelMethods(models.AbstractModel):

    _name = "binotel.methods"

    @api.model
    def _stats_incoming_calls_for_period(
        self, period_start: datetime, period_end: datetime, params: dict
    ) -> dict:

        method_name = "stats/incoming-calls-for-period"
        method_params = {
            "startTime": str(int(period_start.timestamp())),
            "stopTime": str(int(period_end.timestamp())),
        }

        answer = self._exec_method(method_name, method_params, params)

        if (
            answer["status"] == "error"
            and answer["message"].find(
                "Requests are too frequent. You can do this request after"
            )
            > -1
        ):

            timeout = int(answer["message"][57 : answer["message"].find(" sec.")])
            time.sleep(timeout)

            answer = self._stats_incoming_calls_for_period(
                period_start, period_end, params
            )

        return answer

    @api.model
    def _stats_outgoing_calls_for_period(
        self, period_start: datetime, period_end: datetime, params: dict
    ) -> dict:
        method_name = "stats/outgoing-calls-for-period"
        method_params = {
            "startTime": str(int(period_start.timestamp())),
            "stopTime": str(int(period_end.timestamp())),
        }

        answer = self._exec_method(method_name, method_params, params)

        if (
            answer["status"] == "error"
            and answer["message"].find(
                "Requests are too frequent. You can do this request after"
            )
            > -1
        ):
            timeout = int(answer["message"][57 : answer["message"].find(" sec.")])
            time.sleep(timeout)

            answer = self._stats_outgoing_calls_for_period(
                period_start, period_end, params
            )

        return answer

    @api.model
    def _settings_list_of_employees(self, params: dict) -> dict:

        method_name = "settings/list-of-employees"
        return self._exec_method(method_name, {}, params)

    @api.model
    def _exec_method(self, method_name: str, method_params: dict, params: dict) -> dict:

        _logger.info("Executing method %s" % method_name)

        answer = {"status": ""}

        api_host = (
            self.env["ir.config_parameter"].sudo().get_param("binotel.api_host", "")
        )
        api_key = (
            self.env["ir.config_parameter"].sudo().get_param("binotel.api_key", "")
        )
        secret = self.env["ir.config_parameter"].sudo().get_param("binotel.secret", "")

        if not api_host or not api_key or not secret:
            _logger.error("Binotel connection parameters are not set")
            answer["status"] = "Binotel connection parameters are not set"
            params["deny"] = True
            return answer

        method_params["signature"] = self._form_signature(method_params, secret)
        method_params["key"] = api_key

        post_data = json.dumps(method_params)
        headers = {
            "Content-Length": str(len(post_data)),
            "Content-Type": "application/json",
            "charset": "utf-8",
        }

        url = self.form_url(api_host, method_name, params)

        response = requests.post(
            url=url, data=post_data.encode("utf-8"), headers=headers
        )
        if response.status_code == 200:
            answer = json.loads(response.text)
        else:
            answer = {"status": response.text}
            params["deny"] = True

        return answer

    @api.model
    def _form_signature(self, method_params, secret):

        signature = (
            ""
            + secret
            + (
                "[]"
                if len(method_params) == 0
                else json.dumps(method_params).replace(" ", "")
            )
        )
        return hashlib.md5(signature.encode("utf-8")).hexdigest()

    @api.model
    def form_url(self, host: str, method_name: str, params: dict) -> str:

        if params["deny"]:
            return ""

        version = "3.0"
        api_format = "json"

        return "https://%s/api/%s/%s.%s" % (
            host,
            version,
            method_name,
            api_format,
        )


class BinotelCalls(models.Model):

    _name = "binotel.calls"
    _description = "Binotel Calls"
    _order = "call_id"

    call_id = fields.Char("Call ID")
    duration = fields.Integer("Duration, sec")
    phone = fields.Char("Phone number")
    binotel_user = fields.Many2one("binotel.users", "User")
    ticket = fields.Many2one("helpdesk.ticket", "Ticket")
    call_datetime = fields.Datetime("Call Date&time")

    discarded_call_types = [
        "VM",  # голосовая почта без сообщения
        "VM-SUCCESS",  # голосовая почта с сообщением
        "SMS-SENDING",  # SMS сообщение на отправке
        "SMS-SUCCESS",  # SMS сообщение успешно отправлено
        "SMS-FAILED",  # SMS сообщение не отправлено
        "SUCCESS",  # успешно принятый факс
        "FAILED",  # непринятый факс
        "BUSY",  # неуспешный звонок по причине занято
        "NOANSWER",  # неуспешный звонок по причине нет ответа
        "CANCEL",  # неуспешный звонок по причине отмены звонка
        "CONGESTION",  # неуспешный звонок
        "CHANUNAVAIL",  # неуспешный звонок
    ]

    @api.model
    def _load_calls(self, loading_date: date = None) -> None:

        if not loading_date:
            loading_date = date.today()

        date_start = datetime(
            year=loading_date.year,
            month=loading_date.month,
            day=loading_date.day,
            hour=0,
            minute=0,
            second=0,
        )
        date_end = datetime(
            year=loading_date.year,
            month=loading_date.month,
            day=loading_date.day,
            hour=23,
            minute=59,
            second=59,
        )

        binotel = self.env["binotel.methods"].sudo()

        params = {"deny": False}
        calls_data_list = []

        incomings = binotel._stats_incoming_calls_for_period(
            date_start, date_end, params
        )
        if params["deny"]:
            return
        else:
            calls_data_list.append(incomings)

        outgoings = binotel._stats_outgoing_calls_for_period(
            date_start, date_end, params
        )
        if params["deny"]:
            return
        else:
            calls_data_list.append(outgoings)

        min_call_duration = int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("binotel.min_call_duration", 0)
        )
        user_tz = self.env.user.tz or self.env.context.get('tz')
        user_pytz = pytz.timezone(user_tz) if user_tz else pytz.utc
        model_binotel_calls = self.env["binotel.calls"].sudo()
        model_partners = self.env["res.partner"].sudo()

        for calls_data in calls_data_list:
            calls = calls_data["callDetails"]
            for call_key in calls:
                params["deny"] = False
                call = calls[call_key]
                call_history = self._get_call_history(call, params)
                if params["deny"]:
                    continue

                for binotel_user_id in call_history:
                    call_duration = call_history[binotel_user_id]
                    if call_duration < min_call_duration:
                        continue

                    binotel_user_rec = (
                        self.env["binotel.users"]
                        .sudo()
                        .search([("binotel_id", "=", binotel_user_id)], limit=1)
                    )
                    if not binotel_user_rec:
                        continue

                    call_datetime = datetime.fromtimestamp(int(call["startTime"]), tz=user_pytz)
                    client_phone = call["externalNumber"]
                    call_id = call["generalCallID"]

                    binotel_call_data = {
                        "call_id": call_id,
                        "duration": call_duration,
                        "phone": client_phone,
                        "binotel_user": binotel_user_rec.id,
                        "call_datetime": call_datetime,
                    }

                    domain = [
                        "&",
                        ("call_id", "=", call_id),
                        ("binotel_user", "=", binotel_user_rec.id),
                    ]
                    call_rec = model_binotel_calls.search(domain)
                    if call_rec:
                        # updating existing record
                        if not call_rec.ensure_one():
                            _logger.warning(
                                _(
                                    "Several calls with identical ID's found; Call ID: %s"
                                )
                                % call_id
                            )
                            continue
                        else:
                            call_rec.write(
                                binotel_call_data
                            )
                    else:
                        # creating new call record
                        call_rec = model_binotel_calls.create(
                            [
                                binotel_call_data,
                            ]
                        )

                    ticket_id = call_rec.ticket
                    if not ticket_id:
                        # creating new ticket

                        partner_id = model_partners.search(
                            [("phone", "=", client_phone)], limit=1
                        )
                        if not partner_id:
                            # try to search existing call recs with the same phone
                            call_by_phone_recs = model_binotel_calls.search(
                                [
                                    "&",
                                    ("phone", "=", client_phone),
                                    ("call_id", "!=", call_id),
                                ]
                            )
                            if call_by_phone_recs:
                                for rec in call_by_phone_recs:
                                    if rec.ticket and rec.ticket.partner_id:
                                        partner_id = rec.ticket.partner_id
                                        break

                        partner_presentation = (
                            partner_id.name if partner_id else client_phone
                        )

                        ticket_name = _("[%s] - Phone call: %s") % (
                            partner_presentation,
                            client_phone,
                        )
                        ticket_desc = _(
                            "Phone call from a client. Date: %s, duration %s \n Client: %s"
                        ) % (
                            call_datetime,
                            self._form_duration_representation(call_duration),
                            partner_presentation,
                        )

                        ticket_values = {
                            "name": ticket_name,
                            "assigned_date": call_datetime,
                            "description": ticket_desc,
                            "user_id": binotel_user_rec.user_id.id,
                            "partner_id": partner_id.id,
                            "partner_name": partner_presentation,
                            "tag_ids": [
                                (
                                    4,
                                    self.env.ref(
                                        "binotel_module.binotel_ticket_tag"
                                    ).id,
                                )
                            ],
                            "channel_id": self.env.ref(
                                "binotel_module.binotel_ticket_channel"
                            ).id,
                            "category_id": self.env.ref(
                                "binotel_module.binotel_ticket_category"
                            ).id,
                            "duration": float(call_duration) / 3600.0,
                        }
                        ticket = self.env["helpdesk.ticket"].create([ticket_values])
                        call_rec.ticket = ticket.id

    @api.model
    def _get_call_history(self, call: dict, params: dict) -> dict:

        call_history_data = call["historyData"]
        call_id = call["generalCallID"]
        if not call_history_data:
            _logger.error(_("Missing history data for a call with ID : %s") % call_id)
            params["deny"] = True
            return {}

        call_history = {}
        for history_point in call_history_data:
            call_type = history_point["disposition"]
            if call_type in self.discarded_call_types:
                continue

            binotel_user_id = history_point.get("internalNumber", None)
            if not binotel_user_id:
                binotel_user_id = call["internalNumber"]
            else:
                binotel_user_id = self._get_binotel_user_id(binotel_user_id)
                if not binotel_user_id:
                    continue

            call_duration = history_point["billsec"]
            call_history[binotel_user_id] = call_history.get(binotel_user_id, 0) + int(
                call_duration
            )

        return call_history

    @api.model
    def _get_binotel_user_id(self, binotel_user_id: str) -> (str, None):
        if binotel_user_id == "Стандартное приветствие в рабочее время":
            # Отказ тут не нужен, просто пропускаем
            return None
        else:
            if binotel_user_id.find(">") > -1:
                return binotel_user_id[binotel_user_id.find(">") + 1 :].strip()
            else:
                return binotel_user_id

    @api.model
    def _form_duration_representation(self, duration: int) -> str:
        hours = duration // 3600
        mins = (duration % 3600) // 60
        secs = duration % 60

        if hours and mins:
            return _("%s hr %s min %s sec") % (hours, mins, secs)
        elif mins:
            return _("%s min %s sec") % (mins, secs)
        else:
            return _("%s sec") % secs


class BinotelUsers(models.Model):

    _name = "binotel.users"
    _description = "Binotel Users"
    _inherits = {"res.users": "user_id"}
    _rec_name = "binotel_name"

    user_id = fields.Many2one("res.users", "User")
    binotel_id = fields.Char("ID")
    binotel_name = fields.Char("Binotel Name")

    @api.model
    def create(self, vals_list):
        return super(BinotelUsers, self).create(vals_list)

    @api.model
    def _load_users(self):

        binotel = self.env["binotel.methods"].sudo()
        params = {"deny": False}
        answer = binotel._settings_list_of_employees(params)
        if params["deny"]:
            _logger.error(answer["status"])
            return

        users_dict = answer["listOfEmployees"]
        create_vals = []
        for binotel_user_id in users_dict:
            user_data = users_dict[binotel_user_id]
            endpoint_data = user_data["endpointData"]
            if len(endpoint_data) == 0:
                continue
            binotel_id = endpoint_data["internalNumber"]
            binotel_name = user_data["name"]
            email = user_data["email"]
            phone = user_data["mobileNumber"]

            existing_user_id = self.env["binotel.users"].search(
                [("binotel_id", "=", binotel_id)]
            )
            if not existing_user_id:
                domain = [("name", "ilike", binotel_name)]
                if email:
                    email_domain = [("email", "ilike", email)]
                    domain = odoo.osv.expression.OR([domain, email_domain])
                if phone:
                    email_domain = [("phone", "ilike", phone)]
                    domain = odoo.osv.expression.OR([domain, email_domain])
                domain = odoo.osv.expression.AND(
                    [domain, [("active", "in", (True, False))]]
                )
                user_id = self.env["res.users"].search(domain, limit=1)
                if user_id:
                    values = {
                        "user_id": user_id.id,
                        "binotel_id": binotel_id,
                        "binotel_name": binotel_name,
                    }
                else:
                    values = {
                        "name": binotel_name,
                        "login": email if email else binotel_name,
                        "email": email,
                        "phone": phone,
                        "binotel_id": binotel_id,
                        "binotel_name": binotel_name,
                    }
                create_vals.append(values)

        if len(create_vals) > 0:
            try:
                self.env["binotel.users"].create(create_vals)
            except Exception as e:
                _logger.error(e)


class BinotelPartners(models.Model):

    _name = "binotel.partners"
    _description = "Binotel Partners"
    _inherits = {"res.partner": "partner_id"}
    _rec_name = "binotel_name"

    partner_id = fields.Many2one("res.partner", "Partner")
    binotel_id = fields.Char("ID")
    binotel_name = fields.Char("Binotel Name")


class ResPartner(models.Model):

    _inherit = "res.partner"

    def write(self, vals):
        register = self.env["binotel.partner.change.reg"]
        for rec in self:
            registered = register.search([("partner_id", "=", rec.id)])
            if not registered:
                register.create([{"partner_id": rec.id}])
        return super(ResPartner, self).write(vals)


class BinotelPartnersChangeReg(models.Model):

    _name = "binotel.partner.change.reg"
    partner_id = fields.Many2one("res.partner")
