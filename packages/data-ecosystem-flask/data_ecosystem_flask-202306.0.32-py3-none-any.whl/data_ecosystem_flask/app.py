"""
Flask App exposing JIRA and Alation services via Swagger.

Summary:
    This Flask app provides endpoints to interact with
    JIRA and Alation services through a Swagger UI.

Returns:
    None
"""

from flask import Flask, send_file, request, render_template, Blueprint, g
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter
from pathlib import Path
from datetime import datetime
from io import BytesIO
from pandas import ExcelWriter
from requests.exceptions import HTTPError
from openpyxl.utils.exceptions import InvalidFileException
from flask_restx import Api, Resource, fields, Namespace, reqparse
from json import JSONDecodeError
from bs4 import BeautifulSoup
from app_startup import create_api, create_app
import rsconnect
from datetime import datetime
from werkzeug.datastructures import FileStorage
import re

# Ensure .bashrc where zfi4 is your username
# export PYTHONPATH=/home/zfi4/data-ecosystem-services/pade_python:$PYTHONPATH
from data_ecosystem_services.alation_service import (
    schema as pade_schema,
    datasource as pade_datasource,
    tokenendpoint as pade_tokenendpoint,
    manifest as pade_manifest
)
from data_ecosystem_services.cdc_tech_environment_service import (
    environment_file as pade_env_file
)
from data_ecosystem_services.az_key_vault_service import (
    az_key_vault as pade_az_key_vault
)
from data_ecosystem_services.cdc_self_service import (
    environment_metadata as pade_env_metadata
)
from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)
from data_ecosystem_services.cdc_security_service import (
    security_core as pade_security_core,
)

from data_ecosystem_services.posit_service import (
    posit_connect as pade_posit_connect
)

import requests
import openpyxl
import pandas as pd
import csv
import json
import sys
import os
import logging
import io
import importlib
import base64
import dotenv


TIMEOUT_5_SEC = 5
TIMEOUT_ONE_MIN = 60

CURRENT_USER_NAME = "zfi4"
API_PATH = "/data-ecosystem-services/pade_python"

sys.path.append(os.getcwd())
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(app_dir)

# app.config["PYTHONPATH"] = "../../../pade_python/"


app = create_app()


@app.before_request
def before_request():
    g.base_url = request.url_root
    g.log_url = g.base_url + "/logs/get_log_file_tail/1000"


upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

# Define the blueprint
cdc_admin_bp = Blueprint('logs', __name__,
                         url_prefix='/logs')


app.register_blueprint(cdc_admin_bp)


def get_posit_api_key():

    with tracer.start_as_current_span(f"/get_posit_api_key"):

        config = app.cdc_config

        posit_connect_base_url = config.get("posit_connect_base_url")

        logger.info(f"posit_connect_base_url:{posit_connect_base_url}")
        az_kv_az_sub_client_secret_key = config.get(
            "az_kv_az_sub_client_secret_key")
        az_kv_az_sub_client_secret_key = az_kv_az_sub_client_secret_key.replace(
            "-", "_")
        client_secret = os.getenv(az_kv_az_sub_client_secret_key)
        tenant_id = config.get("tenant_id")
        client_id = config.get("client_id")
        az_kv_key_vault_name = config.get("az_kv_key_vault_name")
        running_interactive = False
        if not client_secret:
            running_interactive = True

        az_key_vault = pade_az_key_vault.AzKeyVault(
            tenant_id, client_id, client_secret, az_kv_key_vault_name, running_interactive)

        az_kv_posit_connect_secret_key = config.get(
            "az_kv_posit_connect_secret_key")

        az_kv_posit_connect_secret = az_key_vault.get_secret(
            az_kv_posit_connect_secret_key)

        return az_kv_posit_connect_secret


def get_api_access_token(config):
    """Retrieves the API access token from a configuration dictionary.

    The function fetches various configuration values from the input dictionary,
    including Azure subscription details and Key Vault secrets, to create an Azure
    Key Vault client and fetch the Alation refresh token. The API access token is then
    generated using the TokenEndpoint and the relevant Alation details.

    Args:
        config (dict): A dictionary containing necessary configuration values,
        such as Azure subscription details, Key Vault name, Key Vault secret keys,
        and Alation base URL.

    Returns:
        str: The API access token.
    """

    with tracer.start_as_current_span(f"get_api_access_token"):

        az_sub_tenant_id = config.get("az_sub_tenant_id")
        az_sub_client_id = config.get("az_sub_client_id")
        az_kv_key_vault_name = config.get("az_kv_key_vault_name")
        az_kv_az_sub_client_secret_key = config.get(
            "az_kv_az_sub_client_secret_key")
        az_kv_az_sub_client_secret_key = az_kv_az_sub_client_secret_key.replace(
            "-", "_")
        client_secret = os.getenv(az_kv_az_sub_client_secret_key)
        print(
            f"az_kv_az_sub_client_secret_key:{az_kv_az_sub_client_secret_key}")
        print(f"az_sub_client_id:{az_sub_client_id}")
        # Initialize running_interactive as False
        running_interactive = False

        # Trim leading and trailing whitespace from client_secret
        client_secret = client_secret.strip()

        # Check if the client_secret is None or a zero-length string
        if not client_secret:
            running_interactive = True

        az_key_vault = pade_az_key_vault.AzKeyVault(
            az_sub_tenant_id, az_sub_client_id, client_secret, az_kv_key_vault_name, running_interactive)
        az_kv_edc_refresh_secret_key = config.get(
            "az_kv_edc_refresh_secret_key")
        alation_refresh_token = az_key_vault.get_secret(
            az_kv_edc_refresh_secret_key)
        edc_alation_base_url = config.get("edc_alation_base_url")
        token_endpoint = pade_tokenendpoint.TokenEndpoint(edc_alation_base_url)
        alation_user_id = config.get("edc_alation_user_id")
        api_access_token = token_endpoint.get_api_access_token(
            edc_alation_base_url, alation_user_id, alation_refresh_token)
        logger.info(f"api_access_token:{api_access_token}")
        return api_access_token


