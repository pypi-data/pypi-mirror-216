from typing import List, Optional, Dict, Any
from typing import Union
from uuid import UUID
from datetime import datetime, timezone
from pydantic import BaseModel, Field, validator
from enum import Enum


class StreamPrefixEnum(str, Enum):
    event = "ev"
    attachment = "att"


class Location(BaseModel):
    lat: float = Field(..., ge=-90.0, le=90.0, title="Latitude in decimal degrees")
    lon: float = Field(..., ge=-180.0, le=360.0, title="Longitude in decimal degrees")
    alt: float = Field(0.0, title="Altitude in meters.")
    hdop: Optional[int] = None
    vdop: Optional[int] = None


class GundiBaseModel(BaseModel):
    gundi_id: Union[UUID, str] = Field(
        None,
        title="Gundi ID",
        description="A unique object ID generated by gundi.",
    )
    related_to: Optional[Union[UUID, str]] = Field(
        None,
        title="Related Object - Gundi ID",
        description="The Gundi ID of the related object",
    )
    owner: str = "na"
    data_provider_id: Optional[Union[UUID, str]] = Field(
        None,
        title="Provider ID",
        description="The unique ID of the Integration providing the data.",
    )
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        title="Annotations",
        description="A dictionary of extra data that will be passed to destination systems.",
    )


class Event(GundiBaseModel):
    source_id: Optional[Union[UUID, str]] = Field(
        None,
        title="Source ID",
        description="An unique Source ID generated by Gundi.",
    )
    external_source_id: Optional[str] = Field(
        "none",
        example="901870234",
        description="The manufacturer provided ID for the Source associated with this data (a.k.a. device).",
    )
    recorded_at: Optional[datetime] = Field(
        ...,
        title="Timestamp for the data, preferrably in ISO format.",
        example="2021-03-21 12:01:02-0700",
    )
    location: Location
    title: Optional[str] = Field(
        None,
        title="Event title",
        description="Human-friendly title for this Event",
    )
    event_type: Optional[str] = Field(
        None, title="Event Type",
        description="Identifies the type of this Event"
    )

    event_details: Optional[Dict[str, Any]] = Field(
        None,
        title="Event Details",
        description="A dictionary containing details of this GeoEvent.",
    )
    geometry: Optional[Dict[str, Any]] = Field(
        None,
        title="Event Geometry",
        description="A dictionary containing details of this GeoEvent geoJSON.",
    )
    observation_type: str = Field(StreamPrefixEnum.event.value, const=True)

    @validator("recorded_at", allow_reuse=True)
    def clean_recorded_at(cls, val):

        if not val.tzinfo:
            val = val.replace(tzinfo=timezone.utc)
        return val


class Attachment(GundiBaseModel):
    source_id: Optional[Union[UUID, str]] = Field(
        None,
        title="Source ID",
        description="An unique Source ID generated by Gundi.",
    )
    external_source_id: Optional[str] = Field(
        "none",
        example="901870234",
        description="The manufacturer provided ID for the Source associated with this data (a.k.a. device).",
    )
    file_path: str
    observation_type: str = Field(StreamPrefixEnum.attachment.value, const=True)
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        title="Annotations",
        description="A dictionary of extra data that will be passed to destination systems.",
    )


class Organization(BaseModel):
    id: Union[UUID, str] = Field(
        None,
        title="Organization ID",
        description="Id of the organization owning the connection",
    )
    name: Optional[str] = Field(
        "",
        example="Wild Conservation Organization X",
        description="Name of the organization owning this connection",
    )
    description: Optional[str] = Field(
        "",
        example="An organization in X dedicated to protect YZ..",
        description="Description of the organization owning this connection",
    )


class ConnectionIntegration(BaseModel):
    id: Union[UUID, str] = Field(
        None,
        title="Integration ID",
        description="Id of an integration associated to the connection",
    )
    name: Optional[str] = Field(
        "",
        example="X Data Provider for Y Reserve",
        description="Connection name (Data Provider)",
    )
    type: Optional[str] = Field(
        "",
        example="earth_ranger",
        description="natural key of an integration type",
    )
    base_url: Optional[str] = Field(
        "",
        example="https://easterisland.pamdas.org/",
        description="Base URL of the third party system associated with this integration.",
    )
    status: Optional[str] = Field(
        "unknown",
        example="healthy",
        description="Computed status representing if the integration is working properly or not",
    )


class ConnectionRoute(BaseModel):
    id: Union[UUID, str] = Field(
        None,
        title="Route ID",
        description="Id of a route associated to the connection",
    )
    name: Optional[str] = Field(
        "",
        example="X Animal collars to Y",
        description="Route name",
    )


class Connection(BaseModel):
    id: Union[UUID, str] = Field(
        None,
        title="Connection ID",
        description="Id of the connection",
    )
    provider: ConnectionIntegration
    destinations: Optional[List[ConnectionIntegration]]
    routing_rules: Optional[List[ConnectionRoute]]
    default_route: Optional[ConnectionRoute]
    owner: Optional[Organization]
    status: Optional[str] = Field(
        "unknown",
        example="healthy",
        description="Aggregate status representing if the connection is working properly or not",
    )


