import json
import logging
import time
from jose import jwt
import requests

from odoo import api, models

_logger = logging.getLogger(__name__)


class ForwardQueueJob(models.AbstractModel):
    _name = "cx_api_partner_job.forward_queue_job"
    _description = "Process pending forward queue entries"

    def _create_token(self, company):
        aud = company.api_audience
        iss = company.api_issuer
        key = company.api_key
        exp = time.time() + 600
        if not all([aud, iss, key]):
            raise ValueError("Missing API auth configuration in company settings")
        return jwt.encode({"aud": aud, "iss": iss, "exp": exp, "email": "admin"}, key=key, algorithm=jwt.ALGORITHMS.HS256)

    def _headers(self, company):
        token = self._create_token(company)
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def _is_success(self, response):
        """Check if response indicates success.
        
        Validates both HTTP status and JSON response body.
        """
        if response.status_code >= 400:
            return False, f"HTTP {response.status_code}: {response.text}"
        
        try:
            data = response.json()
            # Check for JSONRPC error
            if data.get("error"):
                return False, json.dumps(data.get("error", {}))
            # Check for ERROR key in response
            if data["result"].get("ERROR"):
                return False, json.dumps({"error": data.get("ERROR")})
            # Assume success if has result or SUCCESS
            if data.get("result") or data.get("SUCCESS"):
                return True, None
            # If no error but also no result, it's suspicious
            return False, "No result or SUCCESS in response"
        except ValueError:
            # JSON parse error
            return False, f"Invalid JSON response: {response.text[:200]}"

    @api.model
    def run_forward_queue(self):
        company = self.env.company
        if not company.contact_forward_enabled:
            return True
        
        base_url = company.api_base_url or ""
        endpoint = company.api_endpoint or ""
        timeout = company.api_timeout or 120
        
        if not base_url or not endpoint:
            _logger.warning("Forward API base_url/endpoint not configured; skipping job")
            return True
        
        url = f"{base_url}{endpoint}"

        queue_model = self.env["cx_api_partner_forward_queue.forward_queue"].sudo()
        
        try:
            headers = self._headers(company)
        except ValueError as ex:
            _logger.error("Cannot create JWT token: %s", str(ex))
            return True
        
        pending = queue_model.search([("status", "=", "pending")], limit=50, order="created_at asc")
        retry_pending = queue_model.search([("status", "=", "retry_pending")], limit=25, order="created_at asc")
        
        # Combine both lists for processing
        items_to_process = list(pending) + list(retry_pending)
        
        _logger.info(f"Forward queue processing: {len(pending)} pending + {len(retry_pending)} retry_pending = {len(items_to_process)} total")
        
        for item in items_to_process:
            try:
                res = requests.post(url, data=json.dumps(json.loads(item.payload)), headers=headers, timeout=timeout)
                is_success, error_msg = self._is_success(res)
                
                if is_success:
                    item.write({
                        "status": "success",
                        "attempts": item.attempts + 1,
                        "response_code": res.status_code,
                        "response_payload": res.text[:5000],  # Limit response size
                        "error_message": None,
                    })
                else:
                    # Determine if retryable
                    new_status = "retry_pending" if item.attempts < 5 else "failed"
                    item.write({
                        "status": new_status,
                        "attempts": item.attempts + 1,
                        "response_code": res.status_code,
                        "error_message": error_msg or res.text[:1000],
                    })
                    
            except requests.Timeout:
                new_status = "retry_pending" if item.attempts < 5 else "failed"
                item.write({
                    "status": new_status,
                    "attempts": item.attempts + 1,
                    "error_message": "Request timeout",
                })
            except requests.ConnectionError as ex:
                new_status = "retry_pending" if item.attempts < 5 else "failed"
                item.write({
                    "status": new_status,
                    "attempts": item.attempts + 1,
                    "error_message": f"Connection error: {str(ex)[:500]}",
                })
            except Exception as ex:
                item.write({
                    "status": "failed",
                    "attempts": item.attempts + 1,
                    "error_message": f"Unexpected error: {str(ex)[:500]}",
                })
        
        return True
