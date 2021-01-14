# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    """  Settings for school base module """
    _inherit = "res.config.settings"

    adm_application_required_field_ids = fields.Many2many(
        'ir.model.fields',
        domain="[('model', '=', 'adm.application')]",
        string="Application required fields",
        store=True,
        relation='adm_app_required_fields')

    adm_application_optional_field_ids = fields.Many2many(
        'ir.model.fields',
        domain="[('model', '=', 'adm.application')]",
        string="Application optional fields",
        store=True,
        relation='adm_app_optional_fields')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()

        config_parameter = self.env['ir.config_parameter'].sudo()
        application_required_fields_str = config_parameter.get_param(
            'adm_application_required_field_ids', '')
        application_required_fields = [
            int(e) for e in application_required_fields_str.split(',')
            if e.isdigit()
            ]

        application_optional_fields_str = config_parameter.get_param(
            'adm_application_optional_field_ids', '')
        application_optional_fields = [
            int(e) for e in application_optional_fields_str.split(',')
            if e.isdigit()
            ]

        res.update({
            'adm_application_required_field_ids': application_required_fields,
            'adm_application_optional_field_ids': application_optional_fields,
            })

        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        for settings in self:
            config_parameter = self.env['ir.config_parameter'].sudo()
            config_parameter.set_param(
                'adm_application_required_field_ids', ",".join(
                    map(str, settings.adm_application_required_field_ids.ids)))
            config_parameter.set_param(
                'adm_application_optional_field_ids', ",".join(
                    map(str, settings.adm_application_optional_field_ids.ids)))
