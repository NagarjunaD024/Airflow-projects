"""Metrics Dashboard View"""
from __future__ import annotations

from typing import TYPE_CHECKING

from airflow.auth.managers.models.resource_details import AccessView
from airflow.utils.session import NEW_SESSION, provide_session
from airflow.www.auth import has_access_view
from flask_appbuilder import BaseView, expose
from sqlalchemy import text

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class MetricsDashboardView(BaseView):
    """A Flask-AppBuilder View for a metrics dashboard"""

    default_view = "index"
    route_base = "/metrics_dashboard"

    @provide_session
    @expose("/")
    @has_access_view(AccessView.PLUGINS)
    def index(self, session: Session = NEW_SESSION):
        """Create dashboard view"""

        def interval(n: int):
            return f"now() - interval '{n} days'"

        dag_run_query = text(
            f"""
            SELECT
                dr.dag_id,
                SUM(CASE WHEN dr.state = 'success' AND dr.start_date > {interval(1)} THEN 1 ELSE 0 END) AS "1_day_success",
                SUM(CASE WHEN dr.state = 'failed' AND dr.start_date > {interval(1)} THEN 1 ELSE 0 END) AS "1_day_failed",
                SUM(CASE WHEN dr.state = 'success' AND dr.start_date > {interval(7)} THEN 1 ELSE 0 END) AS "7_days_success",
                SUM(CASE WHEN dr.state = 'failed' AND dr.start_date > {interval(7)} THEN 1 ELSE 0 END) AS "7_days_failed",
                SUM(CASE WHEN dr.state = 'success' AND dr.start_date > {interval(30)} THEN 1 ELSE 0 END) AS "30_days_success",
                SUM(CASE WHEN dr.state = 'failed' AND dr.start_date > {interval(30)} THEN 1 ELSE 0 END) AS "30_days_failed"
            FROM dag_run AS dr
            JOIN dag AS d ON dr.dag_id = d.dag_id
            WHERE d.is_paused != true
            GROUP BY dr.dag_id
        """
        )

        dag_run_stats = [dict(result) for result in session.execute(dag_run_query)]
        return self.render_template(
            "dashboard.html",
            title="Metrics Dashboard",
            dag_run_stats=dag_run_stats,
        )