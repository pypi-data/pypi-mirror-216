import argparse
from concurrent import futures as cf
from concurrent.futures import Executor
from concurrent.futures import Future
from datetime import datetime
from typing import List, Dict, Optional, Any, Callable, Tuple

from seeq import spy, sdk
from seeq.sdk import ApiClient, ConditionUpdateInputV1, ScalarPropertyV1, ConditionMonitorInputV1, PropertyInputV1, \
    ConditionBatchInputV1

formula = "($s.setRefreshRate(1min){threshold})\n" \
          ".removeShorterThan(2*{ignore_gaps})\n" \
          ".merge({ignore_gaps})\n" \
          ".removeShorterThan({min_duration})\n" \
          ".setMaximumDuration(1day)\n" \
          ".setProperty('Customer','{customer}')\n" \
          ".setProperty('Domain','{domain}')\n" \
          ".setProperty('Server','{server}')\n" \
          ".setProperty('Metric', $s, average())\n" \
          ".setProperty('Workbook', '{workbook_url}')"
formula_bindings = {
    'Cpu.System.UsagePercent.Gauge': {'threshold': '>=0.9', 'min_duration': '5min', 'ignore_gaps': '1min'},
    'Processes.Appserver.ServerLoadPercent.Gauge': {'threshold': '>=2', 'min_duration': '5min',
                                                    'ignore_gaps': '1min'},
    'Threads.HttpServer.LongRunning.Queued.Timer.p75': {'threshold': '>10000', 'min_duration': '5min',
                                                        'ignore_gaps': '1min'},
}

DATASOURCE = 'Seeq Monitoring Script'

# This is hardcoded to our monitors site for simplicity, but can easily be externalized if needed
MONITORS_URL = "https://monitors.seeq.dev/"


def get_session_info(session: spy.Session) -> Tuple[str, str, str]:
    return session.client.host, session.client.auth_token, session.client.csrf_token  # type: ignore


def get_api_client(session_info: Tuple[str, str, str], disable_retries: bool = False) -> ApiClient:
    client = ApiClient(host=session_info[0])
    client.auth_token = session_info[1]
    client.csrf_token = session_info[2]
    if disable_retries:
        client.configuration.retry_timeout_in_seconds = 0
    return client


def run_parallel(job_name: str, fns: List[Callable], fn_args: List = (), use_threads: bool = True,
                 max_parallelism: Optional[int] = None, executor: Optional[Executor] = None,
                 timeout: Optional[int] = None) -> Tuple[List, List[Optional[Exception]], bool]:
    # Initialize result and error lists
    results = [False] * len(fns)
    errors: List[Optional[Exception]] = [None] * len(fns)

    # Run in same process if only one function is given or max_parallelism is 1
    if len(fns) <= 1 or max_parallelism == 1:
        has_errors = False
        for index, fn in enumerate(fns):
            try:
                results[index] = fn(*fn_args[index])
            except Exception as e:
                errors[index] = e
                has_errors = True
        return results, errors, has_errors

    # Execute in parallel and wait for all futures to finish
    local_executor = None
    try:
        local_executor = executor if executor is not None else \
            cf.ThreadPoolExecutor(max_workers=max_parallelism,
                                  thread_name_prefix=job_name) if use_threads else cf.ProcessPoolExecutor(
                max_workers=max_parallelism)
        futures: Dict[int, Future] = {
            index: (local_executor.submit(fn) if fn_args is None else local_executor.submit(fn, *fn_args[index]))
            for index, fn in enumerate(fns)
        }
        cf.wait(futures.values(), timeout=timeout)
    finally:
        if executor is None and local_executor is not None:
            local_executor.shutdown()

    # Collect results and errors
    for index, future in futures.items():
        try:
            results[index] = future.result(timeout=0)
        except Exception as e:
            errors[index] = e

    has_errors = len(list(filter(lambda entry: entry is not None, errors))) > 0

    return results, errors, has_errors


def now_suffix() -> str:
    return f"{datetime.now().isoformat(timespec='seconds').replace(':', '')}Z"


def delete_items(client, items: List[Dict], delete_also: bool = False):
    client.configuration.retry_timeout_in_seconds = 1
    api = sdk.ItemsApi(client)
    suffix = f"_DELETED_{now_suffix()}"
    for item in items:
        id = item['id']

        api.archive_item(id=id, delete=False, archived_reason="BY_USER")
        if delete_also:
            try:
                api.archive_item(id=id, delete=True, archived_reason="BY_USER")
            except Exception as e:
                if 'Data ID' in item:
                    new_data_id = f"{item['Data ID']}{suffix}"
                    api.set_property(id=id, property_name='Data ID', body=PropertyInputV1(value=new_data_id))


def assign_properties(item: Dict[str, Any], properties: List[Dict[str, Any]]) -> Dict[str, Any]:
    for p in properties:
        name = p['name'][0].lower() + p['name'][1:].replace(' ', '')
        item[name] = p['value'] + ('' if p.get('unitOfMeasure', 'string') == 'string' else
                                   p['unitOfMeasure'])
    return item


def get_item(session_info: Tuple[str, str, str], guid: str) -> Dict[str, Any]:
    return sdk.ItemsApi(api_client=get_api_client(session_info)).get_item_and_all_properties(
        id=guid, _response_type='json'  # type: ignore
    )


def get_item_properties(session_info: Tuple[str, str, str],
                        item_ids: List[str],
                        max_parallelism: Optional[int] = None,
                        executor: Optional[Executor] = None,
                        timeout: Optional[int] = None) -> List[Dict[str, Any]]:
    results, errors, has_errors = run_parallel('get_item_properties',
                                               [get_item for _ in item_ids],
                                               [(session_info, guid) for guid in item_ids],
                                               max_parallelism=max_parallelism, executor=executor, timeout=timeout)

    return results  # type: ignore


