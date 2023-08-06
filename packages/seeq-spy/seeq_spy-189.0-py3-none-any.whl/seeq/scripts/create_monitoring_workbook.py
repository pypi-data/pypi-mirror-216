import argparse
import datetime
import itertools
import os
import pickle
import time
from datetime import date
from hashlib import shake_128
from typing import List, Union, Dict, Optional

import pandas as pd
from numpy import nan
from seeq import spy
from seeq.base.seeq_names import SeeqNames
from seeq.spy._common import EMPTY_GUID
from seeq.spy.workbooks import Analysis, AnalysisWorksheet

AGILE_FILTER_NAME = ' Agile Filter'
AGILE_FILTER_FORMULA = '.agileFilter(1min)'
DELTA_NAME = ' 5min Delta'
DELTA_FORMULA = '.aggregate(delta(), periods(5min), middleKey()).max(0)'
PERCENTILE = 'P95'
ROOT_NODE = {'influxdb': 'Monitors-POC', 'legacy': 'Performance Monitors'}
DATASOURCES_WORKBOOK_SUFFIX = ' - Datasources'
DATASOURCE = 'Seeq Monitoring Script'

# On some versions of Seeq some monitor signals we use here are not available. This sets a tolerance for how
# many we can safely tolerate. If we have too many signals missing it's likely that something is wrong with our input
# arguments, and we raise an exception.
MAX_MISSING_SIGNALS = 10

# These are the columns that are returned by spy.push in the result dataframe when pushing signal metadata
PUSH_RESULT_COLUMNS = ['Datasource Class', 'Datasource ID', 'Data ID', 'ID', 'Push Result']

# These are hardcoded to our monitors site for simplicity, but can easily be externalized if needed
MONITORS_URL = "https://monitors.seeq.site/"
SEEQ_PERSONNEL_USER_GROUP_GUID = '792CFDF4-94B3-44B3-A2CA-7157230CC1E2'
CUSTOMER_MONITORS_FOLDER_ID = '54BAFDB1-E742-42C0-B912-8902281E722F'


