==========================
Calyx Services Partner API
==========================

.. |badge1| image:: https://img.shields.io/badge/maturity-Stable-brightgreen
    :target: https://odoo-community.org/page/development-status
    :alt: Stable
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-calyx--servicios%2Fpartner--contact-lightgray.png?logo=github
    :target: https://github.com/calyx-servicios/partner-contact.git
    :alt: calyx-servicios/partner-contact.git

|badge1| |badge2| |badge3|

This module extends the functionality of Contacts to support creation of partners via API

**Table of contents**

.. contents::
   :local:

Configure
=========

* Go to Users & Companies > JWT Validators > cx_api_partner and configure the Issuer and the Secret Key.

Usage
=====

1. Make a request to the API to create a new Partner (/contacts/create/partner).

Code example::

    import time
    import json
    import requests
    from jose import jwt

    BASE_URL = "http://localhost:8069"

    CREATE_PARTNER_URL = f"{BASE_URL}/contacts/create/partner"

    TOKEN = jwt.encode(
        {
            "aud": "cx_api_partner",
            "iss": "issuer",
            "exp": time.time() + 600,
            "email": "admin",
        },
        key="secretkey",  # They key is set in Odoo JWT Validators configuration.
        algorithm=jwt.ALGORITHMS.HS256,
    )


    def create_partner():
        headers = {"Authorization": "Bearer " + TOKEN, "Content-type": "application/json"}
        data = {
            "jsonrpc": "2.0",
            "params":{
                "name": "Chile Company SRL",
                "company" : 5,
                "country" : "Chile",
                "vat" : "123456789",
                "identification_type" : "RUT",
                "responsibility_type" : "Emisor de boleta 2da categoria"
            }
        }

        res = requests.post(CREATE_PARTNER_URL, data=json.dumps(data), headers=headers)
        res = json.loads(res.content)
        print(res)


    create_partner()

Known issues / Roadmap
======================

* Bugs or Roadmap

Bug Tracker
===========

* Contact to the development team

Credits
=======

Authors
~~~~~~~

* Calyx Servicios S.A.

Contributors
~~~~~~~~~~~~

* `Calyx Servicios S.A. <https://odoo.calyx-cloud.com.ar/>`_
  
  * Marco Oegg
  
Maintainers
~~~~~~~~~~~

This module is maintained by Calyx Servicios S.A.

.. image:: https://ss-static-01.esmsv.com/id/13290/galeriaimagenes/obtenerimagen/?width=120&height=40&id=sitio_logo&ultimaModificacion=2020-05-25+21%3A45%3A05
   :alt: Calyx Servicios S.A.
   :target: https://odoo.calyx-cloud.com.ar/

CALYX SERVICIOS S.A. is part of the PGK Consultores economic group, member of an important global network, a world organization.
The PGK Consultores group is one of the 20 largest consultant-studios in Argentina with nearly 300 professionals.

This module is part of the `Partner Contact <https://github.com/calyx-servicios/partner-contact.git>`_ project on GitHub.
