#-*- coding:utf-8 -*-

import json
from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import MissingError, ValidationError

class FormioFormReport(models.Model):
    _name = "formio.form.report"
    _description = "Formio Form Report"

    form_id = fields.Many2one(string="Form",
        comodel_name="formio.form",
        required=True)
    builder_id = fields.Many2one(string="Form Builder",
        comodel_name="formio.builder",
        related="form_id.builder_id",
        store=True)
    name = fields.Char(string="Field Name")
    label = fields.Char(string="Field Label")
    value = fields.Char(string="Value")