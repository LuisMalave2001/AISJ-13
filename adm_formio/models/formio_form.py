#-*- coding:utf-8 -*-

from odoo import models, fields, api

class FormioForm(models.Model):
    _inherit = "formio.form"

    reference = fields.Reference(selection_add=[
        ("adm.inquiry","Inquiry"),
        ("adm.application","Application")])

    admission_to_email = fields.Char("Email to")
