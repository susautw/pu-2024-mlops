class DomainError(Exception):
    """
    Exception raised for errors in the domain.
    """


class RepoError(DomainError):
    """
    Exception raised for errors in the repositories.
    """


class RepoCreateError(RepoError):
    """
    Exception raised for errors in the creation of a repository.
    """


class RepoUpdateError(RepoError):
    """
    Exception raised for errors in the update of a repository.
    """
