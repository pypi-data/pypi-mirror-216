# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from google.cloud.datastore import Client

from cbra.core.conf import settings
from cbra.core.ioc import Container
from .environ import GOOGLE_DATASTORE_NAMESPACE
from .environ import GOOGLE_SERVICE_PROJECT


__all__: list[str] = ['setup']


def setup(container: Container) -> None:
    if GOOGLE_SERVICE_PROJECT and GOOGLE_DATASTORE_NAMESPACE:
        container.inject(
            'GoogleDatastoreClient',
            Client(project=GOOGLE_SERVICE_PROJECT, namespace=GOOGLE_DATASTORE_NAMESPACE)
        )
        container.provide('CredentialRepository', {
            'qualname': (
                settings.CREDENTIALS_REPOSITORY or
                'cbra.ext.google.impl.credentials.DatastoreCredentialRepository'
            )
        })
        container.provide('SubjectResolver', {
            'qualname': 'cbra.ext.google.DatastoreSubjectResolver'
        })
        container.provide('SubjectRepository', {
            'qualname': 'cbra.ext.google.DatastoreSubjectRepository'
        })