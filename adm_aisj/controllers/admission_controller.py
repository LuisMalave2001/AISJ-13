# -*- coding: utf-8 -*-

from odoo.http import request

from odoo.addons.adm.models.application.admission_application \
    import Application
from odoo.addons.adm.controllers.admission_controller import \
    AdmissionController


class AisjAdmissionController(AdmissionController):

    def compute_view_render_params(self, application_id: Application):
        params = (super(AisjAdmissionController, self)
                  .compute_view_render_params(application_id))

        from odoo import api, SUPERUSER_ID

        env = api.Environment(request.env.cr, SUPERUSER_ID, request.env.context)
        additional_support_ids = env['adm_aisj.additional.support'].search([])
        applicant_programs_ids = env['adm_aisj.applicant.programs'].search([])
        interested_options_ids = env['adm_aisj.interested.options'].search([])
        how_hear_about_us_ids = env['adm_aisj.how.hear.about.us'].search([])

        params.update({
            'additional_support_ids': additional_support_ids,
            'applicant_programs_ids': applicant_programs_ids,
            'interested_options_ids': interested_options_ids,
            'how_hear_about_us_ids': how_hear_about_us_ids,
            })

        return params