@cdc_admin_bp.route('/get_log_file_tail/<int:number_of_lines>')
def get_log_file_tail(number_of_lines):

    with tracer.start_as_current_span(f"get_log_file_tail"):

        try:
            log_data = logger_singleton.get_log_file_tail(number_of_lines)
        except AttributeError:
            return "Error: Logger not correctly configured", 500

        log_entries = [line.replace('\\', ':').split(None, 3)
                       for line in log_data.strip().split('\n')]

        for entry in log_entries:

            try:
                time_string = entry[1].split(":data_ecosystem_services:", 1)[0]
                if time_string.count(':') >= 2:
                    datetime_object = datetime.strptime(
                        f"{entry[0]} {time_string}", "%Y-%m-%d %H:%M:%S")
                    entry[0] = datetime_object.strftime("%Y-%m-%d %I:%M:%S %p")
                else:
                    raise ValueError("Invalid date and time format")
            except ValueError:
                return f"Error: Unable to parse date and time from {entry[0]} {time_string}", 500
            except IndexError:
                return f"Error: Unable to split string {entry[1]}", 500

            try:
                module, line_number = entry[1].split(
                    ":data_ecosystem_services:", 1)[1].split(':', 1)
                entry[1] = module
                entry.insert(2, line_number)
            except ValueError:
                return f"Error: Unable to split string {entry[1]}", 500

        return render_template('log_file.html', entries=log_entries)


@app.route('/')
def home():
    API_DESCRIPTION = (
        "The Program Agnostic Data Ecosystem (PADE) provides shared resources, "
        "practices and guardrails for analysts to discover, access, link, and use "
        "agency data in a consistent way. PADE improvements in standardized and "
        "streamlined workflows reduce the effort required to find, access, and "
        f"trust data. Logs can be found at [this link]({request.url_root}/logs/get_log_file_tail/1000)."
    )

    api, ns_welcome, ns_alation, ns_jira, ns_posit, ns_cdc_admin, ns_cdc_security = create_api(
        app, API_DESCRIPTION)

    ns_welcome.add_resource(WelcomeSwagger, '/')
    ns_welcome.add_resource(WelcomeSwagger, "/api/swagger")
    ns_jira.add_resource(Task, '/tasks/<string:project>')
    ns_alation.add_resource(MetadataExcelFileUploadRequest,
                            "/metadata_excel_file_upload_request/<int:schema_id>")
    ns_alation.add_resource(MetadataJsonFileUploadRequest,
                            "/metadata_json_file_upload_request/<int:schema_id>")
    ns_alation.add_resource(MetadataJsonFileDownload,
                            "/metadata_json_file_download/<int:schema_id>")
    ns_alation.add_resource(MetadataExcelFileDownload,
                            "/metadata_excel_file_download/<int:schema_id>")
    ns_alation.add_resource(MetadataExcelFileUpload,
                            "/metadata_excel_file_upload")

    ns_alation.add_resource(MetadataJsonFileUpload,
                            "/metadata_json_file_upload")

    ns_posit.add_resource(ConnectApiKeyVerification,
                          "/connect_api_key_verification")
    ns_posit.add_resource(PythonInformation, "/python_information")
    ns_posit.add_resource(GeneratedManifest, "/generate_manifest")
    ns_posit.add_resource(PublishManifest, "/publish_manifest")
    ns_posit.add_resource(ContentList, "/list_content")
    ns_posit.add_resource(
        DeploymentBundle, "/build_deployment_bundle/<string:content_id>/<string:bundle_id>")
    ns_posit.add_resource(DeploymentBundleList,
                          "/list_deployment_bundles/<string:content_id>")
    ns_posit.add_resource(TaskStatus, "/get_task_status/<string:task_id>")

    ns_cdc_security.add_resource(
        AzSubscriptionClientSecretVerification, "/verify_az_sub_client_secret")

    return {"message": "Welcome to our API"}


class WelcomeSwagger(Resource):
    def get(self):
        """
        Returns the Swagger API documentation.

        Returns:
            dict: The Swagger API documentation schema.
        """
        with tracer.start_as_current_span("/api/swagger"):
            return api.__schema__


