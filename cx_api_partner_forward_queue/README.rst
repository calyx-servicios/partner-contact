=====================
API Partner - Forward Queue
=====================

This module provides a queue system for storing and tracking API forwards to external endpoints.

Description
===========

The Forward Queue module stores pending API requests that need to be forwarded to external endpoints. It works in conjunction with the `cx_api_partner` module to:

- Store requests that fail during immediate forwarding
- Track request status: pending, success, failed, or retry_pending
- Provide visibility into forwarding failures and attempts
- Enable future integration with Odoo job scheduler for automatic retries

Key Features
============

- **Queue Storage**: All forwarding requests are logged to a persistent queue
- **Status Tracking**: Track the lifecycle of each forward request
- **Attempt Counter**: Monitor the number of attempts made for each request
- **Response Logging**: Store HTTP response codes, error messages, and response payloads
- **Admin Visibility**: Only system administrators can view the queue
- **Timestamp Tracking**: Record when requests were created and updated

State Machine
=============

The forward queue implements the following state transitions:

::

    pending
      ↓
    [Job tries to forward]
      ├→ success (HTTP < 400)
      └→ failed (error or HTTP >= 400)

    failed
      ↓
    [Admin marks for retry]
      └→ retry_pending
         ↓
       [Job tries again]
         ├→ success
         └→ failed

Model: Forward Queue
====================

The `cx_api_partner_forward_queue.forward_queue` model stores:

Fields:
-------

- **reference**: Unique identifier for the forward request
- **company_id**: Company that initiated the forward
- **url**: Target URL for the forward
- **method**: HTTP method (GET, POST, PUT, PATCH, DELETE)
- **payload**: Request body (JSON format)
- **headers**: HTTP headers (JSON format)
- **status**: Current state (pending, success, failed, retry_pending)
- **attempts**: Number of attempts made
- **response_code**: HTTP status code from last attempt
- **error_message**: Error message from last failure
- **response_payload**: Response body from last attempt
- **created_at**: Timestamp when created
- **updated_at**: Timestamp when last updated

Methods:
--------

- `_log_success(response_code, response_payload=None)`: Mark as successfully sent
- `_log_failure(error_message, response_code=None, response_payload=None)`: Log a failure
- `_mark_retry_pending()`: Mark for manual retry
- `_increment_attempts()`: Increment the attempt counter

Usage
=====

View Pending Forwards
---------------------

1. Go to CX API Partner → Forward Queue
2. The queue is visible only to system administrators
3. Filter by status (pending, failed, success, retry_pending)
4. Click on any record to view details including payload, headers, and response

Future: Automatic Retries via Job Scheduler
============================================

A future job scheduler can be configured to:

1. Find all records with `status = 'pending'` or `status = 'retry_pending'`
2. Attempt to forward each request to the configured URL
3. Update the status and response fields
4. Move successful requests to `status = 'success'`
5. Move failed requests back to `status = 'failed'`

Example job configuration (to be added later)::

    @api.model
    def _cron_process_forward_queue(self):
        """Process pending forwards in the queue."""
        queue = self.env['cx_api_partner_forward_queue.forward_queue']
        pending = queue.search([('status', 'in', ['pending', 'retry_pending'])])
        
        for record in pending:
            try:
                # Attempt forward
                # Update status
            except Exception as e:
                # Log error

Security
========

- Only system administrators can access the Forward Queue
- Access control is managed via `base.group_system` in `ir.model.access.csv`
- No access for regular users

Dependencies
============

- `cx_api_partner`: Main API Partner module (required)
- `base`: Odoo core module

Known Limitations
=================

- Manual retry is not yet implemented (coming in future version)
- Job scheduler integration is not yet implemented (planned for next version)
- Automatic cleanup of old records is not implemented (can be added on demand)

Support
=======

For issues or feature requests, contact Calyx Servicios.
