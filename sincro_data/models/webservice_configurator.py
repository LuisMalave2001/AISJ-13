# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class WebserviceConfigurator(models.Model):
    _name = 'sincro_data.webservice_configurator'

    name = fields.Char("Name")
    panel_configuration = fields.Many2one("sincro_data.configuration_panel", string="Configuration Panel")
    domain = fields.Char("Domain")
    label = fields.Char("Label")
    model_id = fields.Many2one('ir.model', string='Model')