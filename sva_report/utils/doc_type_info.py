import frappe
import csv
from io import StringIO
from frappe.utils.response import Response

allowed_types = ['Data', 'Int', 'Select', 'Check', 'Phone']
child_types = ['Table', 'Table MultiSelect']
class DocTypeInfo:

    def get_fields(
            doc_type,
            fields,
            parent_field="",
            degree=1,
            link_table=None,
            child_table=None,
            child_degree=1
        ):
        # print("child_degree",child_degree)
        if parent_field:
            parent_field = f"{parent_field}."
        ref_doc_meta = frappe.get_meta(doc_type)
        for field in ref_doc_meta.fields:
            local_field = {"label": field.label,"fieldtype": field.fieldtype,"fieldname": f"{field.fieldname}","options": field.options}
            if field.fieldtype in allowed_types and field.print_hide != 1:
                fields.append({
                    "doc_type":doc_type,
                    "label": field.label,
                    "fieldtype": field.fieldtype,
                    "fieldname": f"{parent_field}{field.fieldname}",
                    "options": field.options,
                    "link_table":link_table,
                    "child_table":child_table
                })
            elif field.fieldtype == 'Link':
                if degree == 1:
                    new_parent_field = field.fieldname
                    if parent_field:
                        new_parent_field = f"{parent_field}{field.fieldname}"
                    link_fields = DocTypeInfo.get_fields(
                        doc_type=field.options,
                        fields=fields,
                        parent_field=new_parent_field,
                        degree=2,
                        link_table=local_field,
                        child_table=child_table,
                        child_degree=2
                    )
            elif field.fieldtype in child_types:
                local_field['parenttype'] = doc_type
                if child_degree == 1:
                    # print(child_degree,field.fieldtype,doc_type,field.options)
                    DocTypeInfo.get_fields(
                        doc_type=field.options,
                        fields=fields,
                        parent_field=field.fieldname,
                        degree=1,
                        link_table=None,
                        child_table=local_field,
                        child_degree=2
                    )

        return fields
    def prepare_fields(report_doc):
        report_fields = [column.fieldname for column in report_doc.columns]
        all_fields = DocTypeInfo.get_fields(report_doc.ref_doctype,[], parent_field="")
        fields = []
        if len(report_fields) > 0:
            for column in report_fields:
                for field in all_fields:
                    if field.get('fieldname') == column:
                        fields.append(field)
        else:
            fields.extend(all_fields)
        return fields
    def prepare_joins(base_tbl,fields):
        joins = []
        unique_link_table = []
        unique_child_table = []
        unique_child_link_table = []
        for field in fields:
            if field.get('child_table') is None and field.get('link_table'):
                tbl_name = f"`tab{field.get('link_table').get('options')}`"
                lnk_fieldname = f"{field.get('link_table').get('fieldname')}"
                if lnk_fieldname not in unique_link_table:
                    joins.append(f"LEFT JOIN {tbl_name} as {lnk_fieldname} ON {lnk_fieldname}.`name` = {base_tbl}.{lnk_fieldname}")
                    unique_link_table.append(lnk_fieldname)
            elif field.get('child_table') and field.get('link_table') is None:
                tbl_name = f"`tab{field.get('child_table').get('options')}`"
                lnk_fieldname = f"{field.get('child_table').get('fieldname')}"
                if lnk_fieldname not in unique_child_table:
                    joins.append(f"LEFT JOIN {tbl_name} as {lnk_fieldname} ON {lnk_fieldname}.`parent` = {base_tbl}.name")
                    unique_child_table.append(lnk_fieldname)
            elif field.get('child_table') and field.get('link_table'):
                tbl_name_ = f"`tab{field.get('child_table').get('options')}`"
                lnk_fieldname_ = f"{field.get('child_table').get('fieldname')}"
                if lnk_fieldname_ not in unique_child_table:
                    joins.append(f"LEFT JOIN {tbl_name_} as {lnk_fieldname_} ON {lnk_fieldname_}.`parent` = {base_tbl}.name")
                    unique_child_table.append(lnk_fieldname_)

                tbl_name = f"`tab{field.get('link_table').get('options')}`"
                lnk_fieldname = f"{field.get('link_table').get('fieldname')}"
                if lnk_fieldname not in unique_child_link_table:
                    joins.append(f"LEFT JOIN {tbl_name} as {lnk_fieldname} ON {lnk_fieldname}.`name` = {lnk_fieldname_}.{lnk_fieldname}")
                    unique_child_link_table.append(lnk_fieldname)
        return '\n'.join(joins)
    def prepare_columns(base_tbl,fields):
        columns = []
        field_obj = {}
        field_index = 0
        for field in fields:
            label = f"{field.get('label')}"
            fl = field_obj.get(label.lower(), None)
            if fl is None:
                field_obj[label.lower()] = 1
            else:
                field_obj[label.lower()] += 1
                label = f"{label}{str(fl)}"

            if len(field.get('fieldname').split('.')) == 3:
                columns.append(f"{field.get('fieldname').split('.')[1]}.{field.get('fieldname').split('.')[2]} as `{label}`")
            elif len(field.get('fieldname').split('.')) == 2:
                columns.append(f"{field.get('fieldname')} as `{label}`")
            elif len(field.get('fieldname').split('.')) == 1:
                columns.append(f"{base_tbl}.{field.get('fieldname')} as `{label}`")

            fields[field_index]['label'] = label
            field_index += 1

        columns_str = ',\n'.join(columns)
        if columns_str=="":
            columns_str = "*"
        return columns_str
    def prepare_condition(filters, rpt_filters):
        base_tbl_cond_list = []
        outer_tbl_condition = []
        if filters is not None:
            for filter in filters:
                if len(filter) == 3:
                    cond_str = f"{filter[0]} {filter[1]} '{filter[2]}'"
                    if len(filter[0].split('.')) == 1:
                        if all(filt.get('fieldname') == filter[0] for filt in rpt_filters):
                            base_tbl_cond_list.append(cond_str)
                        else:
                            outer_tbl_condition.append(cond_str)
                    elif len(filter[0].split('.')) == 2:
                        print("Logic pending")
                        outer_tbl_condition.append(cond_str)
                        # base_tbl_cond_list.append(cond_str)
        base_tbl_cond_str = f"WHERE {'AND'.join(base_tbl_cond_list)}" if len(base_tbl_cond_list) > 0 else ""
        outer_tbl_cond_str = f"WHERE {'AND'.join(outer_tbl_condition)}" if len(outer_tbl_condition) > 0 else ""
        return base_tbl_cond_str,outer_tbl_cond_str
    def prepare_base_query(doctype, fields, doc_filters, req_filters):
        base_tbl = f"`tab{doctype}`"
        columns_str = DocTypeInfo.prepare_columns(base_tbl,fields)
        join_str = DocTypeInfo.prepare_joins(base_tbl,fields)
        base_tbl_cond_str,outer_tbl_cond_str = DocTypeInfo.prepare_condition(req_filters, doc_filters)
        with_query = f"""
            WITH tmp_tble AS (
                select
                    {columns_str}
                from
                    (select * from {base_tbl} {base_tbl_cond_str} ) as {base_tbl}
                {join_str}
                {outer_tbl_cond_str}
            )
        """
        return with_query
    def get_total(with_query, skip=0):
        count=None
        if skip == 0:
            count_query = f"""
                {with_query}
                select count(*) as count from tmp_tble
            """
            count_result = frappe.db.sql(count_query, as_dict=True)
            if len(count_result)>0:
                count = count_result[0].get('count', None)
        return count
    def get_result(with_query, skip=0, limit=10):
        limit_str = '' if limit < 0 else f"LIMIT {limit} OFFSET {skip}"
        data_query = f"""
            {with_query}
            select * from tmp_tble {limit_str}
        """
        results = frappe.db.sql(data_query, as_dict=True)
        return results
    def generate_csv(doc_type, with_query,batch_size = 1000):
        start = 0
        rows_count = batch_size

        header = True

        while batch_size == rows_count:
            rows = DocTypeInfo.get_result(with_query, start, batch_size)
            rows_count = len(rows)

            if header and rows_count:
                # Write header
                csv_buffer = StringIO()
                csv_writer = csv.writer(csv_buffer)
                csv_writer.writerow(rows[0].keys())
                yield csv_buffer.getvalue()
                csv_buffer.seek(0)
                csv_buffer.truncate(0)
                header = False
            for row in rows:
                csv_buffer = StringIO()
                csv_writer = csv.writer(csv_buffer)
                csv_writer.writerow(row.values())
                yield csv_buffer.getvalue()
                csv_buffer.seek(0)
                csv_buffer.truncate(0)
            start += batch_size

        response.body = csv_data.getvalue()
        csv_data.close()
        # Create a CSV buffer in memory
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)

        # Write header
        csv_writer.writerow(data[0])
        yield csv_buffer.getvalue()
        csv_buffer.seek(0)
        csv_buffer.truncate(0)

        # Write data in batches
        for row in data[1:]:
            csv_writer.writerow(row)
            yield csv_buffer.getvalue()
            csv_buffer.seek(0)
            csv_buffer.truncate(0)
    def export_csv(doc_type, with_query):
        response = Response(DocTypeInfo.generate_csv(doc_type, with_query), content_type='text/csv')
        response.http_status_code = 200
        response.headers["Content-Disposition"] = f"attachment; filename={doc_type.lower()}.csv"
        return response

    def get_data(doc_type, doc_name,filters=[], skip=0, limit=10,csv_export='1',debug=False ):
        report_doc = frappe.get_doc(doc_type, doc_name)
        fields = DocTypeInfo.prepare_fields(report_doc)
        with_query = DocTypeInfo.prepare_base_query(report_doc.ref_doctype,fields,report_doc.filters, filters)
        if csv_export != '1':
            count=DocTypeInfo.get_total(with_query, skip)
            results=DocTypeInfo.get_result(with_query, skip, limit)
            return {
                'filters':[
                    {
                        "label":field.get('label'),
                        "name":field.get('label'),
                        "fieldname":field.get('fieldname'),
                        "fieldtype":field.get('fieldtype'),
                        "options":field.get('options')
                    } for field in report_doc.filters
                ],
                'columns':[{
                "label":field.get('label'),
                "name":field.get('label'),
                "fieldname":field.get('fieldname'),
                "fieldtype":field.get('fieldtype'),
                "options":field.get('options')
                } for field in fields],
                'data':results,
                'total_records':count
            }
        else:
            return DocTypeInfo.export_csv(doc_type, with_query)