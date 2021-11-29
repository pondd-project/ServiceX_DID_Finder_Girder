from typing import Any, AsyncGenerator, Dict
from servicex_did_finder_lib import start_did_finder
import logging
import requests

__log = logging.getLogger(__name__)

async def girder_did_finder(did_name: str, 
                            info: Dict[str, Any]
                            ) -> AsyncGenerator[Dict[str, Any], None]:
    __log.info('DID Lookup request for collection {did_name}'.format(did_name=did_name),
               extra = {"requestId": info['request-id']})

    root_url = "https://girder.hub.yt/api/v1/"
    response = requests.get(root_url + "folder?parentType=collection&parentId={did_name}".format(
            did_name=did_name))


    if len(response.json()) == 0:
        # download collection if folders not found
        __log.info('No folders found with parentId: {did_name}!'.format(did_name=did_name))
        yield {
            'file_path': root_url + 'collection/{coll_id}/download'.format(
                coll_id=did_name),
            'adler32': 0,
            'file_size': 0,
            'file_events': 0,
            }
            
    # if folders found, iterate and yield download uri for each folder
    for folder in response.json():
        yield {
            'file_path': root_url + 'folder/{folder_id}/download'.format(folder_id=folder['_id']),
            'adler32': 0,
            'file_size': 0,
            'file_events': 0,
            }

def run_girder_did_finder():
    log = logging.getLogger(__name__)

    try:
        log.info('Starting girder DID finder')
        start_did_finder('girder', girder_did_finder)
    finally:
        log.info('Done running girder DID finder')

if __name__ == "__main__":
    run_girder_did_finder()
