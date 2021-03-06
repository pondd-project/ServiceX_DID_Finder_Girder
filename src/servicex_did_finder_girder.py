# Copyright (c) 2021, University of Illinois/NCSA
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from typing import Any, AsyncGenerator, Dict
from servicex_did_finder_lib import start_did_finder
import logging
import requests

__log = logging.getLogger(__name__)


async def girder_did_finder(did_name: str,
                            info: Dict[str, Any]
                            ) -> AsyncGenerator[Dict[str, Any], None]:
    __log.info('DID Lookup request for collection {did_name}'.format(did_name=did_name),
               extra={"requestId": info['request-id']})

    root_url = "https://girder.hub.yt/api/v1/"
    check_did = did_name.split('#')
    if len(check_did) == 1:
        raise Exception(
            'Must specify data type by appending #item, #folder, or #collection to your dataset id!')
    else:
        did, did_type = did_name.split('#')
        # check for valid
        if did_type not in ['item', 'folder', 'collection']:
            raise Exception(
                'Incorrect data type specified: {did_type}. Allowed data types are item, folder and collection.'.format(
                    did_type=did_type))
    try:
        if did_type == "collection":
            # try downloading as collection
            response = requests.get(root_url + "folder?parentType=collection&parentId={did}".format(
                    did=did))

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
            else:
                # if folders found in collection, iterate and yield download uri for each folder
                for folder in response.json():
                    yield {
                        'file_path': root_url + 'folder/{folder_id}/download'.format(folder_id=folder['_id']),
                        'adler32': 0,
                        'file_size': 0,
                        'file_events': 0,
                    }
        if did_type == "folder":
            yield {
                'file_path': root_url + 'folder/{folder_id}/download'.format(folder_id=did),
                'adler32': 0,
                'file_size': 0,
                'file_events': 0,
            }
        if did_type == "item":
            yield {
                'file_path': root_url + 'item/{item_id}/download'.format(item_id=did),
                'adler32': 0,
                'file_size': 0,
                'file_events': 0,
            }
    except Exception as e:
        __log.info('Could not find dataset with id: {did_name}'.format(did_name=did_name))
        __log.info('Error msg: {e}'.format(e=e))


def run_girder_did_finder():
    log = logging.getLogger(__name__)

    try:
        log.info('Starting girder DID finder')
        start_did_finder('girder', girder_did_finder)
    finally:
        log.info('Done running girder DID finder')


if __name__ == "__main__":
    run_girder_did_finder()
