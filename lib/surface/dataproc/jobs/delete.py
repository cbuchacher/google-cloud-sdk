# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Delete job command."""

from googlecloudsdk.api_lib.dataproc import util
from googlecloudsdk.calliope import base
from googlecloudsdk.calliope import exceptions
from googlecloudsdk.core import log
from googlecloudsdk.core.console import console_io


class Delete(base.Command):
  """Delete the record of an inactive job."""

  detailed_help = {
      'DESCRIPTION': '{description}',
      'EXAMPLES': """\
          To delete the record of a job, run:

            $ {command} job_id
          """,
  }

  @staticmethod
  def Args(parser):
    parser.add_argument(
        'id',
        metavar='JOB_ID',
        help='The ID of the job to delete.')

  @util.HandleHttpError
  def Run(self, args):
    client = self.context['dataproc_client']
    messages = self.context['dataproc_messages']

    job_ref = util.ParseJob(args.id, self.context)
    request = messages.DataprocProjectsJobsDeleteRequest(
        projectId=job_ref.projectId,
        jobId=job_ref.jobId)

    if not console_io.PromptContinue(
        message="The job '{0}' will be deleted.".format(args.id)):
      raise exceptions.ToolException('Deletion aborted by user.')

    client.projects_jobs.Delete(request)
    util.WaitForResourceDeletion(
        client.projects_jobs.Get, job_ref, message='Waiting for job deletion')

    log.DeletedResource(job_ref)