class ApiDaviErro(Exception):
    ...

class ProposalAlreadyAssignedError(Exception):
    ...


class ProposalNotOnExpectedStatusError(Exception):
    ...


class ImportFailedDueToStormServiceError(Exception):
    def __init__(self, error_json):
        self.error_json = error_json