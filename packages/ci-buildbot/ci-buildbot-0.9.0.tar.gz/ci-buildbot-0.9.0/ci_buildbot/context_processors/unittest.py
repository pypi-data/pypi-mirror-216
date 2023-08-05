from typing import Optional

from ..typedefs import MessageContext
from .base import AbstractContextProcessor


class UnittestReportGroupProcessor(AbstractContextProcessor):
    """
    Adds the following keys to the context:

    * ``report_group``: the name of the CodeBuild report group that contains the
        unit test results for this pipeline run.
    * ``report_group_url``: the URL to the CodeBuild report group that contains
        the unit test results for this pipeline run.

    .. important::
        This needs to come before
        :py:class:`ci_buildbot.context_processors.codebuild.CodebuildProcessor``
        in the processor list, because it depends on things that that processor
        discovers.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.report_group: Optional[str] = kwargs['report_group']

    def get_reports_url(self, context: MessageContext) -> None:
        # https://us-west-2.console.aws.amazon.com/codesuite/codebuild/467892444047/testReports/reportGroups/tcc-unittests-Unittests-Unittests?region=us-west-2
        context['report_group_url'] = f"<https://{context['region']}.console.aws.amazon.com/codesuite/codebuild/{context['account_id']}/testReports/reportGroups/{self.report_group}?region={context['region']}|{context['report_group']}>"

    def annotate(self, context: MessageContext) -> None:
        context['report_group'] = self.report_group
        self.get_reports_url(context)
