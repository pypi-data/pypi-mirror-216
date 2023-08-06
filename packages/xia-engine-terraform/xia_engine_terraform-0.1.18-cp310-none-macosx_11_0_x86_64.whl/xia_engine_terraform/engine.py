from typing import Type
import subprocess
import os
import json
import shutil
import logging
import requests
from jinja2 import Template
from xia_fields import StringField, OsEnvironField
from xia_engine import BaseDocument, EmbeddedDocument
from xia_engine import Engine


class TerraformConnectParam(EmbeddedDocument):
    state_path = StringField(description="State File location", required=True)
    template_path = StringField(description="Terraform Template Location", required=True)
    runtime_path = StringField(description="Terraform Runtime Location", required=True)
    tf_state_field = StringField(description="The document field name which should hold the tf job states")
    feedback_url = OsEnvironField(description="OS environment Feedback URL")
    feedback_api_key = OsEnvironField(description="OS environment APP API Key")


class TerraformClient:
    backend_tf = ""

    def __init__(self, template_path: str, runtime_path: str, tf_state_field: str = None,
                 feedback_url: str = None, feedback_api_key: str = None,
                 timeout: int = 60, **kwargs):
        os.makedirs(template_path, exist_ok=True)
        os.makedirs(runtime_path, exist_ok=True)
        self.template_path = template_path
        self.runtime_path = runtime_path
        self.state_path = "."  # state file stored at the same directory as runtime
        self.tf_state_field = tf_state_field
        self.feedback_url = feedback_url
        self.feedback_api_key = feedback_api_key
        self.time_out = timeout
        self.other_params = kwargs.copy()

    def get_db_params(self):
        return self.other_params

    def prepare_state(self, document_class: Type[BaseDocument], doc_id: str):
        """Prepare the location to store state

        Args:
            document_class: Document class
            doc_id: document ID

        Returns:
            state_path for the current document
        """

    def clean_state(self, document_class: Type[BaseDocument], doc_id: str):
        """Clean the state file

        Args:
            document_class: Document class
            doc_id: document ID
        """

    def get_state_path(self, document_class: Type[BaseDocument], doc_id: str):
        """Calculate the state file location

        Args:
            document_class: Document class
            doc_id: document ID

        Returns:
            state_path for the current document
        """

    def prepare_runtime(self, db_params: dict, document_class: Type[BaseDocument], doc_id: str, display_content: dict):
        """Prepare runtime terraform files

        Args:
            db_params: Database parameter
            document_class: Document class related
            doc_id: Document ID
            display_content: document content in database form

        Returns:
            runtime path
        """
        resource_type = document_class.__name__
        dest_dir = self.runtime_path + os.path.sep + resource_type + os.path.sep + doc_id
        source_dir = None
        for template_class in [klass for klass in document_class.mro() if issubclass(document_class, BaseDocument)]:
            source_dir = self.template_path + os.path.sep + template_class.__name__
            if not os.path.exists(source_dir):
                continue
            else:
                break
        if not source_dir:
            raise ValueError(f"Terraform template cannot be found at template_path/{resource_type}")

        os.makedirs(dest_dir, exist_ok=True)

        # Iterate through the files in the source directory
        for root, dirs, files in os.walk(source_dir):
            dest_subdir = os.path.join(dest_dir, root[len(source_dir):].lstrip(os.sep))
            os.makedirs(dest_subdir, exist_ok=True)

            # Copy the files in the current directory to the corresponding destination directory
            for file_name in files:
                source_file_path = os.path.join(root, file_name)
                dest_file_path = os.path.join(dest_subdir, file_name)

                with open(source_file_path, 'rb') as source_file:
                    with open(dest_file_path, 'wb') as dest_file:
                        if source_file_path.endswith(".tf"):
                            if source_file_path.endswith("provider.tf"):
                                template = Template(source_file.read().decode())
                                tf_file = template.render(db_params)
                            elif source_file_path.endswith("backend.tf"):
                                continue   # backend tf is related to engine type
                            else:
                                template_str = source_file.read().decode()
                                template_str = "\n".join([ln for ln in template_str.split("\n")
                                                          if ln.strip() != "default = null  #xia#"])
                                template_str = template_str.replace("#xia# ", "")
                                template = Template(template_str, lstrip_blocks=True, trim_blocks=True)
                                tf_file = template.render(display_content)
                            dest_file.write(tf_file.encode())
                        else:
                            dest_file.write(source_file.read())
            with open(os.path.join(dest_dir, "backend.tf"), "wb") as fp:
                template = Template(self.backend_tf)
                tf_file = template.render(db_params)
                fp.write(tf_file.encode())

        return self.runtime_path + "/" + resource_type + "/" + doc_id

    def clean_runtime(self, document_class: Type[BaseDocument], doc_id: str):
        """Clean runtime directory

        Args:
            document_class: Document class
            doc_id: Document ID
        """
        resource_type = document_class.__name__
        dest_dir = self.runtime_path + os.path.sep + resource_type + os.path.sep + doc_id
        for root, dirs, files in os.walk(dest_dir):
            for file in files:
                if file.endswith('.tf') or file.endswith(".lock.hcl") or file.endswith(".json"):
                    os.remove(os.path.join(root, file))
        for root, dirs, files in os.walk(dest_dir):
            for directory in dirs:
                if directory == '.terraform':
                    dir_to_delete = os.path.join(root, directory)
                    shutil.rmtree(dir_to_delete)

    def _feedback(self, document_class: Type[BaseDocument], doc_id: str, runtime_tf_path: str) -> int:
        """Send the feedback to remote API

        Args:
            document_class: Clean runtime directory
            doc_id: Document ID

        Returns:
            http return code or None if feedback is not supported by the current configuration

        """
        if self.feedback_url and not self.feedback_url.startswith("XIA_") and self.tf_state_field:
            # feedback url starts with XIA_ => URL not configured
            output_result = subprocess.run(['terraform', f"-chdir={runtime_tf_path}", 'output', '-json'],
                                           check=False, capture_output=True, text=True)
            if output_result.returncode != 0:
                logging.error(f"{document_class.__name__}/{doc_id} tf-output failed: {output_result.stderr}")
                return 500
            db_content = self.parse_output(output_result.stdout)
            if db_content.get(self.tf_state_field, "") != "process":
                # We could only send the feedback when the status is not process
                api_endpoint = "/".join([self.feedback_url, document_class.__name__])
                api_headers = {"X-Api-Key": self.feedback_api_key} if self.feedback_api_key else {}
                db_content.pop("_unknown", None)  # We don't send back unknown fields
                r = requests.put(api_endpoint + "/_id/" + doc_id, headers=api_headers, json=db_content)
                if r.status_code > 300:
                    logging.error(f"Feedback error on {document_class.__name__}/{doc_id}")
                return r.status_code

    @classmethod
    def parse_output(cls, output: str):
        """Parse the output into data

        Args:
            output: string (in json format)

        Returns:
            Should be with json format
        """
        return {k: v["value"] for k, v in json.loads(output).items()}

    def lock_wait(self, document_class: Type[BaseDocument], doc_id: str):
        """Wait until the lock is released

        Args:
            document_class: Document class
            doc_id: Document id

        Notes:
            Will use the timeout at the objectif level
        """

    @classmethod
    def _set_status(cls, runtime_tf_path: str, tf_state: str, tf_state_field: str = None) -> str:
        """Update the tf job status

        Args:
            runtime_tf_path: Current running path
            tf_state: Job status to be set
            tf_state_field: The output field should contain tf state

        Returns
            tf state
        """
        if tf_state_field is None:
            return tf_state  # Nothing to update, so we return the given state value
        state_file_location = os.path.join(runtime_tf_path, "state.json")
        with open(state_file_location, "w") as state_file:
            subprocess.run(['terraform', f"-chdir={runtime_tf_path}", 'state', "pull", "-no-color"],
                           check=True, stdout=state_file)
        with open(state_file_location) as state_file:
            state_file_data = state_file.read()
            if not state_file_data:  # Should raise error before
                raise RuntimeError("No state file detected")
            state_info = json.loads(state_file_data)
        state_info["outputs"]["tf_state"]["value"] = tf_state
        state_info["serial"] += 1
        with open(state_file_location, "w") as state_file:
            json.dump(state_info, state_file, indent=2)
        push_result = subprocess.run(['terraform', f"-chdir={runtime_tf_path}", 'state', "push", "-no-color",
                                      "state.json"], check=True, capture_output=True, text=True)
        if push_result.returncode != 0:
            logging.error(f"Push state failed from {runtime_tf_path}: {push_result.stderr}")
        return tf_state

    def apply(self, db_params: dict, document_class: Type[BaseDocument], doc_id: str, display_content: dict) -> str:
        """Apply the modification and return running result

        Args:
            db_params: Database connection parameters
            document_class: Document Class
            doc_id: Document id
            display_content: display contents

        Returns:
            job status
        """
        if not doc_id:
            raise ValueError("Document without primary key is not supported by Terraform Engine")
        if self.tf_state_field and display_content.get(self.tf_state_field, "") != "process":
            return display_content.get(self.tf_state_field, "")  # job status is not process, do nothing
        tf_state_field = self.tf_state_field
        tfstate_path = self.prepare_state(document_class, doc_id)
        db_params["tfstate_path"] = tfstate_path
        runtime_tf_path = self.prepare_runtime(db_params, document_class, doc_id, display_content)
        init_result = subprocess.run(['terraform', f"-chdir={runtime_tf_path}", 'init', "-no-color"],
                                     check=False, capture_output=True, text=True)
        if init_result.returncode != 0:
            raise RuntimeError(f"{document_class.__name__}/{doc_id} tf-init failed: {init_result.stderr}")

        self.lock_wait(document_class, doc_id)
        apply_result = subprocess.run(['terraform', f"-chdir={runtime_tf_path}", 'apply', '-auto-approve', "-no-color"],
                                      check=False, capture_output=True, text=True)
        if apply_result.returncode != 0:
            logging.error(f"{document_class.__name__}/{doc_id} tf-apply failed: {apply_result.stderr}")
            tf_state = self._set_status(runtime_tf_path, "apply_failed", tf_state_field)
            self._feedback(document_class, doc_id, runtime_tf_path)
            self.clean_runtime(document_class, doc_id)
            raise RuntimeError(f"Document {document_class.__name__}/{doc_id} apply failed")
        else:
            tf_state = self._set_status(runtime_tf_path, "complete", tf_state_field)
            self._feedback(document_class, doc_id, runtime_tf_path)
        return tf_state

    def destroy(self, db_params: dict, document_class: Type[BaseDocument], doc_id: str, display_content) -> str:
        """Destroy the defined iad

        Args:
            db_params:
            document_class:
            doc_id:
            display_content:

        Returns:
            job status
        """
        if not doc_id:
            raise ValueError("Document id is needed for destroy resource")
        tf_state_field = self.tf_state_field
        tfstate_path = self.prepare_state(document_class, doc_id)
        db_params["tfstate_path"] = tfstate_path
        runtime_tf_path = self.prepare_runtime(db_params, document_class, doc_id, display_content)
        init_result = subprocess.run(['terraform', f"-chdir={runtime_tf_path}", 'init', "-no-color"],
                                     check=False, capture_output=True, text=True)
        if init_result.returncode != 0:
            logging.error(f"{document_class.__name__}/{doc_id} tf-init failed: {init_result.stderr}")
            return self._set_status(runtime_tf_path, "init_failed", tf_state_field)
        self.lock_wait(document_class, doc_id)
        destroy_result = subprocess.run(['terraform', f"-chdir={runtime_tf_path}",
                                         'destroy', "-auto-approve", "-no-color"],
                                        check=False, capture_output=True, text=True)
        if destroy_result.returncode != 0:
            logging.error(f"{document_class.__name__}/{doc_id} tf-destroy failed: {destroy_result.stderr}")
            return self._set_status(runtime_tf_path, "destroy_failed", tf_state_field)
        self.clean_runtime(document_class, doc_id)
        self.clean_state(document_class, doc_id)
        return "destroyed"

    def output(self, document_class: Type[BaseDocument], doc_id: str) -> dict:
        """Get output data (display form without external data)

        Args:
            document_class: Document type
            doc_id: Document id
        """
        resource_type = document_class.__name__
        runtime_path = self.runtime_path + "/" + resource_type + "/" + doc_id
        os.makedirs(runtime_path, exist_ok=True)
        output_result = subprocess.run(['terraform', f"-chdir={runtime_path}", 'output',
                                        f"-state={self.state_path}/stored.tfstate", '-json'],
                                       check=False, capture_output=True, text=True)
        if output_result.returncode != 0:
            logging.error(f"{document_class.__name__}/{doc_id} tf-output failed: {output_result.stderr}")
            return {}  # In the case of error, nothing to return
        return self.parse_output(output_result.stdout)


