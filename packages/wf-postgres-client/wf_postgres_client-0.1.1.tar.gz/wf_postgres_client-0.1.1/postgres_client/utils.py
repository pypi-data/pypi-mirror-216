import psycopg2.sql
import pandas as pd

def compose_select_sql(
    table,
    schema=None,
    fields=None,
    query_list=None,
):
    select_sql = psycopg2.sql.SQL('SELECT {fields_sql} FROM {source_sql}').format(
        fields_sql=compose_fields_sql(fields),
        source_sql=compose_source_sql(table, schema)
    )
    select_parameters = None
    if query_list is not None:
        conditions_sql, conditions_parameters = compose_conditions_sql(query_list)
        select_sql = psycopg2.sql.SQL(' ').join([
            select_sql,
            psycopg2.sql.SQL('WHERE {conditions_sql}').format(
                conditions_sql=conditions_sql
            )
        ])
        select_parameters = conditions_parameters
    return select_sql, select_parameters

def compose_fields_sql(fields=None):
    if fields is not None:
        fields_sql = psycopg2.sql.join(
            [psycopg2.sql.Identifier(field) for field in fields]
        )
    else:
        fields_sql = psycopg2.sql.SQL('*')
    return fields_sql

def compose_source_sql(
    table,
    schema=None
):
    if schema is not None:
        source_sql = psycopg2.sql.SQL('.').join([
            psycopg2.sql.Identifier(schema),
            psycopg2.sql.Identifier(table)
        ])
    else:
        source_sql = psycopg2.sql.Identifier(table)
    return source_sql

def compose_conditions_sql(query_list):
    conditions_sql_list = list()
    conditions_parameters = list()
    for query in query_list:
        condition_sql, condition_parameters = compose_condition_sql(query)
        conditions_sql_list.append(condition_sql)
        conditions_parameters.extend(condition_parameters)
    conditions_sql = psycopg2.sql.SQL(' AND ').join(conditions_sql_list)
    return conditions_sql, conditions_parameters

def compose_condition_sql(query):
    operator = query.get('operator')
    if operator == 'eq':
        return compose_eq_condition_sql(query)
    if operator == 'gt':
        return compose_gt_condition_sql(query)
    if operator == 'gte':
        return compose_gte_condition_sql(query)
    if operator == 'lt':
        return compose_lt_condition_sql(query)
    if operator == 'lte':
        return compose_lte_condition_sql(query)
    if operator == 'in':
        return compose_in_condition_sql(query)
    raise ValueError(f'Operator \'{operator}\' not supported')

def compose_eq_condition_sql(query):
    fields = query['fields']
    values = query['values']
    if len(fields) != len(values):
        raise ValueError(f'Equals condition received {len(fields)} fields but {len(values)} values')
    condition_sql = psycopg2.sql.SQL('({fields_sql}) = {values_sql}').format(
        fields_sql=psycopg2.sql.SQL(', ').join([psycopg2.sql.Identifier(field) for field in fields]),
        values_sql=psycopg2.sql.SQL(', ').join([psycopg2.sql.Placeholder() for _ in values]),
    )
    parameters_sql = values
    return condition_sql, parameters_sql

def compose_gt_condition_sql(query):
    fields = query['fields']
    values = query['values']
    if len(fields) != 1 or len(values) != 1:
        raise ValueError(f'Greater-than condition can only take a single field and a single value')
    condition_sql = psycopg2.sql.SQL('{field_sql} > {value_sql}').format(
        field_sql=psycopg2.sql.Identifier(fields[0]),
        value_sql=psycopg2.sql.Placeholder(),
    )
    parameters_sql = values
    return condition_sql, parameters_sql

def compose_gte_condition_sql(query):
    fields = query['fields']
    values = query['values']
    if len(fields) != 1 or len(values) != 1:
        raise ValueError(f'Greater-than-or-equal condition can only take a single field and a single value')
    condition_sql = psycopg2.sql.SQL('{field_sql} >= {value_sql}').format(
        field_sql=psycopg2.sql.Identifier(fields[0]),
        value_sql=psycopg2.sql.Placeholder(),
    )
    parameters_sql = values
    return condition_sql, parameters_sql

def compose_lt_condition_sql(query):
    fields = query['fields']
    values = query['values']
    if len(fields) != 1 or len(values) != 1:
        raise ValueError(f'Less-than condition can only take a single field and a single value')
    condition_sql = psycopg2.sql.SQL('{field_sql} < {value_sql}').format(
        field_sql=psycopg2.sql.Identifier(fields[0]),
        value_sql=psycopg2.sql.Placeholder(),
    )
    parameters_sql = values
    return condition_sql, parameters_sql

def compose_lte_condition_sql(query):
    fields = query['fields']
    values = query['values']
    if len(fields) != 1 or len(values) != 1:
        raise ValueError(f'Less-than-or-equal condition can only take a single field and a single value')
    condition_sql = psycopg2.sql.SQL('{field_sql} <= {value_sql}').format(
        field_sql=psycopg2.sql.Identifier(fields[0]),
        value_sql=psycopg2.sql.Placeholder(),
    )
    parameters_sql = values
    return condition_sql, parameters_sql

def compose_in_condition_sql(query):
    fields = query['fields']
    values = query['values']
    if len(fields) != 1:
        raise ValueError(f'In condition can only take a single field')
    condition_sql = psycopg2.sql.SQL('{field_sql} IN ({values_sql})').format(
        field_sql=psycopg2.sql.Identifier(fields[0]),
        values_sql=psycopg2.sql.SQL(', ').join([psycopg2.sql.Placeholder() for _ in values]),
    )
    parameters_sql = values
    return condition_sql, parameters_sql

def convert_to_dataframe(data_list, description):
    column_names = [descriptor.name for descriptor in description]
    dataframe = pd.DataFrame(data_list, columns=column_names)
    dataframe = pd.json_normalize(dataframe.to_dict(orient='records'))
    return dataframe
