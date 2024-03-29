from enum import Enum


class MessageConstants(Enum):
    """Standard message constants"""

    NO_DM = "You can't use this command in private messages or DMs"
    TIMEOUT = "You took too long. Goodbye."
    NO_JOB = "You either don't own this job or the job doesn't exist. Try again."
    NO_REASON = "No reason provided"
    NO_PERM_JOB = (
        "Either you don't own any jobs or you have no permission to delete those jobs"
    )
    NO_HELP_FOUND = "No help found..."
    NO_COMMENTS = "This issue has no comments"
    NO_ASSIGNEES = "This issue has no assignees"
    NO_CONTROL_VIEW = "You can't control this view!"
    BLACKLIST_APPEAL_MSG = "You are blacklisted from using this bot. Take an \U0001f1f1, \U0001f1f1oser. [Here's how to appeal the blacklist.](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
