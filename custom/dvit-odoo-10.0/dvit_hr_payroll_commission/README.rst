.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================================
Payroll Commissions On Invoiced sales
=====================================

This module computes commissions on invoiced sales and allows you to add it to payslip

**Features list :**
    * Add commission rate, commission to contract.
    * Select commission type [ own Commisions, team leader Commisions, sales manager Commisions]
    * Link commission to Payslip.

Installation
============

Nothing special to install this module

Configuration
=============

* You must complete the Employee information and contract information.
* Also we must link a user on the employee.
* We must set sales person and team on the sale orders.
* we must set sale team manager or memeber for team leaders Commisions.

Usage
=====

    * To add commission to the payslip, you need to set commission type and a rate into the employee's contract.

    * You also need to add a the rule PAYCOMM to the contract's salary structure.

    * Create sales invocies with salesperson or sales team setup properly.

    * For sales team leader commission the user should be a team leader or member.

    * Commission is calculated for invoices' payments that occured after contract start date.

    * Commission is calculated based on payments only for now.

    * When you have this properly setup, you just have to compute your payslip to find PAYCOMM into the list.


Known issues / Roadmap
======================

    * Allow commission on invoices

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/mohamedhagag/dvit-odoo/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Sebastien Gendre <sge@open-net.ch>
* Yvon-Philippe Crittin <cyp@open-net.ch>
* David Coninckx <dco@open-net.ch>
* Mohamed M. Hagag <mohamedhagag1981@gmail.com>

Maintainer
----------

This module version is currently maintained by DVIT.ME - http://dvit.me .