class TerraformEngine(Engine):
    """XIA Document Engine based on Terraform

    Notes:
        The status of the data should be the status of terraform engine status
    """
    engine_param = "terraform"
    engine_connector_class = TerraformConnectParam
    engine_connector = TerraformClient

    @classmethod
    def show_tf_example(cls, document_class: Type[BaseDocument]):
        data_sample = document_class.get_sample()
        json_data = data_sample.get_display_data(show_hidden=True)
        print("variable.tf example")
        variable_template = TerraformConfigFactory.generate_variables(json_data)
        print(variable_template)
        print("output.tf example")
        print(TerraformConfigFactory.generate_outputs(json_data))
        print("variable.tf after sample rendering")
        variable_template = "\n".join([ln for ln in variable_template.splitlines()
                                      if ln.strip() != "default = null  #xia#"])
        variable_template = variable_template.replace("#xia# ", "")
        variable_result = Template(variable_template, lstrip_blocks=True, trim_blocks=True).render(json_data)
        print(variable_result)

    @classmethod
    def create(cls, document_class: Type[BaseDocument], db_content: dict, doc_id: str = None):
        """Reflect the data to infrastructure

        Args:
            document_class: Document class
            db_content: database content
            doc_id: provided document id

        """
        db_con = cls.get_connection(document_class)
        if doc_id is None:
            sample_doc = document_class.from_db(**db_content)
            doc_id = sample_doc.get_id()
        display_content = cls.db_to_display(document_class, db_content, lazy=False, show_hidden=True)
        tf_state = db_con.apply(db_con.get_db_params(), document_class, doc_id, display_content)
        return doc_id

    @classmethod
    def get(cls, document_class: Type[BaseDocument], doc_id: str):
        db_con = cls.get_connection(document_class)
        display_data = db_con.output(document_class, doc_id)
        if display_data:
            doc_dict = document_class.from_display(**display_data).get_raw_data()
            doc_dict["_id"] = doc_id
            return doc_dict
        return {}

    @classmethod
    def set(cls, document_class: Type[BaseDocument], doc_id: str, db_content: dict):
        db_con = cls.get_connection(document_class)
        display_content = cls.db_to_display(document_class, db_content, lazy=False, show_hidden=True)
        tf_state = db_con.apply(db_con.get_db_params(), document_class, doc_id, display_content)
        return doc_id

    @classmethod
    def update(cls, _document_class: Type[BaseDocument], _doc_id: str, **kwargs):
        db_con = cls.get_connection(_document_class)
        new_data = cls.get(_document_class, _doc_id)
        if not new_data:
            raise ValueError(f"Document id {_doc_id} not found in the resource {_document_class.__name__}")
        for key, value in kwargs.items():
            field, operator = cls.parse_update_option(key)
            if operator is None:
                new_data[field] = value
        document = _document_class(**new_data)
        display_content = document.get_display_data(lazy=False, show_hidden=True)
        tf_state = db_con.apply(db_con.get_db_params(), _document_class, _doc_id, display_content)
        return cls.get(_document_class, _doc_id)

    @classmethod
    def fetch(cls, document_class: Type[BaseDocument], *args):
        db_con = cls.get_connection(document_class)
        for doc_id in args:
            display_data = db_con.output(document_class, doc_id)
            if display_data:
                doc_dict = document_class.from_display(**display_data).get_raw_data()
                doc_dict["_id"] = doc_id
                yield doc_id, doc_dict

    @classmethod
    def delete(cls, document_class: Type[BaseDocument], doc_id: str):
        db_con = cls.get_connection(document_class)
        old_data = cls.get(document_class, doc_id)
        if not old_data:
            return
        document = document_class(**old_data)
        display_content = document.get_display_data(lazy=False, show_hidden=True)
        tf_state = db_con.destroy(db_con.get_db_params(), document_class, doc_id, display_content)