class Task(Resource):
    """
    Represents the endpoint for retrieving tasks related to a specific project.

    This class is used as a Flask-RESTful resource to handle requests related
    to retrieving tasks for a specific JIRA project.

    Args:
        Resource (type): The base class for implementing Flask-RESTful
        resources.

    Attributes:
        project (str): The name or identifier of the project associated with
        the tasks.
    """

    def get(self, project=None):
        """
        Retrieves tasks associated with a specific project from JIRA.

        Args:
            project (str, optional): The name or identifier of the project. If
            not provided, retrieves tasks for all projects.

        Returns:
            dict: A dictionary containing the retrieved tasks.

        Note:
            This method communicates with JIRA to fetch the tasks.

        Example: DTEDS

        """

        with tracer.start_as_current_span(f"/tasks/{project}"):
            try:

                config = app.cdc_config

                jira_client_secret_key = config.get("jira_client_secret_key")
                az_kv_jira_env_var = jira_client_secret_key.replace("-", "_")
                jira_client_secret = os.getenv(az_kv_jira_env_var)
                logger.info(f"jira_client_secret:{jira_client_secret}")

                if project is None:
                    project = "DTEDS"  # Set your default project value here

                jira_base_url = config.get("jira_base_url")
                api_url = "/rest/api/latest/search"

                url = f"{jira_base_url}{api_url}"

                headers = {
                    "Authorization": f"Bearer {jira_client_secret}",
                    "Content-Type": "application/json"
                }
                logger.info(f"headers:{headers}")

                params = {
                    "jql": f"project = {project} AND issuetype = Task",
                    "fields": ["summary", "status", "assignee"],
                }

                logger.info(f"Retrieving tasks for project {project}")
                logger.info(f"url: {url}")
                logger.info(f"params: {params}")
                response_jira_tasks = requests.get(url,
                                                   headers=headers,
                                                   params=params,
                                                   timeout=TIMEOUT_5_SEC)
                response_jira_tasks_status_code = response_jira_tasks.status_code
                msg = "response_jira_tasks_status_code:"
                msg = msg + f"{response_jira_tasks_status_code}"
                logger.info(msg)
                content_t = response_jira_tasks.content.decode("utf-8")
                response_jira_tasks_content = content_t
                error_message = msg
                if response_jira_tasks_status_code in (200, 201):
                    msg = "response_jira_tasks_content:"
                    msg = msg + f"{response_jira_tasks_content}"
                    logger.info(msg)
                    try:
                        tasks = response_jira_tasks.json()["issues"]
                        logger.info(f"tasks: {tasks}")
                        # Process the retrieved tasks as needed
                        logger_singleton.force_flush()
                        return {"tasks": tasks}
                    except ValueError:
                        msg = f"Failed to retrieve json tasks from url: {url}."
                        msg = msg + f" parms:{params}"
                        msg = msg + "response_jira_tasks_content:"
                        msg = msg + f"{response_jira_tasks_content}"
                        logger.error(f"error_message: {msg}")
                        logger_singleton.force_flush()
                        return {"error": msg}
                else:
                    msg = f"Failed to retrieve tasks from url:{url}"
                    msg = msg + \
                        f": status_code: {response_jira_tasks.status_code}"
                    msg = msg + ": response_jira_tasks_content:"
                    msg = msg + f"{response_jira_tasks_content}"
                    if response_jira_tasks.status_code == 500:
                        try:
                            error_message = response_jira_tasks.json()[
                                "message"]
                        except ValueError:
                            error_message = "Failed to retrieve json from url:"
                            error_message = error_message + \
                                f"{url}: params: {params}."
                    msg = msg + ": error_message: " + error_message
                    logger.error(f"error_message: {msg}")
                    logger_singleton.force_flush()
                    return {"error": msg}
            except Exception as e:
                logger.error(f"An unexpected error occurred: {str(e)}")
                logger_singleton.force_flush()
                return {"error": f"An unexpected error occurred: {str(e)}"}


class MetadataExcelFileUploadRequest(Resource):
    """
    Represents the endpoint for uploading a metadata Excel file.

    This class is used as a Flask-RESTful resource to handle requests related
    to uploading a metadata Excel file.

    Args:
        Resource (type): The base class for implementing Flask-RESTful
        resources.

    Attributes:
        schema_id (int): The ID of the schema associated with the metadata
        Excel file.
    """

    def get(self, schema_id):
        """
        Retrieves the Excel metadata file from SharePoint and uploads it to
        Alation based on the schema_id.

        Args:
            schema_id (int): The ID of the schema associated with the metadata
            Excel file.

        Returns:
            dict: A dictionary containing the response data.

        Note:
            This method uploads the Excel metadata file from SharePoint to
            Alation.

        Example:
            Use schema_id 106788 to test OCIO_PADE_DEV (DataBricks).
        """

        with tracer.start_as_current_span(f"/metadata_excel_file_upload_request/schema_id"):

            return {
                "message": f"Tasks: GET method called for project: {schema_id}"
            }


