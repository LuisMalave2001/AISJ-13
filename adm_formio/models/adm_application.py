# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AdmApplication(models.Model):
    _inherit = "adm.application"

    formio_sent_to_email = fields.Char(string="Formio sent to email")
    formio_reference_form_id = fields.Many2one("formio.form", ondelete="RESTRICT")
    form_count = fields.Integer(stirng="Form Count",
        compute="_compute_form_count")

    def _compute_form_count(self):
        for application in self:
            application.form_count = self.env["formio.form"].search_count([("reference","=","adm.application,%s" % application.id)])
    
    def action_open_forms(self):
        self.ensure_one()
        action = self.env.ref("formio.action_formio_form").read()[0]
        action["domain"] = [("reference","=","adm.application,%s" % self.id)]
        return action