class TerraformLocalConnectParam(TerraformConnectParam):
    """"""


class TerraformLocalClient(TerraformClient):
    backend_tf = """terraform {
  backend "local" {
    path = "{{ tfstate_path }}"
  }
}"""

    def prepare_state(self, document_class: Type[BaseDocument], doc_id: str):
        """Prepare the location to store state

        Args:
            document_class: Document class
            doc_id: document ID

        Returns:
            state_path for the current document
        """
        state_path = self.state_path
        os.makedirs(state_path, exist_ok=True)
        return f"{state_path}/stored.tfstate"
        # return f"../../state/{resource_type}/{doc_id}/stored.tfstate"

    def clean_state(self, document_class: Type[BaseDocument], doc_id: str):
        """Clean the state file

        Args:
            document_class: Document class related resource type
            doc_id: document ID
        """
        resource_type = document_class.__name__
        state_path = os.path.join(self.runtime_path, resource_type, doc_id, self.state_path.lstrip("./"))
        for root, dirs, files in os.walk(state_path):
            for file in files:
                if '.tfstate' in file:
                    os.remove(os.path.join(root, file))

    def get_state_path(self, document_class: Type[BaseDocument], doc_id: str):
        resource_type = document_class.__name__
        return f"{self.state_path}/{resource_type}/{doc_id}/stored.tfstate"