class MetadataJsonFileUploadRequest(Resource):
    """
    Represents the endpoint for uploading a metadata JSON file.

    This class is used as a Flask resource to handle requests related to
    uploading a metadata JSON file.

    Args:
        Resource (type): The base class for implementing Flask resources.

    Attributes:
        schema_id (int): The ID of the schema associated with the metadata JSON
        file.
    """

    def get(self, schema_id):
        """
        Retrieves the JSON metadata file from SharePoint and uploads it to
        Alation based on the schema_id.

        Args:
            schema_id (int): The ID of the schema associated with the metadata
            JSON file.

        Returns:
            dict: A dictionary containing the response data.

        Example:
            Use schema_id 106788 to test OCIO_PADE_DEV (DataBricks).
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance()
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance()
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span(f"/metadata_json_file_upload_request/{schema_id}"):

            try:
                config = app.cdc_config
                edc_alation_base_url = config.get("edc_alation_base_url")
                logger.info(f"edc_alation_base_url:{edc_alation_base_url}")
                api_access_token = get_api_access_token(config)
                logger.info(f"api_access_token:{api_access_token}")

                headers = {"Token": api_access_token,
                           "accept": "application/json"}
                api_url = f"/integration/v1/datasource/{schema_id}/"
                datasource_url = edc_alation_base_url + api_url
                logger.info(f"datasource_url: {datasource_url}")
                logger.info(f"headers: {headers}")
                response_datasource = requests.get(datasource_url,
                                                   headers=headers,
                                                   timeout=TIMEOUT_ONE_MIN)
                response_datasource_text = "not_set"
                # Check the response status code to determine if successful
                if response_datasource.status_code in (200, 201):
                    # Extract the API token from the response
                    datasource = json.loads(response_datasource.text)
                    datasource_title = datasource.get("title")
                    logger.info(f"datasource: {str(datasource_title)}")
                else:
                    response_datasource_text = response_datasource.reason
                    logger.error(
                        f"Failed to get Datasource : {response_datasource_text}")
                    logger_singleton.force_flush()
                    return "Failed to get Datasource :" + str(response_datasource_text)

                msg = "Metadata_Json_File: Upload Processed for "
                msg = msg + f"schema_id: {schema_id}"
                logger.info(msg)
                logger_singleton.force_flush()

                return {
                    "message": msg
                }

            except Exception as e:
                logger.error(f"An unexpected error occurred: {str(e)}")
                logger_singleton.force_flush()
                return {"error": f"An unexpected error occurred: {str(e)}"}


class MetadataJsonFileDownload(Resource):
    """
    A Flask-RESTful resource responsible for downloading metadata JSON files.

    This class handles HTTP requests to the corresponding endpoint. It likely
    implements methods such as GET to handle the downloading of a metadata
    JSON file. Each method corresponds to a standard HTTP method
    (e.g., GET, POST, PUT, DELETE) and carries out a specific operation.

    Args:
        Resource (Resource): A base class from Flask-RESTful for creating new
        RESTful resources.
    """

    def get(self, schema_id):
        """
        Retrieves the JSON metadata file from Alation based on the schema_id.

        Args:
            schema_id (int): The ID of the schema associated with the metadata
            JSON file.

        Returns:
            dict: A dictionary containing the downloaded JSON metadata file.

        Example:
            Use schema_id 106788 to test OCIO_PADE_DEV (DataBricks).
        """

        with tracer.start_as_current_span(f"/metadata_json_file_download/{schema_id}"):
            try:
                config = app.cdc_config
                edc_alation_base_url = config.get("edc_alation_base_url")
                api_access_token = get_api_access_token(config)

                if len(api_access_token.strip()) == 0:
                    msg = "Alation API Access Token is not set"
                    logger.error(msg)
                    return {"error": f"An unexpected error occurred: {msg}"}

                logger.info("###### GET SCHEMA #######")
                headers = {
                    "Token": api_access_token,
                    "Content-Type": "application/json",
                }
                api_url = f"/integration/v1/schema/{schema_id}/"
                schema_url = edc_alation_base_url + api_url
                schema = pade_schema.Schema()
                logger.info(f"schema_url: {schema_url}")
                logger.info(f"headers: {headers}")
                schema_results = schema.get_schema(
                    headers, edc_alation_base_url, schema_id
                )
                logger.info(f"schema_results: {str(schema_results)}")
                response_schema_text = "not_set"
                datasource_id = -1
                # Check the response status code to determine if successful
                if "title" in schema_results:
                    # Extract the API token from the response
                    schema_name = schema_results.get("name")
                    datasource_id = schema_results.get("ds_id")
                else:
                    response_schema_text = schema_results.get("reason")
                    error_msg = "Failed to get schema:" + \
                        str(response_schema_text)
                    error_msg = error_msg + " for schema_id: " + str(schema_id)
                    error_msg = error_msg + \
                        " and schema_name: " + str(schema_name)
                    error_msg = error_msg + \
                        " and datasource_id: " + str(datasource_id)
                    error_msg = error_msg + \
                        " and schema_results: " + str(schema_results)
                    logger.error(error_msg)
                    return {"error": error_msg}

                logger.info("###### GET DATASOURCE #######")
                api_url = f"/integration/v1/datasource/{datasource_id}/"
                datasource_url = edc_alation_base_url + api_url
                logger.info(f"datasource_url: {datasource_url}")
                logger.info(f"headers: {headers}")
                response_datasource = requests.get(datasource_url,
                                                   headers=headers,
                                                   timeout=TIMEOUT_ONE_MIN)
                response_datasource_text = "not_set"
                # Check the response status code to determine if successful
                if response_datasource.status_code in (200, 201):
                    # Extract the API token from the response
                    datasource = json.loads(response_datasource.text)
                    datasource_title = datasource.get("title")
                    logger.info(f"datasource: {str(datasource_title)}")
                else:
                    response_datasource_text = response_datasource.reason
                    return "Failed to get Datasource :" + str(response_datasource_text)

                schema_location = config.get("edc_schema_location")
                logger.info(
                    "Loading manifest schema from {0}".format(schema_location))
                manifest = pade_manifest.Manifest(schema_location)
                obj_file = pade_env_file.EnvironmentFile()
                app_dir = os.path.dirname(os.path.abspath(__file__))
                environment = config.get("environment")
                yyyy = config.get("yyyy")
                mm = config.get("mm")
                dd = config.get("dd")
                manifest_path = (
                    app_dir + "/" + environment + "_manifests/"
                )
                manifest_file = (
                    obj_file.scrub_file_name(datasource_title)
                    + "_"
                    + obj_file.scrub_file_name(schema_name)
                    + "_metadata_"
                    + yyyy
                    + "_"
                    + mm
                    + "_"
                    + dd
                    + ".json"
                )
                manifest_file = manifest_path + manifest_file
                logger.info(f"manifest_file: {manifest_file}")
                logger.info("###### CHECK DATASOURCE #######")
                datasource = pade_datasource.DataSource()
                datasource.check_datasource(
                    schema_name, datasource_id, headers, edc_alation_base_url
                )

                manifest_dict = schema.get_schema_structure(
                    schema_id, headers, edc_alation_base_url, manifest, datasource_id
                )

                # write the file
                jsonString = json.dumps(manifest_dict, indent=4)
                jsonFile = open(manifest_file, "w")
                jsonFile.write(jsonString)
                jsonFile.close()

                msg = "Wrote Manifest template file: " + manifest_file
                logger.info(msg)
                logger.info(
                    f"Validating the manifest file at {manifest_file} with schema"
                )
                metadata = manifest.validateManifest(manifest_file)
                logger.info("Metadata File Validated")
                logger_singleton.force_flush()

                # Return the file as a download
                return send_file(manifest_file, as_attachment=True)
            except Exception as e:
                logger.error(f"An unexpected error occurred: {str(e)}")
                logger_singleton.force_flush()
                return {"error": f"An unexpected error occurred: {str(e)}"}


class MetadataExcelFileDownload(Resource):
    """
    A Flask-RESTful resource responsible for handling requests for downloading
    metadata Excel files with a specific schema id.

    This class corresponds to the endpoint
    '/metadata_excel_file_download/<int:schema_id>'.
    It handles HTTP requests that include a specific schema id in the URL, and
    it likely implements methods like GET to manage the download of the
    associated metadata Excel file.

    Args:
        Resource (Resource): A base class from Flask-RESTful for creating
        new RESTful resources.
    """

    def get(self, schema_id):
        """
        Retrieves the Excel metadata file from Alation based on the schema_id.

        Args:
            schema_id (int): The ID of the schema associated with the metadata
            Excel file.

        Returns:
            dict: A dictionary containing the downloaded Excel metadata file.

        Example:
            Use schema_id 106788 to test OCIO_PADE_DEV (DataBricks).
        """

        with tracer.start_as_current_span(f"/metadata_excel_file_download/{schema_id}"):
            try:
                config = app.cdc_config
                api_access_token = get_api_access_token(config)
                headers = {"Token": api_access_token}
                headers_bearer = {
                    "Authorization": f"Bearer {api_access_token}"}

                logger.info("##### Get all queries #####")
                api_url = "/integration/v1/query/"
                edc_alation_base_url = config.get("edc_alation_base_url")
                query_list_url = edc_alation_base_url + api_url
                logger.info(f"query_list_url: {query_list_url}")
                response = requests.get(query_list_url,
                                        headers=headers,
                                        timeout=TIMEOUT_ONE_MIN)
                queries = json.loads(response.text)
                for query in queries:
                    id = str(query["id"])
                    logger.info(
                        f"##### Get details for a single query {id} #####")
                    query_detail_url = edc_alation_base_url + api_url + id
                    response_detail = requests.get(query_detail_url,
                                                   headers=headers,
                                                   timeout=TIMEOUT_ONE_MIN)
                    query_detail = json.loads(response_detail.text)
                    detail = query_detail.get("detail")
                    logger.info(f"query_detail: {query_detail}")
                    if detail == "You do not have permission to perform this action.":
                        query_title = "No Permission"
                        logger.info(f"id: {id}, title: {query_title}")
                    else:
                        query_id = query_detail["id"]
                        logger.info(f"id: {id}, title: {query_title}")

                logger.info("##### Get all execution sessions #####")
                api_url = "/integration/v1/query/execution_session/"
                session_list_url = edc_alation_base_url + api_url
                response = requests.get(session_list_url,
                                        headers=headers,
                                        timeout=TIMEOUT_ONE_MIN)
                sessions = json.loads(response.text)
                for session in sessions:
                    session_id = session["id"]
                    client_session_id = session["client_session_id"]
                    msg = f"ID: {session_id}, Client-session-ID: {client_session_id}"
                    logger.info(msg)

                query_id = "249"

                # Get query text
                api_url = f"/integration/v1/query/{query_id}/sql/"
                query_text_url = edc_alation_base_url + api_url
                logger.info(f"query_text_url:{query_text_url}")
                response_query_text = requests.get(
                    query_text_url, headers=headers_bearer, timeout=TIMEOUT_ONE_MIN
                )
                response_content_text = "not_set"
                # Check the response status code to determine if the request was
                # successful
                if response_query_text.status_code in (200, 201):
                    # Extract the API token from the response
                    response_content_text = response_query_text.content.decode(
                        "utf-8")
                    # logger.info(f"SQL Query Text response: {query_text}")
                else:
                    logger.info(
                        "Failed to get SQL Query Text :" +
                        str(response_content_text)
                    )

                query_text = response_content_text
                query_text = query_text.replace("\n", " ").replace("'", "'")

                # Get latest result id
                api_url = f"/integration/v1/query/{query_id}/result/latest/"
                query_url = edc_alation_base_url + api_url
                logger.info(f"query_url: {query_url}")
                logger.info(f"headers: {headers}")
                # Send the request to the Alation API endpoint.
                # The endpoint for executing queries is `/integration/v1/query`.
                response_query = requests.get(query_url,
                                              headers=headers,
                                              timeout=TIMEOUT_ONE_MIN)
                logger.info(
                    "response_query.content:" +
                    response_query.content.decode("utf-8")
                )

                # execution_result_id = json_response['id']
                execution_result_id = "570"

                # Get lastest results and place in dataframe
                api_url = f"/integration/v1/result/{execution_result_id}/csv/"
                result_url = edc_alation_base_url + api_url

                # download and parse response as csv
                with requests.Session() as s:
                    response_results = requests.get(
                        result_url, headers=headers, timeout=TIMEOUT_ONE_MIN
                    )
                    decoded_content = response_results.content.decode("utf-8")
                    logger.info("response_results.content:" + decoded_content)
                    csv_reader = csv.reader(
                        decoded_content.splitlines(), delimiter=","
                    )
                    logger.info.logger.info(list(csv_reader))

                # Create a new Pandas DataFrame
                df1 = pd.DataFrame(
                    {"Name": ["John Doe", "Jane Doe"], "Age": [30, 25]})
                df2 = pd.DataFrame(
                    {"Name": ["Jack Doe", "Jill Doe"], "Age": [30, 25]})

                # Create a new openpyxl Workbook object
                wb = openpyxl.Workbook()

                # Create a new openpyxl Worksheet object
                ws = wb.active
                excel_data = io.BytesIO()
                with ExcelWriter(excel_data, engine="xlsxwriter") as writer:
                    # Write the Pandas DataFrames to the Worksheet objects
                    df1.to_excel(
                        writer, sheet_name="My DataFrame 1", index=False)
                    df2.to_excel(
                        writer, sheet_name="My DataFrame 2", index=False)

                # Retrieve the Excel file from the BytesIO object
                excel_data.seek(0)

                mt = "application/vnd.openxmlformats"
                mt = mt + "-officedocument.spreadsheetml.sheet"
                response = send_file(
                    excel_data,
                    as_attachment=True,
                    download_name="my_excel_spreadsheet.xlsx",
                    mimetype=mt,
                )
                return response

            except Exception as e:
                logger.error(f"An unexpected error occurred: {str(e)}")
                logger_singleton.force_flush()
                return {"error": f"An unexpected error occurred: {str(e)}"}


class MetadataExcelFileUpload(Resource):
    """
    A Flask-RESTful resource for handling the upload of metadata Excel files.

    This class corresponds to the endpoint '/metadata_excel_file_upload'.
    It handles HTTP requests for uploading metadata Excel files.
    Each method in this class corresponds to a specific HTTP
    method (e.g., POST) and carries out the upload operation.

    Args:
        Resource (Resource): A base class from Flask-RESTful for creating new
        RESTful resources.

    Returns:
        Response: The response of the HTTP request after processing the
        uploaded file. The specific content and status code of the response
        will depend on the implementation.
    """

    def post(self):
        """
        Uploads the Excel metadata file to Alation via direct upload based on
        the schema_id.

        Args:
            schema_id (int): The ID of the schema associated with the metadata
            Excel file.

        Returns:
            dict: A dictionary containing the response data.

        Example:
            Use schema_id 106788 to test OCIO_PADE_DEV (DataBricks).
        """

        args = upload_parser.parse_args()

        file = args["file"]
        logger.info(f"file: {file}")
        msg = "Metadata_Json_File_Upload: POST method called successfully."
        return {
            "message": msg
        }


class MetadataJsonFileUpload(Resource):
    """
    A Flask-RESTful resource for handling the upload of metadata JSON files.

    This class corresponds to the endpoint '/metadata_json_file_upload'. It
    handles HTTP requests for uploading metadata JSON files.
    Each method in this class corresponds to a specific HTTP
    method (e.g., POST) and carries out the upload operation.

    Args:
        Resource (Resource): A base class from Flask-RESTful for creating new
        RESTful resources.

    Returns:
        Response: The response of the HTTP request after processing the
        uploaded file.
        The specific content and status code of the response will depend on
        the implementation.
    """

    def post(self):
        """Uploads JSON metadata file via direct upload to Alation
        based on schema_id.
        Use 106788 to test OCIO_PADE_DEV (DataBricks)"""
        args = upload_parser.parse_args()

        with tracer.start_as_current_span(f"/metadata_json_file_upload"):

            # Get the uploaded file
            file = args["file"]

            # Read the contents of the file as JSON
            file_contents = file.read()
            json_data = json.loads(file_contents)

            # Extract the alationSchemaID
            schema_id = json_data["alationSchemaID"]

            config = app.cdc_config
            api_access_token = get_api_access_token(config)
            edc_alation_base_url = config.get("edc_alation_base_url")

            logger.info("###### GET SCHEMA #######")
            headers = {
                "Token": api_access_token,
                "Content-Type": "application/json",
            }
            api_url = f"/integration/v1/schema/{schema_id}/"
            schema_url = edc_alation_base_url + api_url
            schema = pade_schema.Schema()

            logger.info(f"schema_url: {schema_url}")
            logger.info(f"headers: {headers}")
            schema_results = schema.get_schema(
                headers, edc_alation_base_url, schema_id
            )

            datasource_id = -1
            # Check the response status code to determine if the request was
            # successful
            if "title" in schema_results:
                # Extract the API token from the response
                schema_name = schema_results.get("name")
                datasource_id = schema_results.get("ds_id")

                logger.info("###### GET DATASOURCE #######")
                api_url = f"/integration/v1/datasource/{datasource_id}/"
                datasource_url = edc_alation_base_url + api_url
                logger.info(f"datasource_url: {datasource_url}")
                logger.info(f"headers: {headers}")
                response_datasource = requests.get(datasource_url,
                                                   headers=headers,
                                                   timeout=TIMEOUT_ONE_MIN)
                response_datasource_text = "not_set"
                # Check the response status code to determine if the request was
                # successful
                if response_datasource.status_code in (200, 201):
                    # Extract the API token from the response
                    datasource = json.loads(response_datasource.text)
                    datasource_title = datasource.get("title")
                    logger.info(f"datasource: {str(datasource_title)}")
                else:
                    response_datasource_text = response_datasource.reason
                    return "Failed to get Datasource :" + str(
                        response_datasource_text
                    )

                schema_location = config.get("edc_schema_location")
                logger.info(
                    f"Loading manifest schema from {schema_location}")
                manifest = pade_manifest.Manifest(schema_location)
                obj_file = pade_env_file.EnvironmentFile()
                app_dir = os.path.dirname(os.path.abspath(__file__))
                environment = config.get("environment")
                yyyy = config.get("yyyy")
                mm = config.get("mm")
                dd = config.get("dd")
                manifest_path = (
                    app_dir + "/" + environment + "_manifests/"
                )
                manifest_file = (
                    obj_file.scrub_file_name(datasource_title)
                    + "_"
                    + obj_file.scrub_file_name(schema_name)
                    + "_metadata_"
                    + yyyy
                    + "_"
                    + mm
                    + "_"
                    + dd
                    + ".json"
                )
                manifest_file = manifest_path + manifest_file
                logger.info(f"manifest_file: {manifest_file}")
                logger.info(f"datasource_id: {datasource_id}")

                az_sub_tenant_id = config.get("az_sub_tenant_id")
                az_sub_client_id = config.get("az_sub_client_id")
                az_kv_key_vault_name = config.get("az_kv_key_vault_name")

                # Initialize running_interactive as False
                running_interactive = False

                # Trim leading and trailing whitespace from client_secret
                client_secret = client_secret.strip()

                # Check if the client_secret is None or a zero-length string
                if not client_secret:
                    running_interactive = True

                az_key_vault = pade_az_key_vault.AzKeyVault(
                    az_sub_tenant_id, az_sub_client_id, client_secret, az_kv_key_vault_name, running_interactive)
                az_kv_edc_refresh_secret_key = config.get(
                    "az_kv_edc_refresh_secret_key")
                alation_refresh_token = az_key_vault.get_secret(
                    az_kv_edc_refresh_secret_key)

                # Save the JSON data to a file
                with open(manifest_file, "w") as file:
                    json.dump(json_data, file)
                schema.upload_schema_manifest(
                    schema_id,
                    headers,
                    edc_alation_base_url,
                    manifest,
                    manifest_file,
                    datasource_id,
                    alation_refresh_token,
                    schema_name,
                    config,
                )
            else:
                response_schema_text = schema_results.get("reason")
                return "Failed to get schema :" + str(response_schema_text)


class AzSubscriptionClientSecretVerification(Resource):
    """
    A Flask-RESTful resource for handling the verification of API keys.

    """

    def get(self):
        """
        Verifies the key stored in key vault based on configuration setting: az_kv_az_sub_client_secret_key

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"/verify_az_sub_client_secret"):

            config = app.cdc_config
            az_kv_az_sub_client_secret_key = config.get(
                "az_kv_az_sub_client_secret_key")
            az_kv_az_sub_client_secret_key = az_kv_az_sub_client_secret_key.replace(
                "-", "_")
            client_secret = os.getenv(az_kv_az_sub_client_secret_key)
            tenant_id = config.get("tenant_id")
            client_id = config.get("client_id")

            security_core = pade_security_core.SecurityCore()
            status_code, response_content = security_core.verify_az_sub_client_secret(
                tenant_id, client_id, client_secret)

            # Handle the verification logic
            return {
                'status_code': status_code,
                'response_content': response_content
            }, 200