def monitor_group_definitions(server: str, influxdb: bool):
    definitions = {
        'System Overview': [
            {'path': ['Cpu', 'System', 'UsagePercent'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', 'Appserver', 'ServerLoadPercent'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'Jobs', 'User', 'Queued'],
             'name': 'Counter',
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'HttpServer', 'LongRunning', 'Queued'],
             'name': 'Counter',
             'calculated_signals': ['agile_filter']},
            {'path': ['Users', 'ActiveAuthenticatedUsers', 'Last15Min'],
             'name': 'Gauge'},
            {'path': ['Processes', 'Appserver', 'Uptime'],
             'name': 'Gauge'},
        ],
        'Cpu Overview': [
            {'path': ['Cpu', 'System', 'UsagePercent'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Cpu', 'Appserver', 'UsagePercent'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'Appserver', 'CpuUsagePercent'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
        ],
        'Cpu Usage': [
            {'path': ['Processes', server, 'Appserver', 'CpuUsagePercent'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'JvmLink', 'CpuUsagePercent'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'Nginx', 'CpuUsagePercent'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'Postgres', 'CpuUsagePercent'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'Renderer', 'CpuUsagePercent'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'ScalarCache', 'CpuUsagePercent'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'ScreenshotWorkers', 'CpuUsagePercent'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'SeriesCache', 'CpuUsagePercent'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'SeriesCachePostgres', 'CpuUsagePercent'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'SupervisorCore', 'CpuUsagePercent'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
        ],
        'Memory overview': [
            {'path': ['Processes', server, 'Appserver', 'MemoryUsageMB'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Memory', 'Appserver', 'AvailableMB'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Memory', 'System', 'AvailablePhysicalMemoryMB'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Cache', 'NonSeries', 'Memory'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
        ],
        'Memory usage': [
            {'path': ['Processes', server, 'Appserver', 'MemoryUsageMB'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'JvmLink', 'MemoryUsageMB'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'Nginx', 'MemoryUsageMB'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'Postgres', 'MemoryUsageMB'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'Renderer', 'MemoryUsageMB'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'ScalarCache', 'MemoryUsageMB'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'ScreenshotWorkers', 'MemoryUsageMB'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'SeriesCache', 'MemoryUsageMB'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'SeriesCachePostgres', 'MemoryUsageMB'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
            {'path': ['Processes', server, 'SupervisorCore', 'MemoryUsageMB'],
             'name': 'Gauge',
             'calculated_signals': ['agile_filter']},
        ],
        'Garbage Collector': [
            {'path': ['Memory', 'GarbageCollector', 'Pause', 'Timer'],
             'name': 'Count',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Memory', 'GarbageCollector', 'Pause', 'Timer'],
             'name': 'Mean',
             'calculated_signals': ['agile_filter']},
            {'path': ['Memory', 'GarbageCollector', 'Pause', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']},
            {'path': ['Memory', 'GarbageCollector', 'TotalPauseTime'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
        ],
        'Persistent Signal Cache': [
            {'path': ['Cache', 'Persistent', 'Signal', 'Read', 'Sample'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Cache', 'Persistent', 'Signal', 'Read', 'Time', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']},
            {'path': ['Cache', 'Persistent', 'Signal', 'Write', 'Time', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']}
        ],
        'Persistent Condition Cache': [
            {'path': ['Cache', 'Persistent', 'Condition', 'Read', 'Capsule'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Cache', 'Persistent', 'Condition', 'Read', 'Time', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']},
            {'path': ['Cache', 'Persistent', 'Condition', 'Write', 'Time', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']}
        ],
        'Disk Space': [
            {'path': ['HardDisk', 'Usage', 'AvailableBytes', 'DataFolder'],
             'name': 'Gauge'},
        ],
        'Disk MyData': [
            {'path': ['HardDisk', 'Usage', 'Folders', 'MyData', 'FileCount'],
             'name': 'Gauge'},
            {'path': ['HardDisk', 'Usage', 'Folders', 'MyData', 'FolderCount'],
             'name': 'Gauge'},
            {'path': ['HardDisk', 'Usage', 'Folders', 'MyData', 'Size'],
             'name': 'Gauge'},
        ],
        'Disk Cache': [
            {'path': ['HardDisk', 'Usage', 'Folders', 'Cache', 'Content', 'FileCount'],
             'name': 'Gauge'},
            {'path': ['HardDisk', 'Usage', 'Folders', 'Cache', 'Series', 'FileCount'],
             'name': 'Gauge'},
            {'path': ['HardDisk', 'Usage', 'Folders', 'Cache', 'Thumbnail', 'FileCount'],
             'name': 'Gauge'},
            {'path': ['HardDisk', 'Usage', 'Folders', 'Cache', 'Content', 'FolderCount'],
             'name': 'Gauge'},
            {'path': ['HardDisk', 'Usage', 'Folders', 'Cache', 'Series', 'FolderCount'],
             'name': 'Gauge'},
            {'path': ['HardDisk', 'Usage', 'Folders', 'Cache', 'Thumbnail', 'FolderCount'],
             'name': 'Gauge'},
            {'path': ['HardDisk', 'Usage', 'Folders', 'Cache', 'Content', 'Size'],
             'name': 'Gauge'},
            {'path': ['HardDisk', 'Usage', 'Folders', 'Cache', 'Series', 'Size'],
             'name': 'Gauge'},
            {'path': ['HardDisk', 'Usage', 'Folders', 'Cache', 'Thumbnail', 'Size'],
             'name': 'Gauge'},
        ],
        'Long running requests': [
            {'path': ['Threads', 'HttpServer', 'LongRunning', 'Running'],
             'name': 'Counter',
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'HttpServer', 'LongRunning', 'Completed'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Threads', 'HttpServer', 'LongRunning', 'Submitted'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Threads', 'HttpServer', 'LongRunning', 'Queued'],
             'name': 'Counter',
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'HttpServer', 'LongRunning', 'Queued', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'HttpServer', 'LongRunning', 'Duration', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'HttpServer', 'LongRunning', 'Queued', 'Timer'],
             'name': 'P75',
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'HttpServer', 'LongRunning', 'Duration', 'Timer'],
             'name': 'P75',
             'calculated_signals': ['agile_filter']},
        ],
        'Users': [
            {'path': ['Users', 'ActiveAuthenticatedUsers', 'Last15Min'],
             'name': 'Gauge'},
            {'path': ['Users', 'BrowserTabs'],
             'name': 'Gauge'},
            {'path': ['Users', 'AuthenticatedUsers'],
             'name': 'Gauge'},
        ],
        'User jobs': [
            {'path': ['Threads', 'Jobs', 'User', 'Running'],
             'name': 'Counter',
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'Jobs', 'User', 'Completed'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Threads', 'Jobs', 'User', 'Queued'],
             'name': 'Counter',
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'Jobs', 'User', 'Queued', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'Jobs', 'User', 'Submitted'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Threads', 'Jobs', 'User', 'Duration', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']},
        ],
        'Date Range jobs': [
            {'path': ['Jobs', 'DateRangeJobs', 'Execution', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']},
            {'path': ['Jobs', 'DateRangeJobs', 'Execution', 'Timer'],
             'name': 'Count',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Jobs', 'DateRangeJobs', 'Completed'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Jobs', 'DateRangeJobs', 'Misfired'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
        ],
        'Report jobs': [
            {'path': ['Jobs', 'ReportJobs', 'Execution', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']},
            {'path': ['Jobs', 'ReportJobs', 'Execution', 'Timer'],
             'name': 'Count',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Jobs', 'ReportJobs', 'Completed'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Jobs', 'ReportJobs', 'Misfired'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
        ],
        'Async Migration jobs': [
            {'path': ['Jobs', 'AsyncMigrationStatus', 'Execution', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']},
            {'path': ['Jobs', 'AsyncMigrationStatus', 'Execution', 'Timer'],
             'name': 'Count',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Jobs', 'AsyncMigrationStatus', 'Completed'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Jobs', 'AsyncMigrationStatus', 'Misfired'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
        ],
        'Thread Pool Queues': [
            {'path': ['Threads', 'HttpServer', 'Jobs', 'Queued'],
             'name': 'Counter',
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'HttpServer', 'Request', 'Queued'],
             'name': 'Counter',
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'HttpServer', 'LongRunning', 'Queued'],
             'name': 'Counter',
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'HttpServer', 'Default', 'Queued'],
             'name': 'Counter',
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'HttpServer', 'Initialization', 'Queued'],
             'name': 'Counter',
             'calculated_signals': ['agile_filter']}
        ],
        'Client Websocket': [
            {'path': ['Threads', 'ClientWebSocket', 'Messages', 'Running'],
             'name': 'Counter',
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'ClientWebSocket', 'Messages', 'Queued'],
             'name': 'Counter',
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'ClientWebSocket', 'Messages', 'Completed'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Threads', 'ClientWebSocket', 'Messages', 'Duration', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']}
        ],
        'Agent Websocket': [
            {'path': ['Threads', 'AgentWebSocket', 'Messages', 'Running'],
             'name': 'Counter',
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'AgentWebSocket', 'Messages', 'Queued'],
             'name': 'Counter',
             'calculated_signals': ['agile_filter']},
            {'path': ['Threads', 'AgentWebSocket', 'Messages', 'Completed'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Threads', 'AgentWebSocket', 'Messages', 'Duration', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']}
        ],
        'Network': [
            {'path': ['Network', 'PubSub', 'Channels', 'BroadcastChannel', 'Subscribers'],
             'name': 'Counter',
             'calculated_signals': ['agile_filter']},
            {'path': ['Network', 'AgentWebSocket', 'ConnectedAgents'],
             'name': 'Gauge'},
            {'path': ['Network', 'HttpServer', 'RestAPI', 'Samples'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Network', 'HttpServer', 'RestAPI', 'Capsules'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']}
        ],
        'Screenshots': [
            {'path': ['Rendering', 'HeadlessCapture', 'Screenshot', 'Timing', 'TotalRenderingTime', 'Timer'],
             'name': 'Count',
             'calculated_signals': ['agile_filter']},
            {'path': ['Rendering', 'HeadlessCapture', 'Screenshot', 'Timing', 'TotalRenderingTime', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']},
            {'path': ['Rendering', 'HeadlessCapture', 'Screenshot', 'Timing', 'Queued', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']},
            {'path': ['Rendering', 'HeadlessCapture', 'Screenshot', 'Timing', 'DataDownload', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']},
            {'path': ['Rendering', 'HeadlessCapture', 'Screenshot', 'Result', 'Aborted'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Rendering', 'HeadlessCapture', 'Screenshot', 'Result', 'Successful'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Rendering', 'HeadlessCapture', 'Screenshot', 'Queued'],
             'name': 'Gauge',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Rendering', 'HeadlessCapture', 'Screenshot', 'Running'],
             'name': 'Gauge',
             'calculated_signals': ['delta_agile_filter']}
        ],
        'Thumbnails': [
            {'path': ['Rendering', 'HeadlessCapture', 'Thumbnail', 'Timing', 'TotalRenderingTime', 'Timer'],
             'name': 'Count',
             'calculated_signals': ['delta_agile_filter']},
            {'path': ['Rendering', 'HeadlessCapture', 'Thumbnail', 'Timing', 'TotalRenderingTime', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']},
            {'path': ['Rendering', 'HeadlessCapture', 'Thumbnail', 'Timing', 'Queued', 'Timer'],
             'name': PERCENTILE,
             'calculated_signals': ['agile_filter']},
            {'path': ['Rendering', 'HeadlessCapture', 'Thumbnail', 'Result', 'Aborted'],
             'name': 'Meter',
             'calculated_signals': ['delta_agile_filter']}
        ],
    }

    def map_name(v: str) -> str:
        if v == 'Gauge':
            return 'Gauge.value'
        if v == 'Counter' or v == 'Meter':
            return f"{v}.count"
        return v.lower()

    if influxdb:
        definitions = {key: [{k: map_name(v) if k == 'name' else v for k, v in d.items()} for d in value]
                       for key, value in definitions.items()}

    return definitions


EXCLUDED_DATASOURCES = {
    'Add-on Calculation Python UDFs',
    'Auth',
    'CassandraV2',
    'ConnectedCount',
    'CSV',
    'External Calculation Python UDFs',
    'FileFolders',
    'FileSignal',
    'Imported CSV Files',
    'Monitors',
    'OAuth 2_0',
    'Postgres Datums',
    'Rx',
    'Seeq - FileSignal',
    'Seeq Calculations',
    'Seeq Data Lab',
    'Seeq Metadata',
    'SeeqMonitors',
    'Seeq - Signal Datasource',
    'Time Series CSV Files',
}

COLOR_CODES = [
    '#0910a4', '#cfd1fc', '#c01311', '#f19695', '#8B6969', '#D2C3C3', '#d94bff', '#eca5ff', '#7e86d6', '#bec2ea',
    '#c70000', '#ff6363', '#0075d2', '#69bdff', '#e6d50a', '#f9f07e', '#ff5959', '#ffacac', '#ffd8ba', '#ffebdc',
    '#ff7d1a', '#ffbe8c', '#e3e751', '#f1f3a8', '#00ced1', '#b4feff', '#0a0dd8', '#7779f9', '#08d2fb', '#b5f1fe',
    '#C67171', '#E7C4C4', '#F4A460', '#FAD8BA', '#8B7355', '#D4C8B9', '#777733', '#D8D8A4', '#DB2645', '#F1A8B5',
    '#5C246E', '#CC97DD', '#23238E', '#9898E6', '#7e86d6', '#bec2ea', '#d94bff', '#eca5ff', '#c70000', '#ff6363',
]
MANY_COLOR_CODES = COLOR_CODES * 13


def assign_color_to_stored_signals(results: pd.DataFrame, lane: int, offset: int = 1) -> None:
    results['Color'] = MANY_COLOR_CODES[2 * lane - offset]


def customize_stored_signals_trend_display(results: pd.DataFrame, lane: int) -> pd.DataFrame:
    results['Line Width'] = 0.5
    results['Lane'] = lane
    results['Axis Group'] = lane,
    results['Line Style'] = 'Solid'
    assign_color_to_stored_signals(results, lane)
    return results


# Use this calculation to smooth a gauge or other counter that can go up or down such as CPU Usage or Job Run Time
def create_agile_filter_calculated_signal(name: str, formula_guid: str, lane: int) -> pd.DataFrame:
    signal_name = name.replace(' >> ', '.') + AGILE_FILTER_NAME + f'-{variable_digest(formula_guid, 3)}'
    df = pd.DataFrame([{
        'Name': signal_name,
        'Type': SeeqNames.Types.signal,
        'Formula': f'$s{AGILE_FILTER_FORMULA}',
        'Formula Parameters': {'$s': formula_guid},
        'Line Width': 1.5,
        'Lane': lane,
        'Axis Group': lane,
        'Color': MANY_COLOR_CODES[2 * lane - 2],
    }])
    df.set_index('Name', inplace=True, drop=False)
    return df


# Use this calculation for meters that only count upward such as those for Samples Read or Jobs Completed
def create_delta_agile_filter_calculated_signal(name: str, formula_guid: str, lane: int) -> pd.DataFrame:
    signal_name = name.replace(' >> ', '.') + DELTA_NAME + AGILE_FILTER_NAME + f'-{variable_digest(formula_guid, 3)}'
    df = pd.DataFrame([{
        'Name': signal_name,
        'Type': SeeqNames.Types.signal,
        'Formula': f'$s{DELTA_FORMULA}{AGILE_FILTER_FORMULA}',
        'Formula Parameters': {'$s': formula_guid},
        'Line Width': 1.5,
        'Lane': lane,
        'Color': MANY_COLOR_CODES[2 * lane - 2],
    }])
    df.set_index('Name', inplace=True, drop=False)
    return df


CALCULATED_SIGNAL_BUILDERS = {
    'agile_filter': create_agile_filter_calculated_signal,
    'delta_agile_filter': create_delta_agile_filter_calculated_signal,
}


def push_calculated_signals(calculated_signals_to_trend: pd.DataFrame, workbook_id: str,
                            worksheet_name: str) -> pd.DataFrame:
    start = time.time()
    print(f'Pushing calculated signals for worksheet {worksheet_name}')

    results = spy.push(
        metadata=calculated_signals_to_trend.reset_index(drop=True),
        datasource=DATASOURCE,
        workbook=workbook_id,
        worksheet=None,
        quiet=True
    )
    results.set_index('Name', inplace=True, drop=False)

    print(f'Finished pushing {len(results)} calculated signals for worksheet {worksheet_name} in'
          f' {int((time.time() - start) * 1000)} millis')

    return results


def init_sq_trend_store(stores):
    if 'sqTrendStore' not in stores:
        stores.update({'sqTrendStore': {'enabledColumns': {}}})


def enable_display_properties(stores) -> None:
    init_sq_trend_store(stores)
    stores['sqTrendStore']['enabledColumns']['SERIES'] = {"fullpath": True, "lane": True}


def enable_dimming(stores) -> None:
    init_sq_trend_store(stores)
    stores['sqTrendStore']['hideUnselectedItems'] = True


def set_trend_labels(label, location, stores) -> None:
    init_sq_trend_store(stores)
    stores['sqTrendStore']['labelDisplayConfiguration'] = {label: location}


def set_auto_update_display_range(stores) -> None:
    stores['sqDurationStore']['autoUpdate']['mode'] = 'MANUAL'
    stores['sqDurationStore']['autoUpdate']['manualInterval'] = {'value': 5, 'units': 'min', 'valid': True}


def set_worksheet_display_items(worksheet: AnalysisWorksheet, signals_to_trend: Union[List, pd.DataFrame]) -> None:
    if isinstance(signals_to_trend, List):
        signals_to_trend = pd.concat(signals_to_trend, ignore_index=True)
    worksheet.display_items = signals_to_trend
    stores = worksheet.current_workstep().get_workstep_stores()
    set_trend_labels('name', 'lane', stores)
    set_auto_update_display_range(stores)
    enable_display_properties(stores)
    enable_dimming(stores)


def create_worksheet_for_monitor(workbook: Analysis, monitor: str, start: datetime.date, end: datetime.date):
    worksheet = workbook.worksheet(monitor)
    worksheet.display_range = {
        'Start': start,
        'End': end
    }
    return worksheet


def get_stored_signal_lane_def(signal_metadata: pd.DataFrame, signal: Dict, lane: int, influxdb: bool) -> \
        pd.DataFrame:
    if influxdb:
        signal_name = signal['name'].split('.')
        signal_asset = signal_name[0] if len(signal_name) > 1 else signal['path'][-1]
        signal_path = build_path_str(signal['path'] if len(signal_name) > 1 else signal['path'][:-1])
        results = signal_metadata[(signal_metadata['Path'].str.lower().str.endswith(signal_path.lower())) &
                                  (signal_metadata['Asset'] == signal_asset) &
                                  (signal_metadata['Name'].str.lower() == signal_name[-1].lower())].copy()
        results['Name'] = build_name_str(signal['path'], signal_name[0])
    else:
        signal_name = build_name_str(signal['path'], signal['name'])
        results = signal_metadata[signal_metadata['Name'].str.lower() == signal_name.lower()].copy()

    if not results.empty:
        results['Lane'] = lane
        if 'calculated_signals' in signal:
            customize_stored_signals_trend_display(results, lane)
        else:
            assign_color_to_stored_signals(results, lane, 2)
    return results


def get_calculated_signal_lane_def(signal_metadata: pd.DataFrame, signal: dict, lane: int) -> Union[pd.DataFrame, None]:
    if 'calculated_signals' not in signal:
        return None
    if signal_metadata.empty:
        return None
    if pd.isnull(signal_metadata['ID'].item()):
        return None

    calculated_signals = [CALCULATED_SIGNAL_BUILDERS[filter_name] for filter_name in signal['calculated_signals']]
    path_in_name = signal['name'].split('.')
    signal_path = build_path_str(signal['path'], [path_in_name[0]]) if len(path_in_name) > 1 \
        else build_path_str(signal['path'])
    return pd.concat([
        filter_func(signal_path, stored_signal, lane)
        for stored_signal in signal_metadata['ID']
        for filter_func in calculated_signals
    ]).set_index('Name', drop=False)


def merge_push_results(lane_defs: List[pd.DataFrame], pushed_signals: pd.DataFrame) -> List[pd.DataFrame]:
    return [
        lane_def.merge(
            pushed_signals[PUSH_RESULT_COLUMNS],
            left_index=True,
            right_index=True
        )
        for lane_def in lane_defs
        if lane_def is not None
    ]


def create_regular_monitor_worksheets(workbook: Analysis,
                                      signal_metadata: pd.DataFrame,
                                      two_weeks_ago: datetime.date,
                                      today: datetime.date,
                                      server: str,
                                      influxdb: bool
                                      ) -> None:
    worksheet_definitions = {}
    calculated_signals_to_push = []
    missing = 0
    for monitor_group, monitor_definitions in monitor_group_definitions(server, influxdb).items():
        worksheet = create_worksheet_for_monitor(workbook, monitor_group, two_weeks_ago, today)
        stored_signal_lane_defs = [get_stored_signal_lane_def(signal_metadata, monitor_definition, i + 1, influxdb)
                                   for i, monitor_definition
                                   in enumerate(monitor_definitions)]
        for stored_signal_lane_def, monitor_definition in zip(stored_signal_lane_defs, monitor_definitions):
            if stored_signal_lane_def.empty:
                missing += 1
                name = build_name_str(monitor_definition['path'], monitor_definition['name'])
                print(f"A Stored Signal {name} wasn't found")

        if missing > MAX_MISSING_SIGNALS:
            raise RuntimeError(f"Too many missing Signals. Arguments to --server and --fqdn probably need to differ")

        calculated_signal_lane_defs = [
            get_calculated_signal_lane_def(stored_signal_lane_def, monitor_definition, i + 1)
            for i, (stored_signal_lane_def, monitor_definition)
            in enumerate(zip(stored_signal_lane_defs, monitor_definitions))
        ]
        calculated_signal_lane_defs = [s for s in calculated_signal_lane_defs if s is not None]

        worksheet_definitions[monitor_group] = {
            'worksheet': worksheet,
            'stored_signal_lane_defs': stored_signal_lane_defs,
            'calculated_signal_lane_defs': calculated_signal_lane_defs
        }

        if influxdb:
            for results in stored_signal_lane_defs:
                if not results.empty:
                    results['Formula'] = '$s'
                    results['Formula Parameters'] = [{'$s': results['ID'].iloc[0]}]
                    results['Type'] = 'CalculatedSignal'
                    results.set_index('Name', inplace=True, drop=False)
                    calculated_signals_to_push.append(results)
        calculated_signals_to_push.extend(calculated_signal_lane_defs)

    # remove ids for calculated signals constructed from stored signals
    if influxdb:
        for results in calculated_signals_to_push:
            if 'ID' in results.columns:
                results['Asset'] = nan
                results['Path'] = nan
                results.drop(columns=['ID', 'Datasource Name', 'Archived'], inplace=True)

    # some worksheets monitor the same signals, so we need to drop duplicates to successfully push everything
    signals_to_push = pd.concat(calculated_signals_to_push, ignore_index=True, copy=False
                                ).drop_duplicates(subset=['Name'])
    pushed_signals = push_calculated_signals(signals_to_push, workbook.id, '{All worksheets}')

    worksheet_definitions = {
        monitor_group: {
            **worksheet_definition,
            **({
                   'stored_signal_lane_defs': merge_push_results(
                       worksheet_definition['stored_signal_lane_defs'],
                       pushed_signals
                   )
               } if influxdb else {}),
            **{
                'calculated_signal_lane_defs': merge_push_results(
                    worksheet_definition['calculated_signal_lane_defs'],
                    pushed_signals
                )
            }
        }
        for monitor_group, worksheet_definition in worksheet_definitions.items()
    }
    for monitor_group, worksheet_definition in worksheet_definitions.items():
        worksheet = worksheet_definition['worksheet']
        lane_defs = [*worksheet_definition['stored_signal_lane_defs'],
                     *worksheet_definition['calculated_signal_lane_defs']]
        if len(lane_defs) > 0:
            set_worksheet_display_items(worksheet, lane_defs)


def create_datasource_monitor_worksheets(workbook: Analysis,
                                         signal_metadata: pd.DataFrame,
                                         two_weeks_ago: datetime.date,
                                         today: datetime.date,
                                         customer: str,
                                         fqdn: str,
                                         influxdb: bool) -> None:
    # Datasources are customer-dependent, so we have to go about them a little differently than other monitor data.
    base_path = f"{ROOT_NODE['influxdb' if influxdb else 'legacy']} >> {customer} >> {fqdn} >> Datasource"
    datasource_signal_paths = signal_metadata[signal_metadata['Path'].str.startswith(base_path)]['Path']
    datasources = datasource_signal_paths.str.split(' >> ', expand=True)
    if len(datasources.columns) <= 4:
        print(f'No Datasource paths found within path: {base_path}')
        return
    unique_datasources = set(sorted(datasources.iloc[:, 4].dropna()))
    eligible_datasources = sorted(unique_datasources - EXCLUDED_DATASOURCES)
    # It's more efficient to push all calcs in one call. Collect the worksheet->calcs, push all the calcs,
    # then add them into the worksheets with the desired formatting.
    worksheets_to_trend_items = []
    calculated_signals_to_push = []
    for datasource_class in eligible_datasources:
        datasource_class_path = f'{base_path} >> {datasource_class}'
        datasource_names = datasource_signal_paths[
            datasource_signal_paths.str.startswith(datasource_class_path)].str.split(' >> ', expand=True)
        unique_datasource_names = sorted(datasource_names.iloc[:, 5].dropna().unique()) \
            if len(datasource_names.columns) > 5 else []

        for datasource_name in unique_datasource_names:
            calculated_signals_to_trend = []
            signals_to_trend = []
            datasource_path = f'{datasource_class_path} >> {datasource_name}'

            # Timer Mean
            path = 'Rx >> Time'
            asset = 'Timer'
            name = 'mean' if influxdb else 'Mean'
            results = signal_metadata[(signal_metadata['Path'] == f'{datasource_path} >> {path}') &
                                      (signal_metadata['Asset'] == asset) &
                                      (signal_metadata['Name'].str.endswith(name))].copy()
            lane = 1
            if not results.empty:
                guid = results['ID'].iloc[0]
                calculated_signals_to_trend.append(create_agile_filter_calculated_signal(
                    f'{path}.{asset}.{name}', guid, 1))
                results['Name'] = f"{path.replace(' >>', '.')}.{asset}.{name}-{variable_digest(guid, 3)}"
                signals_to_trend.append(customize_stored_signals_trend_display(results, lane))
                lane += 1

            # Requests Gauge
            path = 'Requests' if influxdb else ''
            asset = 'Gauge' if influxdb else 'Requests'
            name = 'value' if influxdb else 'Gauge'
            results = signal_metadata[(signal_metadata['Path'] == f"{datasource_path}{' >> ' if path else ''}{path}") &
                                      (signal_metadata['Asset'] == asset) &
                                      (signal_metadata['Name'].str.endswith(name))].copy()
            if not results.empty:
                guid = results['ID'].iloc[0]
                results['Lane'] = lane
                results['Axis Group'] = lane,
                results['Name'] = f"{path.replace(' >>', '.')}.{asset}.{name}-{variable_digest(guid, 3)}"
                signals_to_trend.append(results)
                lane += 1

            # Receive Meters
            for monitor in ['Messages', 'Samples', 'Successes', 'Failures']:
                path = f'Rx >> {monitor}' if influxdb else 'Rx'
                asset = 'Meter' if influxdb else monitor
                name = 'count' if influxdb else 'Meter'
                results = signal_metadata[(signal_metadata['Path'].str.startswith(f'{datasource_path} >> {path}')) &
                                          (signal_metadata['Asset'] == asset) &
                                          (signal_metadata['Name'].str.endswith(name))].copy()
                if not results.empty:
                    guid = results['ID'].iloc[0]
                    calculated_signals_to_trend.append(create_delta_agile_filter_calculated_signal(
                        f'{path}.{asset}.{name}', guid, lane))
                    results['Name'] = f"{path.replace(' >>', '.')}.{asset}.{name}-{variable_digest(guid, 3)}"
                    signals_to_trend.append(customize_stored_signals_trend_display(results, lane))
                    lane += 1

            if len(calculated_signals_to_trend) > 0:
                worksheet = workbook.worksheet(f'{datasource_class} >> {datasource_name}'[:99])
                worksheet.display_range = {'Start': two_weeks_ago, 'End': today}
                worksheets_to_trend_items.append({
                    'Worksheet': worksheet,
                    'Stored Signals': signals_to_trend,
                    'Calculated Signals': calculated_signals_to_trend,
                })
                if influxdb:
                    for results in signals_to_trend:
                        if not results.empty:
                            results['Asset'] = nan
                            results['Path'] = nan
                            results['Formula'] = '$s'
                            results['Formula Parameters'] = [{'$s': results['ID'].iloc[0]}]
                            results['Type'] = 'CalculatedSignal'
                            results.set_index('Name', inplace=True, drop=False)
                            results.drop(columns=['ID', 'Datasource Name', 'Archived'], inplace=True)
                            calculated_signals_to_push.append(results)
                calculated_signals_to_push.extend(calculated_signals_to_trend)

    signals_to_push = pd.concat(calculated_signals_to_push, ignore_index=True, copy=False).drop_duplicates(
        subset=['Name'])
    pushed_signals = push_calculated_signals(signals_to_push, workbook.id, '{All datasource worksheets}')
    for ws_and_items in worksheets_to_trend_items:
        worksheet = ws_and_items['Worksheet']
        stored_signals = merge_push_results(ws_and_items['Stored Signals'], pushed_signals)
        calculated_signals = merge_push_results(ws_and_items['Calculated Signals'], pushed_signals)

        all_signals = pd.concat(stored_signals + calculated_signals, ignore_index=True)
        all_signals['Type'] = 'Signal'
        set_worksheet_display_items(worksheet, all_signals)


def push_workbook(workbook: Analysis,
                  workbook_name: str) -> None:
    print(f'Creating Workbook {workbook_name}.')
    start = time.time()
    url = spy.workbooks.push(
        workbook,
        path=CUSTOMER_MONITORS_FOLDER_ID,
        datasource=DATASOURCE,
        refresh=False,
        quiet=True
    )['URL'][0]
    print(f'Finished creating workbook {workbook_name} in {int((time.time() - start) * 1000)} millis.\n'
          f'Go to {url} to access the workbook.')
    spy.acl.push(workbook.id, {
        'ID': SEEQ_PERSONNEL_USER_GROUP_GUID,
        'Read': True,
        'Write': True,
        'Manage': True,
    }, replace=True, disable_inheritance=False, quiet=True)
    print(f'Gave access for {workbook_name} to Seeq Personnel.')


def build_path_str(*path_lists):
    return ' >> '.join(itertools.chain(*path_lists))


def build_name_str(path, name):
    return '.'.join([*path, name])


def variable_digest(data: str, length: int):
    h = shake_128()
    h.update(data.encode())
    return h.hexdigest(length)


def storage_load(key: str, expiration=24 * 60 * 60):
    try:
        file = f".{key}.pickle"
        last_modified = os.path.getmtime(file)
        if time.time() - expiration <= last_modified:
            with open(file, 'rb') as handle:
                return pickle.load(handle)
        return None
    except:
        return None


def storage_dump(key: str, data):
    try:
        with open(f".{key}.pickle", 'wb') as handle:
            return pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    except:
        pass


def get_asset_tree_signals(session: spy.Session, path: str, root_id: Optional[str] = None,
                           use_cache: bool = True) -> pd.DataFrame:
    print(f"Started retrieving Signals in Asset Tree: {path}")
    start = time.time()
    file_name = f"tree_{path.replace('>', '_').replace(' ', '')}"
    tree = storage_load(file_name) if use_cache else None
    if tree is not None:
        print(f"Finished retrieving {len(tree)} Signals from Asset Tree cache {file_name}")
        return tree
    # Calling SPy Search with only Path (no Type or other options), means it'll use the TreesApi traversal.
    # This is more efficient for this case since we know the tree is limited in scope and mostly contains signals.
    # As a bonus, it also avoids the CRAB-33245 bug.
    tree = spy.search({'Asset': root_id} if root_id else {'Path': path},
                      workbook=EMPTY_GUID,
                      session=session,
                      errors='catalog',
                      quiet=True,
                      recursive=True,
                      all_properties=False)
    if tree.empty:
        raise RuntimeError(f"Couldn't find a tree for {path}. Arguments --customer and/or --fqdn are likely incorrect.")

    tree = tree[tree['Type'].str.contains("Signal") & tree['Path'].str.contains(path)]
    storage_dump(file_name, tree)
    print(f"Finished retrieving {len(tree)} Signals from Asset Tree in {int((time.time() - start) * 1000)} millis")
    return tree


def main(
        url: str,
        user: str,
        access_key: str,
        password: str,
        customer: str,
        server: str,
        fqdn: str,
        workbook_name: str,
        overwrite: bool,
        monitoring: str,
        root_id: Optional[str] = None,
        use_cache: bool = True,
        influxdb: bool = True,
) -> None:
    if monitoring not in ['sh', 'ds', 'both']:
        raise 'Provide one of the following for -m flag "ds" for datasources, "sh" for system health or "both"'

    start = time.time()
    spy.options.allow_version_mismatch = True
    spy.login(url=url, access_key=access_key, username=user, password=password, ignore_ssl_errors=True, quiet=True)
    print("Logged in successfully")
    today = date.today()
    fqdn = fqdn if fqdn else server
    two_weeks_ago = today - datetime.timedelta(days=14)
    workbook_name = workbook_name if workbook_name else f'Monitoring {customer} - {fqdn}'
    worksheet_name = list(monitor_group_definitions(server, influxdb).keys())[0]

    subroot_path = f"{ROOT_NODE['influxdb' if influxdb else 'legacy']} >> {customer} >> {fqdn}"
    signal_metadata = get_asset_tree_signals(spy.session, subroot_path, root_id, use_cache)

    if monitoring == 'sh' or monitoring == 'both':
        workbook_df = spy.search({'Name': workbook_name, 'Type': 'Workbook'}, quiet=True)
        workbook_df.sort_values('ID')
        if not workbook_df.empty and not overwrite:
            print(
                f'{workbook_name} already exists and -o/--overwrite is false. Please set -o/--overwrite to true if you '
                f'would like to overwrite the existing monitoring workbook.')
            return

        if len(workbook_df) > 0:
            workbook = spy.workbooks.Analysis({'Name': workbook_name, 'ID': workbook_df['ID'][0]})
        else:
            workbook = spy.workbooks.Analysis({'Name': workbook_name})
            workbook.worksheet(worksheet_name)
            spy.workbooks.push(workbook, quiet=True)

        try:
            create_regular_monitor_worksheets(workbook, signal_metadata, two_weeks_ago, today, server, influxdb)
        except Exception as e:
            raise Exception(f'Encountered error while building workbook {workbook_name}. No workbook was built') from e
        push_workbook(workbook, workbook_name)

    if monitoring == 'ds' or monitoring == 'both':
        datasource_workbook_name = workbook_name + DATASOURCES_WORKBOOK_SUFFIX
        workbook_df = spy.search({'Name': datasource_workbook_name, 'Type': 'Workbook'}, quiet=True)
        workbook_df.sort_values('ID')
        if len(workbook_df) > 0:
            workbook_datasources = spy.workbooks.Analysis(
                {'Name': datasource_workbook_name, 'ID': workbook_df['ID'][0]})
        else:
            workbook_datasources = spy.workbooks.Analysis({'Name': datasource_workbook_name})
            workbook_datasources.worksheet(worksheet_name)
            spy.workbooks.push(workbook_datasources, quiet=True)

        try:
            create_datasource_monitor_worksheets(workbook_datasources, signal_metadata, two_weeks_ago, today,
                                                 customer, fqdn, influxdb)
        except BaseException as e:
            raise Exception(f'Encountered error while building workbook {datasource_workbook_name}.\n'
                            f'No workbook was built.') from e
        push_workbook(workbook_datasources, datasource_workbook_name)
    print(f'Script completed in {int((time.time() - start) * 1000)} millis.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", required=False, help="User name to log in with")
    parser.add_argument("-p", "--password", required=False, help="Password name to log in with")
    parser.add_argument("-k", "--access_key", required=False, help="Access key to log in with")
    parser.add_argument("-c", "--customer", required=True, help="Customer name for which to build monitoring workbook")
    parser.add_argument("-s", "--server", required=True, help="Customer server name for which to build monitoring "
                                                              "workbook (e.g. xyz-main-p) - case-sensitive")
    parser.add_argument("-f", "--fqdn", required=False,
                        help="Specify a fully-qualified domain name (e.g. xyz.seeq.site) if different from server "
                             "name (xyz-main-p) - case-insensitive, defaults to -s|--server")
    parser.add_argument("-w", "--workbook_name", required=False, help="The name for the monitoring workbook")
    parser.add_argument("-o", "--overwrite", required=False, action='store_true', default=True,
                        help="Overwrite the monitoring workbook if the name already exists")
    parser.add_argument("-m", "--monitoring", default="both", required=False,
                        choices=['sh', 'ds', 'both'],
                        help="Create system health (\"sh\"), datasource (\"ds\") or workbooks monitoring both ("
                             "\"both\").")
    parser.add_argument("-r", "--root_guid", required=False,
                        help="GUID of the Customer Root Asset - useful for cases when there are more than one folder "
                             "with the same name (due to a bad configuration or errors on the monitor ingestion "
                             "proces).")
    parser.add_argument("-n", "--no_cache", required=False, action='store_true',
                        help="Use local cache for the asset tree")
    parser.add_argument("-i", "--influxdb", required=False, action='store_true', default=True,
                        help="Use the new InfluxDB monitors or the legacy File-based monitors")

    args = parser.parse_args()
    main(MONITORS_URL, args.user, args.access_key, args.password, args.customer, args.server, args.fqdn,
         args.workbook_name, args.overwrite, args.monitoring, args.root_guid, not args.no_cache, args.influxdb)


def test_build_path_str():
    assert build_path_str(
        ['Path component 1', 'two'], ['More', 'paths', 'Here'], ['and']
    ) == 'Path component 1 >> two >> More >> paths >> Here >> and'


def test_build_name_str():
    assert build_name_str(
        ['Path component 1', 'two'], 'three'
    ) == 'Path component 1.two.three'