class TerraformLocalEngine(TerraformEngine):
    """Save the state file locally. Should only be used for the development purpose"""
    engine_connector_class = TerraformLocalConnectParam
    engine_connector = TerraformLocalClient


# Afterward will be some predefined Parameters
# Scaleway
class ScwTerraformLocalConnectParam(TerraformLocalConnectParam):
    organization_id: str = StringField(description="Organization ID", required=True)
    project_id: str = StringField(description="Project ID")
    access_key: str = OsEnvironField(description="Project Access Key", prefix="SCW_", required=True)
    secret_key: str = OsEnvironField(description="Project Secret Key", prefix="SCW_", required=True)


class ScwTerraformLocalEngine(TerraformLocalEngine):
    engine_connector_class = ScwTerraformLocalConnectParam


class TerraformConfigFactory:
    @classmethod
    def variable_get_bool(cls, key_name: str, value=None):
        bool_template = """variable "{key}" {
      type = optional(bool)
      default = null  #xia#
      #xia# default = {% if {key} is none or {key} is not defined %}null{% elif {key} %}true{% else %}false{% endif %}

    }
    """
        return bool_template.replace("{key}", key_name)

    @classmethod
    def variable_get_string(cls, key_name: str, value=None):
        string_template = """variable "{key}" {
  type = optional(string)
  default = null  #xia#
  #xia# default = {% if {key} is defined and {key} is not none %}"{{ {key} }}"{% else %}null{% endif %}

}
"""
        return string_template.replace("{key}", key_name)

    @classmethod
    def variable_get_number(cls, key_name: str, value=None):
        number_template = """variable "{key}" {
  type = optional(number)
  default = null  #xia#
  #xia# default = {% if {key} is defined and {key} is not none %}{{ {key} }}{% else %}null{% endif %}

}
"""
        return number_template.replace("{key}", key_name)

    @classmethod
    def variable_get_object(cls, key_name: str, value):
        type_template_str = """{% for k, v in {key}.items() %}
      {% if v is boolean %}
      {{ k }} = optional(bool)
      {% elif v is string %}
      {{ k }} = optional(string)
      {% elif v is number %}
      {{ k }} = optional(number)
      {% endif %}
    {% endfor %}
"""
        if isinstance(value, dict):
            type_template_str = type_template_str.replace("{key}", "value")
            type_template = Template(type_template_str, lstrip_blocks=True, trim_blocks=True)
            type_section = type_template.render(value=value)
            type_section = "\n".join(line for line in type_section.splitlines() if line)
        else:
            type_section = type_template_str
        object_template = """variable "{key}" {
  type = object({
{type}
  })
  default = null  #xia#
#xia#   default = {
#xia#     {% for k, v in {key}.items() %}
#xia#       {% if v is boolean %}
#xia#       {{ k }} = {% if v is none %}null{% elif v %}true{% else %}false{% endif %}

#xia#       {% elif v is string %}
#xia#       {{ k }} = {% if v is not none %}"{{ v }}"{% else %}null{% endif %}

#xia#       {% elif v is number %}
#xia#       {{ k }} = {% if v is not none %}{{ v }}{% else %}null{% endif %}

#xia#       {% endif %}
#xia#     {% endfor %}
#xia#   }
}
"""
        return object_template.replace("{key}", key_name).replace("{type}", type_section)

    @classmethod
    def variable_get_list_boolean(cls, key_name: str, value=None):
        list_template = """variable "{key}" {
    type = list(bool)
    default = null  #xia#
    #xia# default = [{% for v in {key} %}{% if loop.index > 1 %}, {% endif %}{% if v is none %}null{% elif v %}true{% else %}false{% endif %}{% endfor %}]
}
"""
        return list_template.replace("{key}", key_name)

    @classmethod
    def variable_get_list_string(cls, key_name: str, value=None):
        list_template = """variable "{key}" {
    type = list(string)
    default = null  #xia#
    #xia# default = [{% for v in {key} %}{% if loop.index > 1 %}, {% endif %}{% if v is not none %}"{{ v }}"{% else %}null{% endif %}{% endfor %}]
}
"""
        return list_template.replace("{key}", key_name)

    @classmethod
    def variable_get_list_number(cls, key_name: str, value=None):
        list_template = """variable "{key}" {
    type = list(number)
    default = null  #xia#
    #xia# default = [{% for v in {key} %}{% if loop.index > 1 %}, {% endif %}{% if v is not none %}{{ v }}{% else %}null{% endif %}{% endfor %}]
}
"""
        return list_template.replace("{key}", key_name)

    @classmethod
    def variable_get_list_object(cls, key_name: str, value):
        type_template_str = """{% for k, v in {key}.items() %}
      {% if v is boolean %}
      {{ k }} = optional(bool)
      {% elif v is string %}
      {{ k }} = optional(string)
      {% elif v is number %}
      {{ k }} = optional(number)
      {% endif %}
      {% endfor %}
"""
        if isinstance(value, list) and value:
            type_template_str = type_template_str.replace("{key}", "value")
            type_template = Template(type_template_str, lstrip_blocks=True, trim_blocks=True)
            type_section = type_template.render(value=value[0])
            type_section = "\n".join(line for line in type_section.splitlines() if line)
        else:
            type_section = type_template_str
        list_template = """variable "{key}" {
    type = list(object({
{type}
    }))
    default = null  #xia#
#xia#     default = [{% for v in {key} %}
#xia#             {% if loop.index > 1 %},{% endif %}{
#xia#             {% for w, x in v.items() %}
#xia#                 {% if x is boolean %}
#xia#         {{ w }} = {% if x is none %}null{% elif x %}true{% else %}false{% endif %}

#xia#                 {% elif x is string %}
#xia#         {{ w }} = {% if x is not none %}"{{ x }}"{% else %}null{% endif %}

#xia#                 {% elif x is number %}
#xia#         {{ w }} = {% if x is not none %}{{ x }}{% else %}null{% endif %}

#xia#                 {% endif %}
#xia#             {% endfor %}
#xia#     }{% endfor %}]
}
"""
        return list_template.replace("{key}", key_name).replace("{type}", type_section)

    @classmethod
    def output_get_default(cls, key_name: str, value=None):
        output_template = """output "{key}" {
  value = var.{key}
}
"""
        return output_template.replace("{key}", key_name)

    @classmethod
    def generate_variables(cls, dict_data: dict):
        variables = []
        for key, value in dict_data.items():
            if isinstance(value, bool):
                variables.append(cls.variable_get_bool(key, value))
            elif isinstance(value, str):
                variables.append(cls.variable_get_string(key, value))
            elif isinstance(value, (int, float)):
                variables.append(cls.variable_get_number(key, value))
            elif isinstance(value, dict):
                variables.append(cls.variable_get_object(key, value))
            elif isinstance(value, list):
                if value:
                    item = value[0]
                    if isinstance(item, bool):
                        variables.append(cls.variable_get_list_boolean(key, value))
                    elif isinstance(item, str):
                        variables.append(cls.variable_get_list_string(key, value))
                    elif isinstance(item, (int, float)):
                        variables.append(cls.variable_get_list_number(key, value))
                    elif isinstance(item, dict):
                        variables.append(cls.variable_get_list_object(key, value))
        return "\n".join([variable for variable in variables])

    @classmethod
    def generate_outputs(cls, dict_data: dict):
        return "\n".join([cls.output_get_default(key, value) for key, value in dict_data.items()])

