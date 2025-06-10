from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase): ...


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Mapped[str]

    tasks: Mapped[list["TrainingTask"]] = relationship(
        "TrainingTask", back_populates="user"
    )


class TrainingTask(Base):
    __tablename__ = "training_tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))

    name: Mapped[str]
    base_dir: Mapped[str]
    input_dir: Mapped[str]
    task_type: Mapped[str]  # required worker type
    version: Mapped[str]  # required worker version
    created_at: Mapped[datetime]  # ISO format datetime string
    updated_at: Mapped[datetime]  # ISO format datetime string

    user: Mapped[User] = relationship(User, back_populates="tasks")
    statuses: Mapped[list["TrainingStatus"]] = relationship(
        "TrainingStatus", back_populates="task"
    )


class TrainingStatus(Base):
    __tablename__ = "training_status"
    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey(TrainingTask.id))
    phase: Mapped[str]
    progress: Mapped[float]  # 0.0 to 1.0
    description: Mapped[str]  # Optional description of the status
    is_completed: Mapped[bool]  # True if the task is completed

    task: Mapped[TrainingTask] = relationship(TrainingTask, back_populates="statuses")