def create_alert_conditions(client, name_suffix: str,
                            formula: str, formula_bindings: Dict[str, Dict[str, Any]],
                            signals: List[Dict], dry_run: bool):
    inputs = []
    for s in signals:
        bindings = formula_bindings[s['name']]
        workbook_url = f"{MONITORS_URL}workbook/{s['scopedTo']}"
        bound_formula = formula.replace(
            '{customer}', s['customer']).replace(
            '{domain}', s['domain']).replace(
            '{server}', s['server']).replace(
            '{threshold}', bindings['threshold']).replace(
            '{min_duration}', bindings['min_duration']).replace(
            '{ignore_gaps}', bindings['ignore_gaps']).replace(
            '{workbook_url}', workbook_url)
        inputs.append(
            ConditionUpdateInputV1(
                name=f"{s['name']} {name_suffix}", scoped_to=s['scopedTo'],
                data_id=f"{s['dataID'].replace('{Signal}', '{Condition}')} {name_suffix}",
                datasource_class=s['datasourceClass'],
                datasource_id=s['datasourceID'],
                formula=bound_formula,
                parameters=[f"s={s['id']}"],
                replace_capsule_properties=True,
                additional_properties=[ScalarPropertyV1('Cache Enabled', None, True),
                                       ScalarPropertyV1('Customer', None, s['customer']),
                                       ScalarPropertyV1('Domain', None, s['domain']),
                                       ScalarPropertyV1('Server', None, s['server']),
                                       ScalarPropertyV1('Workbook', None, workbook_url)]))

    outputs = []
    if not dry_run and len(inputs) > 0:
        response: Dict = sdk.ConditionsApi(client).put_conditions(
            body=ConditionBatchInputV1(conditions=inputs), _response_type='json')  # type: ignore

        for output in response['itemUpdates']:
            if 'item' in output:
                outputs.append(output)
            else:
                print(output['errorMessage'])

    return outputs


def update_condition_monitor(client, conditions: List[Dict]):
    response: Dict = sdk.ConditionMonitorsApi(client).get_condition_monitors(
        name_search='SaaS Application Alerts', limit=1000000, _response_type='json')  # type: ignore

    outputs = []
    for item in response['conditionMonitorItems']:
        condition_ids = {guid.upper() for guid in item['conditionIds']}
        new_condition_ids = {c['item']['id'].upper() for c in conditions}
        if len(condition_ids.symmetric_difference(new_condition_ids)) > 0:
            input = ConditionMonitorInputV1(
                archived=item['isArchived'],
                condition_ids=list(new_condition_ids),
                cron_schedule=item['cronSchedule'],
                # description=item['description'],
                enabled=item['enabled'],
                name=item['name'],
                query_range_look_ahead=item['queryRangeLookAhead'])

            output: Dict = sdk.ConditionMonitorsApi(client).update_condition_monitor(
                id=item['id'], body=input, _response_type='json')  # type: ignore
            outputs.append(output)


def get_alert_signals(session_info: Tuple[str, str, str], delete_existing: bool = False) -> List[Dict]:
    client = get_api_client(session_info)
    if delete_existing:
        response: Dict = sdk.ItemsApi(client).search_items(
            filters=['Name==Cpu.System.UsagePercent.Gauge Alert && Datasource ID==Seeq Monitoring Script',
                     'Name==Processes.Appserver.ServerLoadPercent.Gauge Alert && Datasource ID==Seeq Monitoring '
                     'Script',
                     'Name==Threads.HttpServer.LongRunning.Queued.Timer.p75 Alert && Datasource ID==Seeq Monitoring '
                     'Script'],
            types=['CalculatedCondition'],
            limit=1000000, _response_type='json')  # type: ignore
        delete_items(client, response['items'], True)

    response: Dict = sdk.ItemsApi(client).search_items(
        filters=['Name==Cpu.System.UsagePercent.Gauge && Datasource ID==Seeq Monitoring Script',
                 'Name==Processes.Appserver.ServerLoadPercent.Gauge && Datasource ID==Seeq Monitoring Script',
                 'Name==Threads.HttpServer.LongRunning.Queued.Timer.p75 && Datasource ID==Seeq Monitoring Script'],
        types=['CalculatedSignal'],
        limit=1000000, _response_type='json')  # type: ignore
    items = {i['id']: i for i in response['items'] if not i['name'].endswith(' Alert')}

    signals = get_item_properties(session_info, list(items.keys()))
    return [s for s in [assign_properties(s, s['properties']) for s in signals] if 'customer' in s]


def main(url: str, user: str, access_key: str, password: str, delete_existing: bool):
    spy.options.allow_version_mismatch = True
    spy.login(url=url, access_key=access_key, username=user, password=password, ignore_ssl_errors=True, quiet=True)
    session_info = get_session_info(spy.session)
    client = get_api_client(session_info)
    signals = get_alert_signals(session_info, delete_existing)

    conditions = create_alert_conditions(client, 'Alert', formula, formula_bindings, signals, False)

    update_condition_monitor(client, conditions)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", required=False, help="User name to log in with")
    parser.add_argument("-p", "--password", required=False, help="Password name to log in with")
    parser.add_argument("-k", "--access_key", required=False, help="Access key to log in with")
    parser.add_argument("-d", "--delete_existing", required=False, default=False,
                        help="Deletes existing alert signals when true")

    args = parser.parse_args()
    main(MONITORS_URL, args.user, args.access_key, args.password, args.delete_existing)