class RouteConfiguration(BaseModel):
    id: Union[UUID, str] = Field(
        None,
        title="Route Configuration ID",
        description="Id of the configuration associated with the route",
    )
    name: Optional[str] = Field(
        "",
        example="Event Type Mappings",
        description="A descriptive name for the configuration",
    )
    data: Optional[Dict[str, Any]] = {}


class Route(BaseModel):
    id: Union[UUID, str] = Field(
        None,
        title="Route ID",
        description="Id of the route",
    )
    name: Optional[str] = Field(
        "",
        example="X Route for Y",
        description="Route name",
    )
    owner: Optional[Union[UUID, str]]
    data_providers: Optional[List[ConnectionIntegration]]
    destinations: Optional[List[ConnectionIntegration]]
    configuration: Optional[RouteConfiguration]
    additional: Optional[Dict[str, Any]] = {}


class IntegrationAction(BaseModel):
    id: Union[UUID, str] = Field(
        None,
        title="Integration Action ID",
        description="Id of an integration in Gundi",
    )
    type: Optional[str] = Field(
        "",
        example="pull",
        description="Free text to allow grouping and filtering actions",
    )
    name: Optional[str] = Field(
        "",
        example="Pull Events",
        description="A human-readable name for the action",
    )
    value: Optional[str] = Field(
        "",
        example="pull_events",
        description="Short text id for the action, to be used programmatically",
    )
    description: Optional[str] = Field(
        "",
        example="Pull Events from X system",
        description="Description of the action",
    )
    action_schema: Optional[Dict[str, Any]] = Field(
        {},
        alias="schema",
        example="{}",
        description="Schema definition of any configuration required for this action, in jsonschema format.",
    )


class IntegrationActionSummery(BaseModel):
    id: Union[UUID, str] = Field(
        None,
        title="Integration Action ID",
        description="Id of an integration in Gundi",
    )
    type: Optional[str] = Field(
        "",
        example="pull",
        description="Free text to allow grouping and filtering actions",
    )
    name: Optional[str] = Field(
        "",
        example="Pull Events",
        description="A human-readable name for the action",
    )
    value: Optional[str] = Field(
        "",
        example="pull_events",
        description="Short text id for the action, to be used programmatically",
    )


class IntegrationType(BaseModel):
    id: Union[UUID, str] = Field(
        None,
        title="Integration Type ID",
        description="Id of an integration in Gundi",
    )
    name: Optional[str] = Field(
        "",
        example="EarthRanger",
        description="Name of the third-party system or technology",
    )
    description: Optional[str] = Field(
        "",
        example="EarthRanger is a software solution for wildlife monitoring and protection in real-time.",
        description="Description of the third-party system or technology",
    )
    actions: Optional[List[IntegrationAction]]


class IntegrationActionConfiguration(BaseModel):
    id: Union[UUID, str] = Field(
        None,
        title="Configuration ID",
        description="Id of the configuration",
    )
    integration: Union[UUID, str] = Field(
        None,
        title="Integration ID",
        description="Id of the integration that this configuration is for",
    )
    action: IntegrationActionSummery
    data: Optional[Dict[str, Any]] = {}


class Integration(BaseModel):
    id: Union[UUID, str] = Field(
        None,
        title="Integration ID",
        description="Id of an integration in Gundi",
    )
    name: Optional[str] = Field(
        "",
        example="X Data Provider for Y Reserve",
        description="Route name",
    )
    type: IntegrationType
    base_url: Optional[str] = Field(
        "",
        example="https://easterisland.pamdas.org/",
        description="Base URL of the third party system associated with this integration.",
    )
    enabled: Optional[bool] = Field(
        True,
        example="true",
        description="Enable/Disable this integration",
    )
    owner: Organization
    configurations: Optional[List[IntegrationActionConfiguration]]
    default_route: Optional[ConnectionRoute]
    additional: Optional[Dict[str, Any]] = {}
    status: Optional[Dict[str, Any]] = Field(  # ToDo: Review once Activity/Monitoring is implemented
        {},
        example="{}",
        description="A json object with detailed information about the integration health status",
    )


# Earth Ranger Supported Actions & Configuration Schemas
class EarthRangerActions(str, Enum):
    AUTHENTICATE = "auth"
    PUSH_EVENT = "push_event"
    # ToDo. Add more as we support them


class ERAuthActionConfig(BaseModel):
    username: Optional[str] = Field(
        "",
        example="user@pamdas.org",
        description="Username used to authenticate against Earth Ranger API",
    )
    password: Optional[str] = Field(
        "",
        example="passwd1234abc",
        description="Password used to authenticate against Earth Ranger API",
    )
    token: Optional[str] = Field(
        "",
        example="1b4c1e9c-5ee0-44db-c7f1-177ede2f854a",
        description="Token used to authenticate against Earth Ranger API",
    )


class ERPushEventActionConfig(BaseModel):
    event_type: Optional[str] = Field(
        "",
        example="animal_sighting",
        description="Event type to be applied to event sent to Earth Ranger (Optional).",
    )


models_by_stream_type = {
    StreamPrefixEnum.event: Event,
    StreamPrefixEnum.attachment: Attachment,
}
