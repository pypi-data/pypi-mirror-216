#  Copyright (c) 2023 Roboto Technologies, Inc.

from ..domain.actions import ActionDelegate
from ..domain.datasets import DatasetDelegate
from ..domain.orgs import OrgDelegate
from ..domain.tokens import TokenDelegate
from ..domain.triggers import TriggerDelegate
from ..http import HttpClient


class CLIContext:
    _http: HttpClient | None
    datasets: DatasetDelegate
    orgs: OrgDelegate
    tokens: TokenDelegate
    triggers: TriggerDelegate
    actions: ActionDelegate

    @property
    def http(self) -> HttpClient:
        # Necessary since http is lazy set after parsing args
        if self._http is None:
            raise ValueError("Unset HTTP client!")

        return self._http

    @http.setter
    def http(self, http: HttpClient) -> None:
        self._http = http
