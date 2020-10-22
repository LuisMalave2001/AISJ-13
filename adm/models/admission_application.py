# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from ..utils import formatting
import base64
import requests
from urllib.request import urlopen
from odoo.http import content_disposition, dispatch_rpc, request, serialize_exception as _serialize_exception, Response

status_types = [
    ("stage", "Stage"),
    ("done", "Done"),
    ("return", "Return To Parents"),
    ("started", "Application Started"),
    ("submitted", "Submitted"),
    ("cancelled", "Cancelled")
]


class Questions(models.Model):
    _name = "adm.application.question"
    question = fields.Char(string="Question")
    answer = fields.Char(string="Answer")


class ApplicationStatus(models.Model):
    _name = "adm.application.status"
    _order = "sequence"

    name = fields.Char(string="Status Name")
    description = fields.Text(string="Description")
    sequence = fields.Integer(readonly=True, default=-1)
    fold = fields.Boolean(string="Fold")
    type_id = fields.Selection(status_types, string="Type", default='stage')

    partner_id = fields.Many2one("res.partner", string="Customer")

    task_ids = fields.One2many("adm.application.task", "status_id", "Status Ids")

    @api.model
    def create(self, values):
        next_order = self.env['ir.sequence'].next_by_code('sequence.application.task')

        values['sequence'] = next_order
        return super().create(values)


class Gender(models.Model):
    _name = "adm.gender"

    name = fields.Char("Gender")


