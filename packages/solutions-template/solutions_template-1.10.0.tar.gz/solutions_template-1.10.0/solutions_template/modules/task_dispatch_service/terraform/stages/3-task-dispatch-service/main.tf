/**
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

# TODO: Add Terraform blocks below.

# Used to retrieve project_number later
data "google_project" "project" {
}

resource "google_pubsub_topic" "task_topic" {
  name                       = var.task_topic
  message_retention_duration = var.message_retention_duration
}

# Create a Pub/Sub trigger
resource "google_eventarc_trigger" "trigger_task_pubsub" {
  provider = google-beta
  name     = var.eventarc_trigger_name
  location = var.region

  matching_criteria {
    attribute = "type"
    value     = "google.cloud.pubsub.topic.v1.messagePublished"
  }
  destination {
    {% if eventarc_destination == "cloudrun" -%}
    cloud_run_service {
      service = var.eventarc_cloudrun_service
      region  = var.region
    }{%- endif %}

    {% if eventarc_destination == "gke" -%}
    gke {
      cluster   = var.eventarc_gke_cluster
      location  = var.region
      namespace = var.eventarc_gke_namespace
      path      = var.eventarc_gke_path
      service   = var.eventarc_gke_service
    }{%- endif %}
  }

  service_account = "${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

