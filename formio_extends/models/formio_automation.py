#-*- coding:utf-8 -*-

import json
from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import MissingError, ValidationError

class FormioAutomation(models.Model):
    _name = "formio.automation"
    _description = "Formio Automation"
    _rec_name = "builder_id"

    model_id = fields.Many2one(string="Model",
        comodel_name="ir.model",
        required=True)
    builder_id = fields.Many2one(string="Form Builder",
        comodel_name="formio.builder",
        ondelete="restrict")
    mapping_ids = fields.One2many(string="Default Value Mappings",
        comodel_name="formio.automation.mapping",
        inverse_name="automation_id")
    object_form_field_id = fields.Many2one(string="Object Form Field",
        comodel_name="ir.model.fields")
    mail_template_id = fields.Many2one(string="Email Template",
        comodel_name="mail.template")

    @api.model
    def process(self, recs, id):
        if type(id) == int:
            form_automation = self.browse(id)
        else:
            form_automation = self.env.ref(str(id), raise_if_not_found=True)
        if not form_automation:
            raise MissingError("Formio Automation not found!")
        form_builder = form_automation.builder_id
        if not form_builder:
            raise MissingError("No form builder set for formio automation. Contact the system administrator")
        if form_builder.state != "CURRENT":
            raise ValidationError("State of form builder is INVALID. Contact the system administrator.")
        for mapping in form_automation.mapping_ids:
            splitted_keys = mapping.form_field_key.split('.')
            if splitted_keys[-1] not in form_builder.schema:
                raise MissingError("%s not found in form builder schema. Contact the system administrator." % mapping.form_field_key)
        form_obj = self.env["formio.form"]
        for rec in recs:
            submission_data = {}
            for mapping in form_automation.mapping_ids:
                splitted_keys = mapping.form_field_key.split('.')

                looking_dict = submission_data
                for splitted_key in splitted_keys[:-1]:
                    if splitted_key not in submission_data:
                        submission_data[splitted_key] = {}
                    looking_dict = submission_data[splitted_key]

                key = splitted_keys[-1]
                value = rec.mapped(mapping.object_field_name)

                looking_dict[key] = value and value[0] or ""
            form = form_obj.sudo().create({
                "builder_id": form_builder.id,
                "title": form_builder.title,
                "public_share": True,
                "public_access_date_from": datetime.now(),
                "public_access_interval_number": form_builder.public_access_interval_number,
                "public_access_interval_type": form_builder.public_access_interval_type or "minutes",
                "submission_data": json.dumps(submission_data),
                "reference": rec._name + "," + str(rec.id)
            })
            if form_automation.object_form_field_id:
                rec.write({
                    form_automation.object_form_field_id.name: form.id,
                })
            if form_automation.mail_template_id:
                form_automation.mail_template_id.sudo().send_mail(rec.id)
            return form