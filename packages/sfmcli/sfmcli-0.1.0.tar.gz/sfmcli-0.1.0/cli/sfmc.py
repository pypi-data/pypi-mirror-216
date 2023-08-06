from __future__ import annotations

import logging
import time
from datetime import datetime
from math import ceil
from multiprocessing import Pool

import requests

from cli.database import initialize_database
from cli.database import session
from cli.models import DataExtension
from cli.models import DataExtensionPage

log_format = '%(asctime)s:%(filename)s:%(levelname)s:%(message)s'

logging.basicConfig(
    filename='log.log',
    level=logging.INFO,
    format=log_format,
)

logger = logging.getLogger()

TOKENS: dict[str, dict] = {}


class Pipeline:
    def __init__(self, *funcs):
        self.funcs = funcs

    def __call__(self, data, arg1, arg2):
        state = data, arg1, arg2
        for func in self.funcs:
            state = func(*state)
        return state


def get_access_token(config):
    token = TOKENS.get(config['name'])
    current_timestamp = time.time()

    if token and current_timestamp < token['expires_at_timestamp']:
        return token['access_token']

    payload = {
        'grant_type': 'client_credentials',
        'client_id': config['client_id'],
        'client_secret': config['client_secret'],
        'account_id': config['mid'],
    }
    try:
        response = requests.post(
            f"https://{config['subdomain']}.auth.marketingcloudapis.com/v2/token", data=payload,  # noqa: E501
        ).json()
        TOKENS[config['name']] = {
            'access_token': response['access_token'],
            'expires_at_timestamp': time.time() + response['expires_in'],
        }

        return response['access_token']
    except requests.exceptions.RequestException as e:
        logger.critical(
            f"couldn't get access_token for {config}. exception {e}",
        )
        raise SystemExit(e)


def get_data_extensions_with_origin_info(config):
    data_extensions = list()
    response = requests.get(config['cloud_page_url']).json()

    for de in response:
        if session.query(DataExtension).filter_by(name=de['name']).first() is None:  # noqa: E501
            data_extension = DataExtension(
                name=de['name'],
                origin_external_key=de['external_key'],
                origin_instance=config['name'],
            )
            data_extensions.append(data_extension)

    session.add_all(data_extensions)
    session.commit()


def update_data_extensions_target_info(config):
    data_extensions = list()

    reponse = requests.get(config['cloud_page_url']).json()

    for de in reponse:
        data_extension = session.query(
            DataExtension,
        ).filter_by(name=de['name']).first()
        if data_extension is not None:
            data_extension.target_external_key = de['external_key']
            data_extension.target_instance = config['name']
            data_extensions.append(data_extension)

    session.add_all(data_extensions)
    session.commit()


def get_pages(data_extension, config):
    logger.info(f'getting pages for {data_extension}')
    page_size = 2500
    base_url = f"https://{config['subdomain']}.rest.marketingcloudapis.com/data/v1/customobjectdata/key/{data_extension.origin_external_key}/rowset?$pageSize={page_size}"  # noqa: E501

    try:
        headers = {'Authorization': f'Bearer {get_access_token(config)}'}
        response = requests.get(base_url, headers=headers).json()

        count = response['count']

        if not count > 0:
            logger.info(f'skipped {data_extension} because it has no items')
            return 0

        sample_record = response['items'][0]
        has_sfmc_key = len(sample_record.keys()) > 0

        data_extension_pages = list()

        for page in range(1, ceil(count / page_size) + 1):
            data_extension_page = session.query(DataExtensionPage).filter_by(
                url=f'{base_url}&$page={page}',
            ).first()
            if data_extension_page is None:
                data_extension_page = DataExtensionPage(
                    url=f'{base_url}&$page={page}',
                    data_extension_id=data_extension.id,
                    status='new',
                    has_sfmc_key=has_sfmc_key,
                )
                data_extension_pages.append(data_extension_page)

        session.add_all(data_extension_pages)
        session.commit()
    except Exception as e:
        logger.critical(
            f"couldn't get pages for {data_extension}. exception {e}",
        )


def get_page_items_and_append_target_data(data_extension_page, origin, target):
    logger.info(f'getting page items for {data_extension_page}')

    try:
        headers = {'Authorization': f'Bearer {get_access_token(origin)}'}
        response = requests.get(data_extension_page.url, headers=headers)
        items = response.json()['items']

        return (data_extension_page, [{**item['keys'], **item['values']} for item in items], target)  # noqa: E501
    except Exception as e:
        session.query(DataExtensionPage).filter(DataExtensionPage.id == data_extension_page.id).update(  # noqa: E501
            {'status': 'pending get_page_items_and_append_target_data'},
        )
        session.commit()
        logger.critical(
            f"couldn't get page items for {data_extension_page}. exception {e}",  # noqa: E501
        )


