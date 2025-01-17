#!/bin/sh
# Copyright 2015 Google Inc. All rights reserved.
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

# Releases the built docker image to the registry with the latest tag.


LOCAL_IMAGE=datalab
CLOUD_IMAGE=gcr.io/cloud-datalab/datalab:local

# Grant read permissions to all users on all objects added in the GCS bucket
# that holds docker image files by ACLing the bucket and setting the default
# for any new items added (only needed for public containers)
# gsutil -m acl ch -r -u AllUsers:R gs://artifacts.cloud-datalab.appspot.com

echo "Publishing $LOCAL_IMAGE to $CLOUD_IMAGE ..."
docker tag -f $LOCAL_IMAGE $CLOUD_IMAGE
gcloud docker push $CLOUD_IMAGE
