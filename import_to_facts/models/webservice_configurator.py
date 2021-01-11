# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class WebserviceConfigurator(models.Model):
    _name = 'import_to_facts.webservice_configurator'

    name = fields.Char("Name")
    panel_configuration = fields.Many2one("import_to_facts.configuration_panel", string="Configuration Panel")