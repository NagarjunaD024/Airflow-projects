"""Plugins example"""
from __future__ import annotations

from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint

from plugins.metrics_plugin.views.dashboard import MetricsDashboardView

# Creating a flask blueprint
metrics_blueprint = Blueprint(
    "Metrics",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)


class MetricsPlugin(AirflowPlugin):
    """Defining the plugin class"""

    name = "Metrics Dashboard Plugin"
    flask_blueprints = [metrics_blueprint]
    appbuilder_views = [
        {"name": "Dashboard", "category": "Metrics", "view": MetricsDashboardView()}
    ]