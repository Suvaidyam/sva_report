// Copyright (c) 2023, Rahul Sah and contributors
// For license information, please see license.txt
var fields = []
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
frappe.ui.form.on("SVA Report", {
	refresh(frm) {

	},
  map_columns:async(frm)=>{
      // MultiSelectDialog with custom query method
      if(!fields.length){
          fields = await callAPI({
              method:'sva_report.controllers.get_report_data.get_fields',
              args:{
                  doc:frm.doc.ref_doctype
              },
              freeze_message: __("Getting fields..."),
          })
          // console.log("fields",fields)
      }
      var d = new frappe.ui.Dialog({
          'fields': fields.map(field=> {return {fieldname:field.fieldname, fieldtype:"Check", label:field.label}}),
          primary_action: function(obj){
              d.hide();
              console.log(d.get_values(),obj);
          }
      });
      // d.fields_dict.ht.$wrapper.html('Hello World');
      d.show();
    }
});
