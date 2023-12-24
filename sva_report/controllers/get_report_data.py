# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe
from sva_report.utils.filter import Filter
from sva_report.utils.doc_type_info import DocTypeInfo
allowed_types = ['Data', 'Int', 'Select', 'Check', 'Phone']
child_types = ['Table', 'Table MultiSelect']
@frappe.whitelist()
def execute(doc,filters=[],skip=0, limit=10,csv_export=0,debug=None):
    res= DocTypeInfo.get_data('SVA Report',doc, filters,skip, limit,csv_export, debug )
    return res
