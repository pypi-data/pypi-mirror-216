from dataclasses import dataclass
from typing import List

import pandas as pd

from pix_framework.calendar.availability import absolute_unavailability_intervals_within
from pix_framework.calendar.resource_calendar import RCalendar
from pix_framework.discovery.resource_profiles import ResourceProfile
from pix_framework.log_ids import EventLogIDs
from pix_framework.statistics.distribution import get_best_fitting_distribution


@dataclass
class ResourceDistribution:
    """Resource is the item of activity-resource duration distribution for Prosimos."""

    resource_id: str
    distribution: dict

    def to_dict(self) -> dict:
        """Dictionary with the structure compatible with Prosimos:"""
        return {"resource_id": self.resource_id} | self.distribution

    @staticmethod
    def from_dict(resource_distribution: dict) -> "ResourceDistribution":
        return ResourceDistribution(
            resource_id=resource_distribution["resource_id"],
            distribution={key: resource_distribution[key] for key in resource_distribution if key != "resource_id"},
        )


@dataclass
class ActivityResourceDistribution:
    """Activity duration distribution per resource for Prosimos."""

    activity_id: str
    activity_resources_distributions: List[ResourceDistribution]

    def to_dict(self) -> dict:
        """Dictionary with the structure compatible with Prosimos:"""
        return {
            "task_id": self.activity_id,
            "resources": [resource.to_dict() for resource in self.activity_resources_distributions],
        }

    @staticmethod
    def from_dict(activity_resource_distribution: dict) -> "ActivityResourceDistribution":
        return ActivityResourceDistribution(
            activity_id=activity_resource_distribution["task_id"],
            activity_resources_distributions=[
                ResourceDistribution.from_dict(resource_distribution)
                for resource_distribution in activity_resource_distribution["resources"]
            ],
        )


def discover_activity_resource_distribution(
    event_log: pd.DataFrame,
    log_ids: EventLogIDs,
    resource_profiles: List[ResourceProfile],
    resource_calendars: List[RCalendar],
) -> List[ActivityResourceDistribution]:
    """
    Discover the performance (activity duration) for each resource profile in [resource_profiles]. Treats
    each resource profile as a pool with shared performance (i.e., all the resources of a profile will
    have the same performance for an activity A, computed with the durations of the executions of A performed
    by any resource in that profile).

    :param event_log: event log to discover the activity durations from.
    :param log_ids: column IDs of the event log.
    :param resource_profiles: list of resource profiles with their ID and resources.
    :param resource_calendars: list of calendars containing their ID and working intervals.

    :return: list of duration distribution per activity and resource.
    """
    # Go over each resource profile, computing the corresponding activity durations
    activity_resource_distributions = []
    for resource_profile in resource_profiles:
        assert (
                len(resource_profile.resources) > 0
        ), "Trying to compute activity performance of an empty resource profile."
        # Get the calendar of the resource profile
        calendar_id = resource_profile.resources[0].calendar_id
        calendar = next(calendar for calendar in resource_calendars if calendar.calendar_id == calendar_id)
        # Get the list of resources of this profile and the activities assigned to them
        resources = [resource.id for resource in resource_profile.resources]
        assigned_activities = resource_profile.resources[0].assigned_tasks
        # Filter the log with activities performed by them
        filtered_event_log = event_log[
            event_log[log_ids.activity].isin(assigned_activities) & event_log[log_ids.resource].isin(resources)
            ]
        # For each assigned activity
        for activity_label, events in filtered_event_log.groupby(log_ids.activity):
            # Get their durations
            durations = compute_activity_durations_without_off_duty(events, log_ids, calendar)
            # Compute duration distribution
            duration_distribution = get_best_fitting_distribution(durations).to_prosimos_distribution()
            # Create empty activity-resource distribution
            activity_resource_distribution = ActivityResourceDistribution(activity_label, [])
            # Append distribution to the durations of this activity (per resource)
            for resource in resources:
                activity_resource_distribution.activity_resources_distributions += [
                    ResourceDistribution(resource, duration_distribution)
                ]
            # Add resource distributions of this activity
            activity_resource_distributions += [activity_resource_distribution]
    # Return list of activity-resource performance
    return activity_resource_distributions


def compute_activity_durations_without_off_duty(
    events: pd.DataFrame,
    log_ids: EventLogIDs,
    calendar: RCalendar,
) -> List[float]:
    """
    Returns activity durations without off-duty time.
    """
    # Compute the calendar-aware duration of each event
    calendar_aware_durations = []
    for start, end in events[[log_ids.start_time, log_ids.end_time]].values.tolist():
        # Recover off-duty periods based on given calendar
        unavailable_periods = absolute_unavailability_intervals_within(
            start=start,
            end=end,
            schedule=calendar,
        )
        # Compute total off-duty duration
        unavailable_time = sum(
            [
                (unavailable_period.end - unavailable_period.start).total_seconds()
                for unavailable_period in unavailable_periods
            ]
        )
        # Compute raw duration and subtract off-duty periods
        calendar_aware_durations += [(end - start).total_seconds() - unavailable_time]
    # Return durations without off-duty time
    return calendar_aware_durations