class ConnectApiKeyVerification(Resource):
    """
    A Flask-RESTful resource for handling the verification of API keys.

    """

    def get(self):
        """
        Verifies the key stored in key vault based on configuration setting: az_kv_posit_connect_secret_key

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"/connect_api_key_verification"):

            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")

            logger.info(f"posit_connect_base_url:{posit_connect_base_url}")
            connect_api_key = get_posit_api_key()
            posit_connect = pade_posit_connect.PositConnect()
            status_code, response_content, api_url = posit_connect.verify_api_key(
                connect_api_key, posit_connect_base_url)

            # Handle the verification logic
            return {
                'status_code': status_code,
                'posit_connect_base_url': posit_connect_base_url,
                'api_url': api_url,
                "connect_api_key": connect_api_key,
                'response_content': response_content
            }, 200


class DeploymentBundle(Resource):
    """
    A Flask-RESTful resource for handling POSIT Deployment Bundle.

    """

    def get(self, content_id, bundle_id):
        """
        Generates DeploymentBundle

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"/build_deployment_bundle"):

            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")

            logger.info(f"posit_connect_base_url:{posit_connect_base_url}")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key")
            connect_api_key = get_posit_api_key()
            posit_connect = pade_posit_connect.PositConnect()
            status_code, response_content, api_url = posit_connect.build_deployment_bundle(
                connect_api_key, posit_connect_base_url, content_id, bundle_id)

            # Handle the verification logic
            return {
                'posit_connect_base_url': posit_connect_base_url,
                'api_url': api_url,
                'response_content': response_content
            }, 200


