# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Implements Context functionality."""

import _utils


class Context(object):
  """Maintains contextual state for connecting to Cloud APIs.
  """

  _global_context = None

  def __init__(self, project_id, credentials):
    """Initializes an instance of a Context object.

    Args:
      project_id: the current cloud project.
      credentials: the credentials to use to authorize requests.
    """
    if project_id is None:
      if Context._global_context:
        project_id = Context._global_context._project_id
      else:
        raise Exception('Cannot create Context with no project_id. ' +
                        'Please use set_project_id to set a default project.')
    self._project_id = project_id
    self._credentials = credentials

  @property
  def credentials(self):
    """Retrieves the value of the credentials property.

    Returns:
      The current credentials used in authorizing API requests.
    """
    return self._credentials

  @property
  def project_id(self):
    """Retrieves the value of the project_id property.

    Returns:
      The current project id to associate with API requests.
    """
    return self._project_id

  @staticmethod
  def default(project_id=None, credentials=None):
    """Retrieves a default Context object, creating it if necessary.

      The default Context is a global shared instance used every time the default context is
      retrieved.

      Attempting to use a Context with no project_id will raise an exception.

      If the context already exists and either or both of the arguments are not None, they
      will update the default context with the new values.

    Args:
      project_id: The project ID to use for the default context.
      credentials: The credentials to use for the default Context. If not supplied an attempt
          will be made to create them from gcloud credentials.

    Returns:
      An initialized and shared instance of a Context object.
    """

    if Context._global_context is None:
      if credentials is None:
        credentials = _utils.get_credentials()

      Context._global_context = Context(project_id, credentials)
    else:
      if project_id is not None:
        Context._global_context._project_id = project_id
      if credentials is not None:
        Context._global_context._credentials = credentials

    return Context._global_context
