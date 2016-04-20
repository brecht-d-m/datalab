# Copyright 2016 Google Inc. All rights reserved.
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

""" Support for getting gcloud credentials. """

import argparse
import oauth2client.client
import oauth2client.file
import oauth2client.tools
import json
import os


def get_config_dir():
  config_dir = os.getenv('CLOUDSDK_CONFIG')
  if config_dir is None:
    if os.name == 'nt':
      try:
        config_dir = os.path.join(os.environ['APPDATA'], 'gcloud')
      except KeyError:
        # This should never happen unless someone is really messing with things.
        drive = os.environ.get('SystemDrive', 'C:')
        config_dir = os.path.join(drive, '\\gcloud')
    else:
      config_dir = os.path.join(os.path.expanduser('~'), '.config/gcloud')
  return config_dir


def get_credentials():
  """ Get the credentials to use. We try application credentials first, followed by
      user credentials. If neither of these exist we will do an auth flow provided we are
      not running inside Docker. The path to the application credentials can be overridden
      by pointing the GOOGLE_APPLICATION_CREDENTIALS environment variable to some file;
      the path to the user credentials can be overridden by pointing the CLOUDSDK_CONFIG
      environment variable to some directory (after which we will look for the file
      $CLOUDSDK_CONFIG/gcloud/credentials). Unless you have specific reasons for
      overriding these the defaults should suffice.
  """
  try:
    credentials = oauth2client.client.GoogleCredentials.get_application_default()
  except Exception as e:

    # Try load user creds from file
    cred_file = get_config_dir() + '/credentials'
    if cred_file is not None and os.path.exists(cred_file):
      with open(cred_file) as f:
        creds= json.loads(f.read())
      # Use the first gcloud one we find
      for entry in creds['data']:
        if entry['key']['type'] == 'google-cloud-sdk':
          return oauth2client.client.OAuth2Credentials.from_json(json.dumps(entry['credential']))

    if os.path.exists('/.dockerinit*'):
      # Inside Docker; nothing more we can do.
      raise e
    else:
      # Try do an auth flow.
      flow = oauth2client.client.OAuth2WebServerFlow(
          client_id='32555940559.apps.googleusercontent.com',
          client_secret='ZmssLNjJy2998hD4CTg2ejr2',
          scope=[
              'https://www.googleapis.com/auth/userinfo.email',
              'https://www.googleapis.com/auth/cloud-platform',
          ],
          redirect_uri='http://localhost:8080/oauthcallback')
      storage = oauth2client.file.Storage(cred_file)
      parser = argparse.ArgumentParser(parents=[oauth2client.tools.argparser])
      flags = parser.parse_args()
      credentials = oauth2client.tools.run_flow(flow, storage, flags)

  return credentials
