# Copyright (c) 2023, Management System for Agrasarteach@suvaidyam.com and contributors
# For license information, please see license.txt

import frappe

@frappe.whitelist()
def insert_child_doc(doctype=None,parent=None,parentfield=None,parenttype=None,fieldname=None,label=None,fieldtype=None):
    doc = frappe.get_doc({
        'doctype': doctype,
        'parent':parent,
        'parentfield':parentfield,
        'parenttype':parenttype,
        'fieldname':fieldname,
        'label':label,
        'fieldtype':fieldtype
    })
    doc.insert(ignore_permissions=True)
    return doc

@frappe.whitelist()
def delete_all_child_doc(doctype=None,parent=None,parentfield=None,parenttype=None):
    frappe.db.delete(doctype, {
        "parent":parent,
        'parentfield':parentfield,
        'parenttype':parenttype
    })
    return True
@frappe.whitelist()
def get_all_child_doc(doctype=None,parent=None,parentfield=None,parenttype=None):
    list = frappe.db.get_list(doctype, 
        filters={
            "parent":parent,
            'parentfield':parentfield,
            'parenttype':parenttype
        },
        pluck='fieldname',
        ignore_permissions=True
    )
    return list