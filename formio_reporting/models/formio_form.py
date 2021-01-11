#-*- coding:utf-8 -*-

import json
from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import MissingError, ValidationError

class FormioForm(models.Model):
    _inherit = "formio.form"

    form_report_ids = fields.One2many(string="Reports",
        comodel_name="formio.form.report",
        inverse_name="form_id")

    @api.constrains("submission_data")
    def _generate_form_report_ids(self):
        for form in self:
            form.form_report_ids.unlink()
            form_report_obj = form.form_report_ids
            if not form.submission_data:
                continue

            schema = json.loads(form.builder_id.schema)
            components = schema.get("components", [])
            components_dict = {}
            for component in components:
                components_dict[component["key"]] = component
            if not components_dict:
                continue

            data = json.loads(form.submission_data)
            for key, value in data.items():
                form._create_report_from_component(key, value, components_dict.get(key, {}))

    def _create_report_from_component(self, key, value, component, label=False):
        self.ensure_one()
        form_report_obj = self.env["formio.form.report"]
        component_type = component.get("type", False)
        label = label or component.get("label", False)
        if component_type == "selectboxes":
            for checkbox_key, checkbox_value in value.items():
                if checkbox_value:
                    for component_value in component.get("values"):
                        if component_value["value"] == checkbox_key:
                            form_report_obj.create({
                                "name": key,
                                "label": label,
                                "value": component_value["label"],
                                "form_id": self.id,
                            })
                            break
        elif component_type == "datagrid":
            disabled_fields = []
            datagrid_components = component.get("components", [])
            datagrid_components_dict = {}
            for datagrid_component in datagrid_components:
                datagrid_components_dict[datagrid_component["key"]] = datagrid_component
                if datagrid_component["disabled"]:
                    disabled_fields.append(datagrid_component["key"])
            for datagrid_value in value:
                keys = [key]
                labels = [component["label"]]
                for field in disabled_fields:
                    if datagrid_value.get(field, None):
                        field_value = datagrid_value.pop(field)
                        keys.append(field_value)
                        labels.append(field_value)
                for datagrid_value_key, datagrid_value_value in datagrid_value.items():
                    datagrid_value_component = datagrid_components_dict.get(datagrid_value_key, {})
                    if not datagrid_value_component:
                        continue
                    final_keys = list(keys)
                    final_labels = list(labels)
                    final_keys.append(datagrid_value_key)
                    final_labels.append(datagrid_value_component["label"])
                    self._create_report_from_component(" / ".join(final_keys), datagrid_value_value,
                        datagrid_value_component, label=" / ".join(final_labels))
        elif component_type == "container":
            container_components = component.get("components", [])
            container_components_dict = {}
            for container_component in container_components:
                if container_component["type"] == "columns":
                    for column in container_component["columns"]:
                        for column_component in column["components"]:
                            container_components_dict[column_component["key"]] = column_component
                container_components_dict[container_component["key"]] = container_component
            for container_key, container_value in value.items():
                if container_key not in container_components_dict:
                    continue
                self._create_report_from_component(container_key, container_value, container_components_dict[container_key])
        else:
            if type(value) in [list, dict]:
                return
            elif component_type in ["button","signature"]:
                return
            elif component_type == "radio":
                temp_value = False
                for component_value in component.get("values"):
                    if component_value["value"] == value:
                        temp_value = component_value["label"]
                        break
                value = temp_value
            elif component_type == "select":
                for component_value in component.get("data", {}).get("values", []):
                    if component_value["value"] == value:
                        value = component_value["label"]
                        break

            form_report_obj.create({
                "name": key,
                "label": label,
                "value": str(value),
                "form_id": self.id,
            })