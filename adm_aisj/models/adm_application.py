# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AdmApplication(models.Model):
    _inherit = 'adm.application'

    passport_number_1 = fields.Char()
    passport_number_2 = fields.Char()
    passport_expiration_date = fields.Date()
    expected_starting_date = fields.Date()

    upload_passport_copy_attachment_id = fields.Many2one('ir.attachment', string="Upload passport copy")
    permit_copy_attachment_id = fields.Many2one('ir.attachment', string="Upload Iqama/ Residency Permit Copy")

    # Parent/Guardian relation
    # I know we can use relationship_ids field, but, this can make the things really
    # complicated.
    # So, a simple silution is create a specific field for then
    guardian_relationship1_id = fields.Many2one('school_base.relationship')
    guardian_relationship2_id = fields.Many2one('school_base.relationship')

    guardian1_partner_id = fields.Many2one('res.partner')
    guardian2_partner_id = fields.Many2one('res.partner')

    # Guardian 1
    guardian_relationship1_id_residency_permit_id_number = fields.Many2one('ir.attachment')
    guardian_relationship1_id_parent_passport_upload = fields.Many2one('ir.attachment')

    # Guardian 2
    guardian_relationship2_id_residency_permit_id_number = fields.Many2one('ir.attachment')
    guardian_relationship2_id_parent_passport_upload = fields.Many2one('ir.attachment')

    immunization_history_attachment_id = fields.Many2one('ir.attachment')
    immunization_history_attachment_id_data = fields.Binary(related='immunization_history_attachment_id.datas')
    testing_attachment = fields.Binary('lol', attachment=True)

    report_cards_attachment_id = fields.Many2one('ir.attachment')
    report_cards_attachment_id_data = fields.Binary(related='report_cards_attachment_id.datas')

    previous_school_profile_attachment_id = fields.Many2one('ir.attachment')
    previous_school_profile_attachment_id_data = fields.Binary(related='previous_school_profile_attachment_id.datas')

    standardized_tests_attachment_id = fields.Many2one('ir.attachment')
    standardized_tests_attachment_id_data = fields.Binary(related='standardized_tests_attachment_id.datas')

    family_identification_document_attachment_id = fields.Many2one('ir.attachment')
    amily_identification_document_attachment_id_data = fields.Binary(related='family_identification_document_attachment_id.datas')

    special_evaluation_report_attachment_id = fields.Many2one('ir.attachment')
    special_evaluation_report_attachment_id_data = fields.Binary(related='special_evaluation_report_attachment_id.datas')

    business_card_attachment_id = fields.Many2one('ir.attachment')
    business_card_attachment_id_data = fields.Binary(related='business_card_attachment_id.datas')

    c_aisj_parent_questionaire_sel = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ]

    c_aisj_parent_quest_math = fields.Selection(c_aisj_parent_questionaire_sel)
    c_aisj_parent_quest_english = fields.Selection(c_aisj_parent_questionaire_sel)
    c_aisj_parent_quest_language = fields.Selection(c_aisj_parent_questionaire_sel)
    c_aisj_parent_quest_sciences = fields.Selection(c_aisj_parent_questionaire_sel)
    c_aisj_parent_quest_history = fields.Selection(c_aisj_parent_questionaire_sel)
    c_aisj_parent_quest_pe = fields.Selection(c_aisj_parent_questionaire_sel)
    c_aisj_parent_quest_arts = fields.Selection(c_aisj_parent_questionaire_sel)
    c_aisj_parent_quest_social_studies = fields.Selection(c_aisj_parent_questionaire_sel)
    c_aisj_parent_quest_arabic = fields.Selection(c_aisj_parent_questionaire_sel)

    # You might ask, why we use numbers?
    # That's because there are too many of these question
    c_aisj_parent_questionaire_q1 = fields.Char("My child's challenged at school include")
    c_aisj_parent_questionaire_q2 = fields.Char("In What activities outside of school is your child involved?")

    c_aisj_parent_questionaire_q3 = fields.Selection([
        ('fluent', 'Fluent'),
        ('limited', 'Limited'),
        ('beginner', 'Beginner'),
        ], "Applicant's proficiency in English")

    c_aisj_parent_questionaire_q4 = fields.Many2many(
        'adm_aisj.applicant.programs',
        string="Has the applicant received any of the following programs?")

    c_aisj_parent_questionaire_q5 = fields.Many2many(
        'adm_aisj.additional.support',
        string="Has your child ever received additional support in-school or"
               " outside of school in the following areas?")

    c_aisj_parent_questionaire_q6 = fields.Many2many(
        'adm_aisj.interested.options',
        string="Why are you interested in AISJ for your child?")

    c_aisj_parent_questionaire_q7 = fields.Text("What experiences are you hoping your child will have at AISJ?")
    c_aisj_parent_questionaire_q8 = fields.Many2many(
        'adm_aisj.how.hear.about.us',
        string="How did you hear about us?")

    c_aisj_parent_questionaire_q9 = fields.Char("Is there anything you really want us to know about your family as you apply to AISJ?")
    c_aisj_parent_questionaire_q10 = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        "Has your family attended an Admissions visit or tour at AISJ?")

    c_aisj_additional_questions_q1 = fields.Selection([
        ('adjusts_with_ease', "Adjusts with ease to new situations"),
        ('take_time', "Takes time to adjust to new situation"),
        ('list_ideas', "List any ideas that would ease adjustment to AISJ."),
    ], string="My Child")

    c_aisj_additional_questions_q1_list = fields.Char(string="List any ideas that would ease adjustment to AISJ.")

    c_aisj_additional_questions_q2 = fields.Selection([
                ('academic_program', "Academic Program"),
                ('after_school_activities', "After School Activities"),
                ('arts', "Arts"),
                ('athletics', "Athletics"),
                ('class_sizes', "Class Sizes"),
                ('diverse_student_body', "Diverse student Body"),
                ('english_additional', "English as an additional Language"),
                ('experienced_faculty', "Experienced Faculty"),
                ('learning_support', "Learning Support"),
                ('location', "Location"),
                ('school_fees', "School Fees"),
                ('university_acceptances', "University Acceptances"),
                ('volunteer_opportunities', "Volunteer Opportunities"),
                ('other', "Other"),
        ], string="What is important to you when choosing a school?")
    c_aisj_additional_questions_q3 = fields.Char("Has your child ever been on academic probation?")
    c_aisj_additional_questions_q4 = fields.Char("Has your child ever been asked to withdraw from a school?")

    c_aisj_parent_q1 = fields.Selection([
                ('father_and_mother', "Father and mother"),
                ('father_and_stepmother', "Father and stepmother"),
                ('father_only', "Father only"),
                ('mother_and_stepfather', "Mother and stepfather"),
                ('mother_only', "Mother only"),
                ('grandparents', "Grandparents"),
                ('shares_time_with_both_parents', "Shares time with both parents"),
                ('other', "Other"),
        ], string="With whom does the applicant live?")
    c_aisj_parent_q2 = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Does your employer pay tuition directly to the school?")

    c_aisj_schools_q1 = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Has your child applied to The American International School of Jeddah before?")
    c_aisj_schools_q2 = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Has your child attended The American International School of Jeddah Before?")

    c_aisj_elementary_q1 = fields.Boolean(string="Has your child been previously enrolled in a daycare/preschool program?")
    c_aisj_elementary_q1_age = fields.Integer(string="Age")
    c_aisj_elementary_q1_country_id = fields.Many2one('res.country', string="Country")

    c_aisj_elementary_q2 = fields.Boolean(string="Is your child toilet trained?")
    c_aisj_elementary_q2_age = fields.Integer(string="At what age did your child toilet train?")

    c_aisj_elementary_q3 = fields.Boolean(string="Does your child communicate using words/phrases?")

    ELEMENTARY_SELECTION_QUESTIONS = [
        ('always', "Always"),
        ('most_of_the_time', "Most of the time"),
        ('sometimes', "Sometimes"),
        ('rarely', "Rarely"),
        ('never', "Never"),
        ]

    c_aisj_elementary_q4 = fields.Selection(ELEMENTARY_SELECTION_QUESTIONS, string="Is your child able to separate from you easily?")
    c_aisj_elementary_q5 = fields.Selection(ELEMENTARY_SELECTION_QUESTIONS, string="Does your child express appropriate emotions depending on his/her mood?")
    c_aisj_elementary_q6 = fields.Selection(ELEMENTARY_SELECTION_QUESTIONS, string="Does your child make eye contact while speaking or playing with you?")
    c_aisj_elementary_q7 = fields.Selection(ELEMENTARY_SELECTION_QUESTIONS, string="Does your child interact and engage with other children?")
    c_aisj_elementary_q8 = fields.Selection(ELEMENTARY_SELECTION_QUESTIONS, string="Does your child interact and engage with familiar adults?")
    c_aisj_elementary_q9 = fields.Selection(ELEMENTARY_SELECTION_QUESTIONS, string="Does your child eat regular meals and snack independently?")
    c_aisj_elementary_q10 = fields.Selection(ELEMENTARY_SELECTION_QUESTIONS, string="Does your child sleep in regular routines (naps, nighttime)?")
    c_aisj_elementary_q11 = fields.Selection(ELEMENTARY_SELECTION_QUESTIONS, string="Does your child show interest in a variety of activities?")
    c_aisj_elementary_q12 = fields.Selection(ELEMENTARY_SELECTION_QUESTIONS, string="Does your child focus on one activity for more than 10 minutes (not including TV)?")
    c_aisj_elementary_q13 = fields.Selection(ELEMENTARY_SELECTION_QUESTIONS, string="Does your child follow simple instructions?")
    c_aisj_elementary_q14 = fields.Selection(ELEMENTARY_SELECTION_QUESTIONS, string="Does your child follow rules (at home, or at school)?")

    grant_aisj_photo_permission = fields.Boolean(string="Grant Aisj photo permission")


class ApplicationSiblings(models.Model):
    _inherit = "adm.application.sibling"

    aisj_status = fields.Selection([('attending_to_aisj', 'Attending to AISJ'), ('applying', 'Applying to AISJ'), ('neither', 'Neither'), ], string='Status')
    c_aisj_relationship_to_application = fields.Char()
    c_years_attended = fields.Char()
