'''
Created on Feb 1, 2020

@author: LuisMora s
'''
from odoo import models, fields


class Relationship(models.Model):
    _name = "school_base.relationship"

    partner_1 = fields.Many2one("res.partner", string="Partner 1", required=True, ondelete="cascade")
    partner_2 = fields.Many2one("res.partner", string="Partner", required=True, ondelete="cascade")
    family_id = fields.Many2one("res.partner", string="Family", required=True, domain=[('is_family', '=', True)])
    relationship_type_id = fields.Many2one("school_base.relationship_type", string="Relationship")
    custody = fields.Boolean(string="Custody")
    correspondence = fields.Boolean(string="Correspondence")
    grand_parent = fields.Boolean(string="Grand Parent")
    grade_related = fields.Boolean(string="Grade Related")
    family_portal = fields.Boolean(string="Family Portal")
    is_emergency_contact = fields.Boolean("Is an emergency contact?")

    # relationship_type = fields.Selection([
    #         ('sibling', "Sibling"),
    #         ('father', "Father"),
    #         ('mother', "Mother"),
    #         ('uncle', "Uncle"),
    #         ('grandmother', "Grandmother"),
    #         ('grandfather', "Grandfather"),
    #         ('other', "Other"),
    #     ],
    #     string="Type", default='other'
    # )
