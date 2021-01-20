# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ConfiguratorPanel(models.Model):
    _name = 'sincro_data.configuration_panel'

    sequence = fields.Integer(readonly=True, default=-1)
    name = fields.Char(String="Name")
    # parent_id = fields.Many2one('import_to_facts.configuration_panel', string='Parent field')
    # parent_id = fields.Many2one("res.partner", string="Customer")
    field_id = fields.Many2one('ir.model.fields', string='Odoo field')
    alias_field = fields.Char('Alias')
    domain = fields.Char("Domain")
    # adm_application_import_field_ids = fields.Many2many(
    #     'import_to_facts.import_field',
    #     string="Imported fields",
    #     # store=True,
    #     relation='import_to_facts_config_panel_import_fields'
    # )
    parent_id = fields.Many2one("sincro_data.configuration_panel", string="Parent ID")
    fields = fields.One2many("sincro_data.configuration_panel", "parent_id",
                             string="Configuration Panel Childs")

    # recur_conf_panel_ids = fields.Many2many(
    #     'import_to_facts.configuration_panel',
    #     string="Config Panel Recur",
    #     # store=True,
    #     relation='import_to_facts_recur_config_panel_relation'
    # )
