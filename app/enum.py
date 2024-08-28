import enum


class TaskStatus(str, enum.Enum):
    IN_QUEUE = 'In Queue'
    RUN = 'Run'
    COMPLETED = 'Completed'
