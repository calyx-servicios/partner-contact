"""Forward Queue model for storing pending API forwards."""
import json
from datetime import datetime

from odoo import fields, models


class ForwardQueue(models.Model):
    """Model to store and track pending API forwards to external endpoints."""

    _name = "cx_api_partner_forward_queue.forward_queue"
    _description = "Forward Queue"
    _order = "created_at DESC"

    # Reference and identification
    reference = fields.Char(
        string="Reference",
        required=True,
        index=True,
        help="Unique identifier for this forward request"
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        ondelete="cascade",
    )

    # Target information
    url = fields.Char(
        string="Target URL",
        required=True,
        help="Full URL where the request will be forwarded"
    )

    method = fields.Selection(
        selection=[
            ("GET", "GET"),
            ("POST", "POST"),
            ("PUT", "PUT"),
            ("PATCH", "PATCH"),
            ("DELETE", "DELETE"),
        ],
        string="HTTP Method",
        default="POST",
        required=True,
    )

    # Request data
    payload = fields.Text(
        string="Payload",
        help="Request body (JSON format)"
    )

    headers = fields.Text(
        string="Headers",
        help="Request headers (JSON format)"
    )

    # Status tracking
    status = fields.Selection(
        selection=[
            ("pending", "Pending"),
            ("success", "Success"),
            ("failed", "Failed"),
            ("retry_pending", "Retry Pending"),
        ],
        string="Status",
        default="pending",
        required=True,
        index=True,
        help="Current state of the forward request"
    )

    attempts = fields.Integer(
        string="Attempts Made",
        default=0,
        help="Number of attempts made to forward this request"
    )

    # Response tracking
    response_code = fields.Integer(
        string="HTTP Status",
        help="HTTP status code from the last attempt"
    )

    error_message = fields.Text(
        string="Error Message",
        help="Error message from the last failed attempt"
    )

    response_payload = fields.Text(
        string="Response",
        help="Response body from the last attempt"
    )

    # Timestamps
    created_at = fields.Datetime(
        string="Created",
        default=lambda self: datetime.now(),
        readonly=True,
    )

    updated_at = fields.Datetime(
        string="Updated",
        default=lambda self: datetime.now(),
        readonly=True,
    )

    def _log_success(self, response_code, response_payload=None):
        """Mark this forward as successfully sent."""
        self.write({
            "status": "success",
            "response_code": response_code,
            "response_payload": response_payload,
            "updated_at": datetime.now(),
        })

    def _log_failure(self, error_message, response_code=None, response_payload=None):
        """Log a failed forward attempt."""
        self.write({
            "status": "failed",
            "error_message": error_message,
            "response_code": response_code,
            "response_payload": response_payload,
            "updated_at": datetime.now(),
        })

    def _mark_retry_pending(self):
        """Mark this forward as pending retry."""
        self.write({
            "status": "retry_pending",
            "updated_at": datetime.now(),
        })

    def _increment_attempts(self):
        """Increment the attempt counter."""
        self.attempts += 1
