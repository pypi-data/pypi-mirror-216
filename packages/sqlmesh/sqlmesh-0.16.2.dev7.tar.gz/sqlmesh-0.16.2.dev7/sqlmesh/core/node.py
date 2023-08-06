from __future__ import annotations

import abc
import typing as t
from enum import Enum

from croniter import croniter

from sqlmesh.utils.date import TimeLike, preserve_time_like_kind, to_datetime
from sqlmesh.utils.pydantic import PydanticModel

class IntervalUnit(str, Enum):
    """IntervalUnit is the inferred granularity of an incremental model.

    IntervalUnit can be one of 4 types, DAY, HOUR, MINUTE. The unit is inferred
    based on the cron schedule of a model. The minimum time delta between a sample set of dates
    is used to determine which unit a model's schedule is.
    """

    DAY = "day"
    HOUR = "hour"
    MINUTE = "minute"

class Node(PydanticModel):
    """
    Args:
        start: The earliest date that the model will be backfilled for. If this is None,
            then the date is inferred by taking the most recent start date of its ancestors.
            The start date can be a static datetime or a relative datetime like "1 year ago"
    """
    _croniter: t.Optional[croniter] = None
    _interval_unit: t.Optional[IntervalUnit] = None
    
    #lookback: int
    start: t.Optional[TimeLike]

    @property
    def batch_size(self) -> t.Optional[int]:
        """The maximal number of units in a single task for a backfill."""
        return None

    def interval_unit(self, sample_size: int = 10) -> IntervalUnit:
        """Returns the IntervalUnit of the model

        The interval unit is used to determine the lag applied to start_date and end_date for model rendering and intervals.

        Args:
            sample_size: The number of samples to take from the cron to infer the unit.

        Returns:
            The IntervalUnit enum.
        """
        if not self._interval_unit:
            schedule = croniter(self.cron)
            samples = [schedule.get_next() for _ in range(sample_size)]
            min_interval = min(b - a for a, b in zip(samples, samples[1:]))
            if min_interval >= 86400:
                self._interval_unit = IntervalUnit.DAY
            elif min_interval >= 3600:
                self._interval_unit = IntervalUnit.HOUR
            else:
                self._interval_unit = IntervalUnit.MINUTE
        return self._interval_unit

    def normalized_cron(self) -> str:
        """Returns the UTC normalized cron based on sampling heuristics.

        SQLMesh supports 3 interval units, daily, hourly, and minutes. If a job is scheduled
        daily at 1PM, the actual intervals are shifted back to midnight UTC.

        Returns:
            The cron string representing either daily, hourly, or minutes.
        """
        unit = self.interval_unit()
        if unit == IntervalUnit.MINUTE:
            return "* * * * *"
        if unit == IntervalUnit.HOUR:
            return "0 * * * *"
        if unit == IntervalUnit.DAY:
            return "0 0 * * *"
        return ""

    def croniter(self, value: TimeLike) -> croniter:
        if self._croniter is None:
            self._croniter = croniter(self.normalized_cron())
        self._croniter.set_current(to_datetime(value))
        return self._croniter

    def cron_next(self, value: TimeLike) -> TimeLike:
        """
        Get the next timestamp given a time-like value and the model's cron.

        Args:
            value: A variety of date formats.

        Returns:
            The timestamp for the next run.
        """
        return preserve_time_like_kind(value, self.croniter(value).get_next())

    def cron_prev(self, value: TimeLike) -> TimeLike:
        """
        Get the previous timestamp given a time-like value and the model's cron.

        Args:
            value: A variety of date formats.

        Returns:
            The timestamp for the previous run.
        """
        return preserve_time_like_kind(value, self.croniter(value).get_prev())

    def cron_floor(self, value: TimeLike) -> TimeLike:
        """
        Get the floor timestamp given a time-like value and the model's cron.

        Args:
            value: A variety of date formats.

        Returns:
            The timestamp floor.
        """
        return preserve_time_like_kind(value, self.croniter(self.cron_next(value)).get_prev())


