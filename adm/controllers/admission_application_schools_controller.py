# -*- coding: utf-8 -*-
import logging
from odoo import http
from datetime import datetime
import base64
import itertools
import re
import json
from odoo.http import content_disposition, dispatch_rpc, request, serialize_exception as _serialize_exception, Response
from odoo.addons.adm.controllers.admission_application_controller import AdmissionController

_logger = logging.getLogger(__name__)


def get_parameters():
    return request.httprequest.args


def post_parameters():
    return request.httprequest.form


def lookup(s, lookups):
    for pattern, value in lookups:
        if re.search(pattern, s):
            return value


class Admission(http.Controller):

    @staticmethod
    def get_partner():
        return request.env["res.users"].browse([request.session.uid]).partner_id

    @staticmethod
    def _login_redirect(uid, redirect=None):
        return redirect if redirect else '/web'

    # < model("res.country"): country >
    @http.route("/admission/applications/<model('adm.application'):application_id>/schools", auth="public", methods=["GET"], website=True)
    def get_siblings(self, application_id):
        # contact_id = self.get_partner()
        # ApplicationEnv = request.env["adm.application"]
        #
        # contact_time_ids = request.env["adm.contact_time"].browse(request.env["adm.contact_time"].search([])).ids
        # degree_program_ids = request.env["adm.degree_program"].browse(request.env["adm.degree_program"].search([])).ids
        #
        # application_status_ids = request.env["adm.application.status"].browse(request.env["adm.application.status"].search([])).ids
        #
        # student_application = ApplicationEnv.browse([application_id])
        # language_ids = request.env['adm.language'].browse(http.request.env['adm.language'].search([]))
        # language_level_ids = request.env['adm.language.level'].browse(request.env['adm.language.level'].search([]))

        response = request.render('adm.template_application_schools_information_webpage', AdmissionController.compute_view_render_params(application_id))
        return response
