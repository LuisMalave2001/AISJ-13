#-*- coding:utf-8 -*-

from odoo import models, fields, api

class AdmInquiry(models.Model):
    _inherit = "adm.inquiry"

    form_count = fields.Integer(stirng="Form Count",
        compute="_compute_form_count")

    def _compute_form_count(self):
        for inquiry in self:
            inquiry.form_count = self.env["formio.form"].search_count([("reference","=","adm.inquiry,%s" % inquiry.id)])
    
    def action_open_forms(self):
        self.ensure_one()
        action = self.env.ref("formio.action_formio_form").read()[0]
        action["domain"] = [("reference","=","adm.inquiry,%s" % self.id)]
        return action