class PythonInformation(Resource):
    """
    A Flask-RESTful resource for handling POSIT Python Information.

    """

    def get(self):
        """
        Generates python information about POSIT

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"/api_key_verification"):

            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")

            logger.info(f"posit_connect_base_url:{posit_connect_base_url}")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key")
            connect_api_key = get_posit_api_key()
            posit_connect = pade_posit_connect.PositConnect()
            status_code, response_content, api_url = posit_connect.get_python_information(
                connect_api_key, posit_connect_base_url)

            # Handle the verification logic
            return {
                'posit_connect_base_url': posit_connect_base_url,
                'api_url': api_url,
                "az_kv_posit_connect_secret_key": az_kv_posit_connect_secret_key,
                'response_content': response_content
            }, 200


class GeneratedManifest(Resource):
    """
    A Flask-RESTful resource for handling POSIT Manifest Generation

    """

    def get(self):
        """
        Generates manifest JSON

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"/generate_manifest"):

            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")

            # Get the full URL
            full_url = request.url
            # Split the URL by '/'
            url_parts = full_url.split('/')
            # Remove the last 2 parts (i.e., the file name or the route)
            url_parts = url_parts[:-2]
            # Join the parts back together
            url_without_filename = '/'.join(url_parts)
            base_url = url_without_filename
            environment = config.get("environment")
            obj_file = pade_env_file.EnvironmentFile()

            app_dir = os.path.dirname(os.path.abspath(__file__))

            manifest_path = (
                app_dir + "/" + environment + "_posit_manifests/"
            )

            swagger_path = (
                app_dir + "/" + environment + "_swagger_manifests/"
            )

            yyyy = str(datetime.now().year)
            dd = str(datetime.now().day).zfill(2)
            mm = str(datetime.now().month).zfill(2)

            json_extension = (
                "_"
                + yyyy
                + "_"
                + mm
                + "_"
                + dd
                + ".json"
            )
            manifest_file = manifest_path + "manifest" + json_extension
            # swagger_file = swagger_path + "swagger" + json_extension
            # use cached json file for now
            # having issues downloading
            swagger_file = swagger_path + "swagger_2023_06_22.json"
            connect_api_key = get_posit_api_key()
            requirements_file = app_dir + "/requirements.txt"

            # headers = {
            #     "Authorization": f"Bearer {connect_api_key}",
            # }
            swagger_url = f"{base_url}/swagger.json"
            # response = requests.get(swagger_url, headers=headers)

            # response_data = None
            # error_message = None
            # if response.status_code == 200:  # HTTP status code 200 means "OK"
            #     try:
            #         response_data =  response.json()
            #         response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
            #   except requests.HTTPError as http_err:
            #        error_message = f"HTTP error occurred: {http_err}"
            #        soup = BeautifulSoup(response.text, 'html.parser')
            #        error_message = (soup.prettify())
            #    except JSONDecodeError:
            #        error_message = "The response could not be decoded as JSON."
            #        soup = BeautifulSoup(response.text, 'html.parser')
            #        error_message = (soup.prettify())
            #    except Exception as err:
            #        error_message = f"An error occurred: {err}"
            #        error_message = "Response content:"+ response.content.decode()
            # else:
            #    error_message = f"Request failed with status code {response.status_code}"
            # if error_message is not None:
            #    return {
            #        'headers' : headers,
            #        'swagger_url' :  swagger_url,
            #        'manifest_json': "",
            #        'status_message': error_message
            #    }, 500
            # with open(swagger_file, 'w') as f:
            #    f.write(response_data)

            logger.info(f"swagger_file:{swagger_file}")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key")
            connect_api_key = get_posit_api_key()

            posit_connect = pade_posit_connect.PositConnect()

            manifest_json = posit_connect.generate_manifest(
                swagger_file, requirements_file)

            with open(manifest_file, 'w') as f:
                f.write(manifest_json)

            # Handle the verification logic
            return {
                'swagger_url': swagger_url,
                'manifest_json': manifest_json,
                'status_message': 'success'
            }, 200


