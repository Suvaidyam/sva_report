// Copyright (c) 2023, Rahul Sah and contributors
// For license information, please see license.txt
var fields = []
var checked_data = []
// Calling APIs Common function
function callAPI(options) {
  return new Promise((resolve, reject) => {
    frappe.call({
      ...options,
      callback: async function (response) {
        resolve(response?.message || response?.value)
      }
    });
  })
}
async function arrangeFields(fields, checked_data = []) {
  const groupedFields = {};
  await fields.forEach(field => {
    const doctype = field.doc_type || 'default';
    if (!groupedFields[doctype]) groupedFields[doctype] = [];
    groupedFields[doctype].push(field);
  });
  return Object.entries(groupedFields).flatMap(([doctype, fields]) => [
    { fieldname: `${doctype}_section_break`, fieldtype: "Section Break", label: `${doctype} Details` },
    ...fields.map(field => {
      if (checked_data.length > 0 && checked_data.includes(field.fieldname)) {
        return { fieldname: field.fieldname, fieldtype: "Check", label: field.label, ft: field.fieldtype, default: 1 }
      } else {
        return { fieldname: field.fieldname, fieldtype: "Check", label: field.label, ft: field.fieldtype, default: 0 }
      }
    })
  ]);
}
frappe.ui.form.on("SVA Report", {
  refresh(frm) {

  },
  map_columns: async (frm) => {
    if (!fields.length) {
      fields = await callAPI({
        method: 'sva_report.controllers.get_report_data.get_fields',
        args: {
          doc: frm.doc.ref_doctype
        },
        freeze_message: __("Getting fields..."),
      })
    }
    if (!checked_data.length) {
      checked_data = await callAPI({
        method: 'sva_report.controllers.child_table_crud.get_all_child_doc',
        args: {
          doctype: "Report Column",
          parent: frm.doc.name,
          parentfield: "columns",
          parenttype: "SVA Report",
        },
        freeze_message: __("Getting fields..."),
      })
    }
    const arrangedFields = await arrangeFields(fields, checked_data);
    let dialog_fields = [{
      "fieldname": "origin_details_section",
      "fieldtype": "Section Break",
      "label": "Origin details"
    }, ...arrangedFields]
    var d = new frappe.ui.Dialog({
      'fields': dialog_fields,
      primary_action: async function (obj) {
        const filteredKeys = Object.entries(obj).filter(([key, value]) => value === 1).map(([key, value]) => key);
        const checked_docs = d?.fields?.filter((field) => filteredKeys?.includes(field?.fieldname))
        await callAPI({
          method: 'sva_report.controllers.child_table_crud.delete_all_child_doc',
          args: {
            doctype: "Report Column",
            parent: frm.doc.name,
            parentfield: "columns",
            parenttype: "SVA Report",
          },
          freeze_message: __("Mapping columns..."),
        })
        if (checked_docs.length > 0) {
          await checked_docs?.forEach(async (doc) => {
            await callAPI({
              method: 'sva_report.controllers.child_table_crud.insert_child_doc',
              args: {
                doctype: "Report Column",
                parent: frm.doc.name,
                parentfield: "columns",
                parenttype: "SVA Report",
                fieldname: doc.fieldname,
                label: doc.label,
                fieldtype: doc.ft
              },
              freeze_message: __("Mapping columns..."),
            })
          });
        }
        d.hide();
      }
    });
    d.show();
  }
});