class Application(models.Model):
    _name = "adm.application"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def _read_group_status_ids(self, stages, domain, order):
        status_ids = self.env['adm.application.status'].search([])
        return status_ids

    # Admission Information
    preferred_degree_program = fields.Many2one("adm.degree_program",
                                               string="Preferred Degree Program")

    # Demographic
    #name = fields.Char(string="Name", compute="_compute_name",
                     #  default="Undefined", related="partner_id.name")
    name = fields.Char(string="Name", related="partner_id.name")
    first_name = fields.Char(string="First Name", related="partner_id.first_name")
    middle_name = fields.Char(string="Middle Name", related="partner_id.middle_name")
    last_name = fields.Char(string="Last Name", related="partner_id.last_name")
    date_of_birth = fields.Date(string="Date of birth", related="partner_id.date_of_birth")
    identification = fields.Char(string="Cedula / ID number", related="partner_id.identification")
    birth_country = fields.Many2one("res.country", string="Birth Country", related="partner_id.country_id")
    birth_city = fields.Char("Birth City", related="partner_id.city")
    gender = fields.Many2one("adm.gender", string="Gender", related="partner_id.gender")
    #gender =  fields.Selection([("m", "male"), ("f", "female")], string="Gender", related="partner_id.gender")

    father_name = fields.Char("Father name")
    mother_name = fields.Char("Mother name")
    family_id = fields.Many2one(related="partner_id.parent_id", string="Family")


    # Contact
    email = fields.Char(string="Email", related="partner_id.email", index=True)
    phone = fields.Char(string="Phone", related="partner_id.mobile")
    home_phone = fields.Char(string="Home phone", related="partner_id.phone")
    other_contacts_ids = fields.One2many("adm.application.other_contacts", "application_id", string="Other Contacts")
    citizenship = fields.Many2one("res.country", string="Citizenship")
    language_spoken = fields.Many2one("adm.language", string="Language Spoken")
    image = fields.Binary("Applicant´s Photo", related="partner_id.image_1920")
    # School
    current_school = fields.Char(string="Current School")
    current_school_address = fields.Char(string="Current School Address")

    grade_level = fields.Many2one(string="GradeLevel", related="inquiry_id.grade_level_id", required=True)

    previous_school = fields.Char(string="Previous School")
    previous_school_address = fields.Char(string="Previous School Address")

    gpa = fields.Float("GPA")
    cumulative_grades = fields.Float("Cumulative Grade")
    regional_exam_grade = fields.Float("Regional Grade")
    bac_grade = fields.Float("BAC Grade")

    # Skills
    language_ids = fields.One2many("adm.application.language", "application_id",
                                   string="Languages", kwargs={
            "website_form_blacklisted": False
        })

    # Location
    country_id = fields.Many2one("res.country", related="partner_id.country_id", string="Country")
    state_id = fields.Many2one("res.country.state", related="partner_id.state_id", string="State")
    city = fields.Char(string="City", related="partner_id.city")
    street = fields.Char(string="Street Address", related="partner_id.street")
    zip = fields.Char("zip", related="partner_id.zip")

    # Relationships
    relationship_ids = fields.One2many(string="Relationship", related="partner_id.relationship_ids", readonly=False)

    # Documentation
    letter_of_motivation_id = fields.Many2one("ir.attachment", string="Letter of motivation")
    cv_id = fields.Many2one("ir.attachment", string="C.V")
    grade_transcript_id = fields.Many2one("ir.attachment", string="Grade transcript")
    letters_of_recommendation_id = fields.Many2one("ir.attachment", string="Letter of recommendation")

    # Additional student info
    resident_status = fields.Selection((('permanent', 'Permanent'), ('transient', 'Transient')),
                                       string="Resident status")
    resident_length_of_stay = fields.Char("Length of stay")

    first_language = fields.Many2one("adm.language", string="First Language")
    first_language_skill_write = fields.Boolean("First Language writing")
    first_language_skill_read = fields.Boolean("First Language reading")
    first_language_skill_speak = fields.Boolean("First Language speaking")
    first_language_skill_listen = fields.Boolean("First Language listening")

    # first_language_skill_write = fields.Many2many("adm.language.skill.type", string="First language skills")

    second_language = fields.Many2one("adm.language", string="Second Language")
    second_language_skill_write = fields.Boolean("Second Language writing")
    second_language_skill_read = fields.Boolean("Second Language reading")
    second_language_skill_speak = fields.Boolean("Second Language speaking")
    second_language_skill_listen = fields.Boolean("Second Language listening")
    # second_language_skills = fields.Many2many("adm.language.skill.type", string="Second language skills")

    third_language = fields.Many2one("adm.language", string="Third Language")
    third_language_skill_write = fields.Boolean("Third Language writing")
    third_language_skill_read = fields.Boolean("Third Language reading")
    third_language_skill_speak = fields.Boolean("Third Language speaking")
    third_language_skill_listen = fields.Boolean("Third Language listening")
    # third_language_skills = fields.Many2many("adm.language.skill.type", string="Third language skills")

    # Signture Attachment
    signature_attach_url = fields.Char("Signature Attachment URL")

    # languages level
    languages_levels = [
        ("beginner", "Beginner"),
        ("elementary", "Elementary"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("fluent", "Fluent")
    ]
    first_level_language = fields.Selection(languages_levels, string="Level", default='beginner')
    second_level_language = fields.Selection(languages_levels, string="Level", default='beginner')
    third_level_language = fields.Selection(languages_levels, string="Level", default='beginner')

    number_years_in_english = fields.Char("Years in English")
    additional_info_other = fields.Char("Other")

    special_education = fields.Boolean("Special Education")
    special_education_desc = fields.Text("Special Education Description")

    psycho_educational_testing = fields.Boolean("Psycho educational testing")

    emotional_support = fields.Boolean("Emotional support")
    emotional_support_desc = fields.Text("Emotional support description")

    iep_education = fields.Boolean("IEP Education")

    # Previous School
    previous_school_ids = fields.One2many("adm.previous_school_description", "application_id")

    # houses
    house_address_ids = fields.One2many(related="family_id.house_address_ids", string="House addresses")

    # Siblings
    sibling_ids = fields.Many2many("res.partner", "application_sibling_ids")

    # References
    isp_community_reference_1 = fields.Char("ISP Community Reference #1")
    isp_community_reference_2 = fields.Char("ISP Community Reference #2")

    personal_reference_contact_information_1 = fields.Char("Personal Reference #1 Contact Information:")
    personal_reference_name_1 = fields.Char("Personal Reference #1 Name")

    personal_reference_contact_information_2 = fields.Char("Personal Reference #2 Contact Information:")
    personal_reference_name_2 = fields.Char("Personal Reference #2 Name")

    # Medical information
    doctor_name = fields.Char("Doctor name")
    doctor_phone = fields.Char("Doctor phone")
    doctor_address = fields.Char("Doctor Direction")
    permission_to_treat = fields.Boolean("Permission To Treat")
    blood_type = fields.Char("Blood Type")
    medical_allergies_ids = fields.One2many(string="Allergies", related="partner_id.medical_allergies_ids",
                                            readonly=False)
    medical_conditions_ids = fields.One2many(string="Conditions", related="partner_id.medical_conditions_ids",
                                             readonly=False)
    medical_medications_ids = fields.One2many(string="Medications", related="partner_id.medical_medications_ids",
                                              readonly=False)

    # Institutional Fee Declaration
    # ===================================================================================================================
    # fee_paid_by_employeer = fields.Boolean()
    # fee_company_name = fields.Char()
    # fee_company_send_invoice = fields.Char()
    # fee_email = fields.Char()
    # fee_signature = fields.Boolean()
    # ===================================================================================================================

    # Meta
    contact_time_id = fields.Many2one("adm.contact_time",
                                      string="Preferred contact time")

    partner_id = fields.Many2one("res.partner", string="Contact")
    status_id = fields.Many2one("adm.application.status",
                                string="Status", group_expand="_read_group_status_ids")
    task_ids = fields.Many2many("adm.application.task")

    inquiry_id = fields.Many2one("adm.inquiry")

    state_tasks = fields.One2many(string="State task", related="status_id.task_ids")

    status_type = fields.Selection(string="Status Type", related="status_id.type_id")
    forcing = False

    family_id = fields.Many2one(string="Family", related="partner_id.parent_id")

    # QUESTION CUSTOMIZED PREESCOLAR

    # DATOS DEL EMBARAZO Y NACIMIENTO
    pe_alguna_complicacion = fields.Char("Alguna complicación")
    pe_peso_al_nacer = fields.Integer("Peso al nacer")
    pe_tipo_parto = fields.Char("Parto Inducido/ Espontáneo/ Cesárea")
    pe_lactancia = fields.Char("Lactancia")
    pe_alimentacion_actual = fields.Char("Alimentación actual")

    # DATOS DEL DESARROLLO MOTOR DEL NIÑO/A
    pe_edad_aprox = fields.Integer("Edad aproximada")
    pe_se_sento = fields.Integer("Se sentó")
    pe_gateo = fields.Integer("Gateó")
    pe_se_paro = fields.Integer("Se paró")
    pe_camino = fields.Integer("Caminó")
    pe_motor_comentario = fields.Char("Comentarios")

    # DATOS DEL DESARROLLO DEL LENGUAJE
    pe_primeras_palabras = fields.Char("Primeras Palabras")
    pe_primeras_frases = fields.Char("Primeras Frases")
    pe_oraciones_completas = fields.Char("Oraciones Completas")
    pe_se_expresa_con_fluidez = fields.Char("Se expresa con fluidez")
    pe_dificultad_lenguaje_expresivo = fields.Char("Dificultad en el lenguaje expresivo")
    pe_pronunciacion = fields.Char("Pronunciación")
    pe_leng_comentario = fields.Char("Comentarios")

    # DATOS DEL DESARROLLO SOCIAL
    pe_panales_dia = fields.Integer("De día")
    pe_panales_noche = fields.Integer("De noche")
    pe_edad_dejo_panales = fields.Integer("¿Edad que dejó los pañales?")
    pe_avisa_bano = fields.Boolean("Avisa para ir al baño")
    pe_puedes_usar_solo_bano = fields.Char("Puede usar solo el baño")
    pe_duerme_toda_noche = fields.Boolean("Duerme toda la noche")
    pe_hora_acostarse = fields.Char("Hora de acostarse")
    pe_hora_despertase = fields.Char("Hora en que se levanta")
    pe_como_se_levanta = fields.Char("¿Cómo se levanta?")
    pe_objeto_para_dormir = fields.Char("¿Necesita algún objeto para dormir?")
    pe_temor_algo = fields.Char("¿Le teme a algo o muestra ansiedad ante alguna situación especial?")
    pe_tipo_estrategia = fields.Char("¿Qué tipo de estrategia se usan en casa para establecer disciplina?")
    pe_comer_sentado = fields.Boolean("¿Acostumbrado a comer sentado?")
    pe_viste_solo = fields.Boolean("¿Se viste o desviste solo?")
    pe_juega_solo = fields.Char("¿Juega solo?")
    pe_escucha_cuento = fields.Char("¿Escucha atentamente un cuento cuando es leído?")
    pe_intereses_preferencias = fields.Char("Intereses y preferencias:")

    # HABILIDADES PARA EL APRENDIZAJE Y VIDA ESCOLAR
    pe_se_concentra = fields.Boolean("¿Logra concentrase en una actividad?")
    pe_termina_lo_que_comienza = fields.Boolean("¿Termina lo que comienza?")
    pe_logra_seguir_indicaciones = fields.Boolean("¿Logra seguir indicaciones?")
    pe_logra_separarse_padres = fields.Boolean("¿Logra separarse de los padres?")
    pe_relacion_otros_ninos = fields.Char("¿Cómo es su relación con otros niños?")
    pe_a_quienes_prefiere_jugar = fields.Char("¿A quiénes prefiere para jugar?")
    pe_experiencia_escolar_previa = fields.Char("Experiencia escolar previa")
    pe_referencia_evaluaciones_anteriores = fields.Char("Referencia de evaluaciones anteriores")
    pe_nee = fields.Char("NEE")
    pe_terapias_clases_especiales = fields.Char("Terapias, clases especiales")
    pe_motivo_eleccion = fields.Char("¿Qué motivó su elección por este colegio?")

    # COMENTARIO ADICIONAL
    pe_comentario_adicional = fields.Char("Comentarios Adicionales")

    # HERMANOS INFORMATION
    brothers = fields.One2many("adm.application.brother", "application_id", "Brothers")

    order_id = fields.Many2one("sale.order", string="Sale Order")

    def message_get_suggested_recipients(self):
        recipients = super().message_get_suggested_recipients()
        try:
            for inquiry in self:
                if inquiry.email:
                    inquiry._message_add_suggested_recipient(recipients, partner=self.partner_id, email=inquiry.email,
                                                             reason=_('Custom Email Luis'))
        except exceptions.AccessError:  # no read access rights -> just ignore suggested recipients because this imply modifying followers
            pass
        return recipients

    def force_back(self):
        status_ids_ordered = self.env['adm.application.status'].search([], order="sequence")
        index = 0
        for status in status_ids_ordered:
            if status == self.status_id:
                break
            index += 1

        index -= 1
        if index >= 0:
            next_status = status_ids_ordered[index]
            self.with_context({'forcing': True}).status_id = next_status

    def print_default(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/report/html/adm.report_default/'+str(self.id),
            'target': '_blank',
            'res_id': self.id,
        }

    def print_custom(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/report/html/adm.report_custom/'+str(self.id),
            'target': '_blank',
            'res_id': self.id,
        }

    # GENERATE THE INTERNAL REPORT AND WILL SAVE INT ATTACHMENT OF THE APPLICATION
    def generate_internal_report(self):
        AttachmentEnv = self.env["ir.attachment"]
        REPORT_ID = 'adm.report_internal_custom'
        pdf = self.env.ref(REPORT_ID).render_qweb_pdf(self.ids)
        # pdf result is a list
        b64_pdf = base64.b64encode(pdf[0])
        # save pdf as attachment
        #requests.session = request.session

        file_id = AttachmentEnv.sudo().create({
            'name': 'Internal Report',
            # 'datas_fname': upload_file.filename,
            'res_name': 'reportInternal.pdf',
            'type': 'binary',
            'res_model': 'adm.application',
            'res_id': self.id,
            'datas': b64_pdf,
           # 'datas': base64.b64encode(urlopen('/report/html/adm.report_internal_custom/'+str(self.id)).read()),
            #'datas': base64.b64encode(s.get(url).content),
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/report/html/adm.report_custom/'+str(self.id),
            'target': '_blank',
            'res_id': self.id,
        }

    def force_next(self):
        status_ids_ordered = self.env['adm.application.status'].sudo().search([], order="sequence")
        index = 0
        for status in status_ids_ordered:
            if status == self.status_id:
                break
            index += 1

        index += 1
        if index < len(status_ids_ordered):
            next_status = status_ids_ordered[index]
            self.with_context({'forcing': True}).status_id = next_status

    def force_status_submitted(self, next_status_id):
        self.with_context({'forcing': True}).status_id = next_status_id

    def move_to_next_status(self):
        self.forcing = False
        status_ids_ordered = self.env['adm.application.status'].search([], order="sequence")
        index = 0
        for status in status_ids_ordered:
            if status == self.status_id:
                # print("Encontrado! -> {}".format(index))
                break
            index += 1

        index += 1
        if index < len(status_ids_ordered):
            next_status = status_ids_ordered[index]

            if self.status_id.type_id == 'done':
                raise exceptions.except_orm(_('Application completed'), _('The Application is already done'))
            elif self.status_id.type_id == 'cancelled':
                raise exceptions.except_orm(_('Application cancelled'), _('The Application cancelled'))
            else:
                self.status_id = next_status

    def cancel(self):
        status_ids_ordered = self.env['adm.application.status'].search([], order="sequence")
        for status in status_ids_ordered:
            if status.type_id == 'cancelled':
                self.status_id = status
                break

    @api.depends("first_name", "middle_name", "last_name")
    def _compute_name(self):
        for record in self:
            record.name = formatting.format_name(record.first_name, record.middle_name, record.last_name)
            record.partner_id.first_name = record.first_name

    @api.depends("first_name", "middle_name", "last_name")
    def _update_contact(self):
        for record in self:
            record.partner_id.first_name = record.first_name

    @api.onchange("first_name", "middle_name", "last_name")
    def _set_full_name(self):
        self.name = formatting.format_name(self.first_name, self.middle_name, self.last_name)

    @api.onchange("country_id")
    def _onchange_country_id(self):
        res = {}
        if self.country_id:
            res['domain'] = {'state_id': [('country_id', '=', self.country_id.id)]}

    @api.model
    def create(self, values):
        first_status = self.env['adm.application.status'].search([], order="sequence")[0]
        values['status_id'] = first_status.id
        values['name'] = formatting.format_name(values['first_name'], values['middle_name'], values['last_name'])

        return super(Application, self).create(values)

    def write(self, values):

        status_ids = self.env['adm.application.status'].sudo().search([])

        first_name = values["first_name"] if "first_name" in values else self.first_name
        middle_name = values["middle_name"] if "middle_name" in values else self.middle_name
        last_name = values["last_name"] if "last_name" in values else self.last_name

        partner_related_fields = dict()
        #partner_related_fields["name"] = values["name"] = formatting.format_name(first_name, middle_name, last_name)

        # "related" in self.fields_get()["email"]
        # Se puede hacer totalmente dinamico, no lo hago ahora por falta de tiempo
        # Pero sin embargo, es totalmente posible. 
        # Los no related directamente no tiene related, y los que si son
        # tiene el campo related de la siguiente manera: (model, field)
        # fields = self.fields_get()

        if "first_name" in values:
           partner_related_fields["first_name"] = first_name
        if "middle_name" in values:
           partner_related_fields["middle_name"] = middle_name
        if "last_name" in values:
           partner_related_fields["last_name"] = last_name

        if "email" in values:
            partner_related_fields["email"] = values["email"]
        if "phone" in values:
            partner_related_fields["mobile"] = values["phone"]
        if "home_phone" in values:
            partner_related_fields["phone"] = values["home_phone"]
        if "country_id" in values:
            partner_related_fields["country_id"] = values["country_id"]
        if "state_id" in values:
            partner_related_fields["state_id"] = values["state_id"]
        if "city" in values:
            partner_related_fields["city"] = values["city"]
        if "street" in values:
            partner_related_fields["street"] = values["street"]
        if "zip" in values:
            partner_related_fields["zip"] = values["zip"]
        if "date_of_birth" in values:
            partner_related_fields["date_of_birth"] = values["date_of_birth"]
        if "identification" in values:
            partner_related_fields["identification"] = values["identification"]

        self.sudo().partner_id.write(partner_related_fields)

        print(status_ids)
        #         PARA PONER VALOR POR DEFECTO
        #         self._context.get('forcing', False):
        if "status_id" in values and not self._context.get('forcing', False):
            if not self.state_tasks & self.task_ids == self.state_tasks and self:
                raise exceptions.ValidationError("All task are not completed")
        else:
            self.forcing = False

        return super().write(values)


class ApplicationOtherContacts(models.Model):
    _name = "adm.application.other_contacts"

    contact_name = fields.Char("Contact Name")
    contact_identification = fields.Char("Contact Identification")

    application_id = fields.Many2one("adm.application", string="Application")


class ApplicationTasks(models.Model):
    _name = "adm.application.task"

    name = fields.Char("Name")
    description = fields.Char("Description")
    status_id = fields.Many2one("adm.application.status", string="Status")


class ApplicationBrothers(models.Model):
    _name = "adm.application.brother"

    name = fields.Char("Name")
    age = fields.Integer("Edad")
    school = fields.Char("Colegio en que estudia")
    application_id = fields.Many2one("adm.application", "Application")


class AdmissionApplicationLanguages(models.Model):
    _name = "adm.application.language"

    language_id = fields.Many2one("adm.language", string="Language")
    language_level_id = fields.Many2one("adm.language.level", string="Language Level")
    application_id = fields.Many2one("adm.application", string="Application")