class PublishManifest(Resource):
    """
    A Flask-RESTful resource for handling POSIT Manifest Publication

    """

    def get(self):
        """
        Publishes manifest JSON

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"/publish_manifest"):

            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")

            # Get the full URL
            full_url = request.url
            # Split the URL by '/'
            url_parts = full_url.split('/')
            # Remove the last 2 parts (i.e., the file name or the route)
            url_parts = url_parts[:-2]
            # Join the parts back together
            url_without_filename = '/'.join(url_parts)
            base_url = url_without_filename
            environment = config.get("environment")
            obj_file = pade_env_file.EnvironmentFile()

            app_dir = os.path.dirname(os.path.abspath(__file__))

            manifest_path = (
                app_dir + "/" + environment + "_posit_manifests/"
            )

            manifest_file = obj_file.get_latest_file(manifest_path)

            logger.info(f"manfiest_file:{manifest_file}")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key")
            connect_api_key = get_posit_api_key()

            posit_connect = pade_posit_connect.PositConnect()

            status_code, response_content, api_url = posit_connect.publish_manifest(
                connect_api_key, posit_connect_base_url, manifest_file)

            # Handle the verification logic
            return {
                'status_code': status_code,
                'response_content': response_content,
                'api_url': api_url
            }, 200


class ContentList(Resource):
    """
    A Flask-RESTful resource for handling POSIT Content Lists

    """

    def get(self):
        """
        Publishes manifest JSON

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"/list_conent"):

            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key")
            connect_api_key = get_posit_api_key()

            posit_connect = pade_posit_connect.PositConnect()

            status_code, response_content, api_url = posit_connect.list_content(
                connect_api_key, posit_connect_base_url)

            # Handle the verification logic
            return {
                'status_code': status_code,
                'response_content': response_content,
                'api_url': api_url
            }, 200


