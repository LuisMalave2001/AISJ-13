# -*- coding: utf-8 -*-
import logging
from odoo import http
from datetime import datetime
import base64
import itertools
import re
import json
from odoo.http import content_disposition, dispatch_rpc, request, \
    serialize_exception as _serialize_exception, Response
from odoo.addons.adm.controllers.admission_controller import \
    AdmissionController

_logger = logging.getLogger(__name__)


class ApplicationController(AdmissionController):

    @http.route("/admission/applications/create", auth="public",
                methods=["POST"], website=True, csrf=False)
    def info_create_post(self, **params):
        PartnerEnv = http.request.env["res.partner"]
        ApplicationEnv = http.request.env["adm.application"]

        field_ids = http.request.env.ref(
            "adm.model_adm_application").sudo().field_id
        fields = [field_id.name for field_id in field_ids]
        keys = params.keys() & fields
        result = {k: params[k] for k in keys}
        field_types = {field_id.name: field_id.ttype for field_id in field_ids}

        # sibling_name_list = post_parameters().getlist("sibling_name")
        # sibling_age_list = post_parameters().getlist("sibling_age")
        # sibling_school_list = post_parameters().getlist("sibling_school")

        many2one_fields = [name for name, value in field_types.items() if
                           value == "many2one"]

        # siblings = [(5, 0, 0)]
        # for idx in range(len(sibling_name_list)):
        #     if sibling_name_list[idx] != '' and sibling_age_list[idx] !=
        #     '' and sibling_school_list[idx] != '':
        #         siblings.append((0, 0, {
        #             'name': sibling_name_list[idx],
        #             'age': sibling_age_list[idx],
        #             'school': sibling_school_list[idx],
        #             }))
        # result["sibling_ids"] = siblings

        for key in result.keys():
            if key in many2one_fields:
                result[key] = int(result[key])
                if result[key] == -1:
                    result[key] = False
                    pass

        parent = http.request.env.user.partner_id.sudo()
        family = parent.family_ids and parent.family_ids[0]

        if not family:
            family = PartnerEnv.sudo().create({
                'name': 'Family of %s' % parent.name,
                'is_family': True,
                'is_company': True,
                'member_ids': [(4, parent.id, False)]
                })
            parent.write({
                'family_ids': [(4, family.id, False)]
                })

        # noinspection PyUnresolvedReferences
        partner = PartnerEnv.sudo().create({
            "first_name": result.get("first_name"),
            "middle_name": result.get("middle_name"),
            "last_name": result.get("last_name"),
            "image_1920": params.get("file_upload") and base64.b64encode(
                params["file_upload"].stream.read()),
            "parent_id": family.id,
            "person_type": "student",
            "family_ids": [(4, family.id, False)],
            })
        family.write({
            'member_ids': [(4, partner.id, False)]
            })
        application = ApplicationEnv.create({
            "first_name": result.get("first_name"),
            "middle_name": result.get("middle_name"),
            "last_name": result.get("last_name"),
            "partner_id": partner.id,
            "responsible_user_id": request.env.user.id
            })
        result["relationship_ids"] = [(0, 0, {
            "partner_2": parent.id
            })]
        application.sudo().write(result)

        return (http.request
                .redirect("/admission/applications/%s" % application.id))

    @http.route("/admission/applications/"
                "<model(adm.application):application_id>/check", auth="public",
                methods=["POST"], website=True, csrf=False)
    def check_application(self, application_id, **params):

        # if len(self.getPendingTasks(application_id)) == 0:
        # BUSCAMOS EL STATUS QUE SEA DE TIPO SUBMITTED PARA TRANSLADAR
        # LA PETICION DEL USUARIO
        #     StatusEnv = request.env["adm.application.status"].sudo()
        #     statusSubmitted = (StatusEnv.browse(StatusEnv
        #                        .search([('type_id', '=', 'submitted')])))
        #     application_id.sudo().force_status_submitted(
        #     statusSubmitted.id.id)

        return request.redirect(
            http.request.httprequest.referrer + "?checkData=1")

    @http.route("/admission/adm_insertId", auth="public", methods=["GET"],
                cors='*', csrf=False)
    def insert_id(self, **kw):
        # define una funcion principal
        return json.dumps(request.httprequest.headers.environ['HTTP_ORIGIN'])

    #####################
    # Application Pages #
    #####################
    @http.route("/admission/applications/"
                "<model(adm.application):application_id>/", auth="public",
                methods=["GET"], website=True, csrf=False)
    def see_application(self, application_id, **params):
        return request.render("adm.template_application_menu_instructions",
                              self.compute_view_render_params(application_id))

    @http.route("/admission/applications", auth="public", methods=["GET"],
                website=True)
    def admission_list(self, **params):

        # obtenemos todos los registros de reenrollment en las cuales el
        # estudiante asociado este relacionado mediante la familia con el
        # user que esta accediendo dede el portal.
        application_ids = request.env.user.application_ids
        response = http.request.render(
            "adm.template_admission_application_list", {
                "application_ids": application_ids,
                })
        return response

    @http.route("/admission/applications/"
                "<model(adm.application):application_id>/info", auth="public",
                methods=["GET"], website=True, csrf=False)
    def info(self, application_id, **params):
        return request.render("adm.template_application_student_info",
                              self.compute_view_render_params(application_id))

    @http.route("/admission/applications/"
                "<model(adm.application):application_id>/medical-info",
                auth="public", methods=["GET"], website=True, csrf=False)
    def medical_info(self, application_id, **params):
        return request.render("adm.template_application_menu_medical_info",
                              self.compute_view_render_params(application_id))

    @http.route(
        "/admission/applications/"
        "<model('adm.application'):application_id>/additional-questions",
        auth="public", methods=["GET"], website=True)
    def get_additional_questions(self, application_id):

        response = request.render(
            'adm.template_application_additional_questions_webpage',
            AdmissionController.compute_view_render_params(application_id))
        return response

    @http.route("/admission/applications/"
                "<model(adm.application):application_id>/document-comun",
                auth="public", methods=["GET"], website=True, csrf=False)
    def document_document_comun(self, application_id, **params):
        return (request
                .render("adm.template_application_menu_upload_file_comun",
                        self.compute_view_render_params(application_id)))

    @http.route("/admission/applications/"
                "<model('adm.application'):application_id>/"
                "parent-questionnaire", auth="public", methods=["GET"],
                website=True)
    def get_questionnaire(self, application_id):
        return request.render(
            'adm.template_application_parent_questionnaire_webpage',
            AdmissionController.compute_view_render_params(application_id))

    @http.route("/admission/applications/"
                "<model('adm.application'):application_id>/family/parents",
                auth="public", methods=["GET"], website=True)
    def get_parents(self, application_id):
        return request.render('adm.template_application_parents_webpage',
                              AdmissionController
                              .compute_view_render_params(application_id))

    @http.route("/admission/applications/"
                "<model('adm.application'):application_id>/schools",
                auth="public", methods=["GET"], website=True)
    def get_school(self, application_id):
        return request.render(
            'adm.template_application_schools_information_webpage',
            AdmissionController.compute_view_render_params(application_id))

    @http.route("/admission/applications/"
                "<model('adm.application'):application_id>/family/siblings",
                auth="public", methods=["GET"], website=True)
    def get_siblings(self, application_id):
        return request.render(
            'adm.template_application_siblings_webpage',
            AdmissionController.compute_view_render_params(application_id))