def create_page_items(data_extension_page, items, target):
    logger.info(f'creating items for {data_extension_page}')
    has_sfmc_key = data_extension_page.has_sfmc_key

    try:
        headers = {'Authorization': f'Bearer {get_access_token(target)}'}
        payload = {
            'items': items,
        }

        response = {}

        if has_sfmc_key:
            response = requests.put(
                f"https://{target['subdomain']}.rest.marketingcloudapis.com/data/v1/async/dataextensions/key:{data_extension_page.data_extension.target_external_key}/rows",  # noqa: E501
                headers=headers,
                json=payload,
            ).json()
            session.query(DataExtensionPage).filter(DataExtensionPage.id == data_extension_page.id).update(  # noqa: E501
                {'request_id': response['requestId'], 'status': 'processed'},
            )
            session.commit()
            return 0

        response = requests.put(
            f"https://{target['subdomain']}.rest.marketingcloudapis.com/data/v1/async/dataextensions/key:{data_extension_page.data_extension.target_external_key}/rows",  # noqa: E501
            headers=headers,
            json=payload,
        ).json()
        session.query(DataExtensionPage).filter(DataExtensionPage.id == data_extension_page.id).update(  # noqa: E501
            {'request_id': response['requestId'], 'status': 'processed'},
        )
        session.commit()
    except Exception as e:
        session.query(DataExtensionPage).filter(
            DataExtensionPage.id ==
            data_extension_page.id,
        ).update({'status': 'pending create_page_items'})
        session.commit()
        logger.critical(
            f"couldn't creat items for {data_extension_page}. exception {e}",
        )


def clean_data_extension(data_extension, target):
    try:
        headers = {
            'Content-Type': 'application/soap+xml; charset=UTF-8',
        }
        body = """<?xml version="1.0" encoding="UTF-8"?>
            <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                <s:Header>
                    <a:Action s:mustUnderstand="1">Perform</a:Action>
                    <a:To s:mustUnderstand="1">https://{subdomain}.soap.marketingcloudapis.com/Service.asmx</a:To>
                    <fueloauth xmlns="http://exacttarget.com">{access_token}</fueloauth>
                </s:Header>
                <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                    <PerformRequestMsg xmlns="http://exacttarget.com/wsdl/partnerAPI" xmlns:ns2="urn:fault.partner.exacttarget.com">
                        <Action>ClearData</Action>
                        <Definitions>
                            <Definition xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="DataExtension">
                                <CustomerKey>{external_key}</CustomerKey>
                            </Definition>
                        </Definitions>
                    </PerformRequestMsg>
                </s:Body>
        </s:Envelope>""".format(subdomain=target['subdomain'], access_token=get_access_token(target), external_key=data_extension['external_key'])
        logger.info('this process may take a while')

        response = requests.post(
            f"https://{target['subdomain']}.soap.marketingcloudapis.com/Service.asmx",
            headers=headers,
            data=body,
        )
        logger.info(response.content)
        return 0
    except Exception as e:
        logger.critical(
            f"couldn't clean data extension {data_extension}. exception {e}",
        )


def populate(origin, target):
    initialize_database()

    start_time = datetime.now()
    logger.info('start of populate')

    logger.info('getting data extensions with origin info')
    get_data_extensions_with_origin_info(origin)

    logger.info('updating data extensions with target info')
    update_data_extensions_target_info(target)

    pipeline = Pipeline(
        get_page_items_and_append_target_data, create_page_items,
    )

    logger.info('this process may take a while')

    with Pool() as pool:
        logger.info(
            'getting data extensions pages from origin with target info',
        )
        data_extensions = list(
            session.query(DataExtension).filter(
                DataExtension.origin_instance != None,
                DataExtension.target_instance != None,
            ),
        )
        data_extension_tupled = []

        for data_extension in data_extensions:
            data_extension_tupled.append((data_extension, origin))

        pool.starmap(get_pages, data_extension_tupled)

        logger.info('executing pipeline')
        data_extesion_pages = list(
            session.query(DataExtensionPage).filter_by(
                status='new',
            ).join(DataExtensionPage.data_extension),
        )
        data_extesion_pages_tupled = []

        for data_extesion_page in data_extesion_pages:
            data_extesion_pages_tupled.append(
                (data_extesion_page, origin, target),
            )

        pool.starmap(pipeline, data_extesion_pages_tupled)

    time_elapsed = datetime.now() - start_time
    logger.info(f'end of populate (hh:mm:ss.ms) {time_elapsed}')


def clean(target):
    start_time = datetime.now()
    logger.info('start of clean')

    data_extensions = requests.get(target['cloud_page_url']).json()
    data_extension_tupled = []
    for data_extension in data_extensions:
        data_extension_tupled.append((data_extension, target))

    with Pool() as pool:
        logger.info('cleaning all data extensions')
        pool.starmap(clean_data_extension, data_extension_tupled)

    time_elapsed = datetime.now() - start_time
    logger.info(f'end of clean (hh:mm:ss.ms) {time_elapsed}')