class DeploymentBundleList(Resource):
    """
    A Flask-RESTful resource for handling POSIT Bundle Lists

    """

    def get(self, content_id):
        """
        Publishes manifest JSON

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"/list_conent"):

            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key")
            connect_api_key = get_posit_api_key()

            posit_connect = pade_posit_connect.PositConnect()

            status_code, response_content, api_url = posit_connect.list_deployment_bundles(
                connect_api_key, posit_connect_base_url, content_id)

            # Handle the verification logic
            return {
                'status_code': status_code,
                'response_content': response_content,
                'api_url': api_url
            }, 200


class TaskStatus(Resource):
    """
    A Flask-RESTful resource for handling POSIT Bundle Lists

    """

    def get(self, task_id):
        """
        Gets Task Status

        Returns:
            tuple: A tuple containing the status code and response from the server.
            The response will be in JSON format if possible, otherwise it will be the raw text response.
        """

        with tracer.start_as_current_span(f"/get_task_status"):

            config = app.cdc_config

            posit_connect_base_url = config.get("posit_connect_base_url")
            az_kv_posit_connect_secret_key = config.get(
                "az_kv_posit_connect_secret_key")
            connect_api_key = get_posit_api_key()

            posit_connect = pade_posit_connect.PositConnect()

            status_code, response_content, api_url = posit_connect.get_task_details(
                connect_api_key, posit_connect_base_url, task_id)

            # Handle the verification logic
            return {
                'status_code': status_code,
                'response_content': response_content,
                'api_url': api_url
            }, 200


metric_exporter = AzureMonitorMetricExporter()

logger = app.logger
logger_singleton = pade_env_logging.LoggerSingleton.instance()
tracer = app.tracer

FlaskInstrumentor().instrument_app(app)
# When running in Posit Workbench, apply ProxyFix middleware
# See: https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
if "RS_SERVER_URL" in os.environ and os.environ["RS_SERVER_URL"]:
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)


if __name__ == "__main__":
    app.run(debug=True)
