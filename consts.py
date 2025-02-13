from enum import Enum
from typing import TypedDict, Union

# PROGRAM DATA TYPES
class StreamType(Enum):
    DMC = 'dmc'
    DLIVE = 'dlive'
class StreamFmp4(TypedDict):
    enabled: bool

class Stream(TypedDict):
    type: StreamType
    fmp4: StreamFmp4

class Site(TypedDict):
    class Relive(TypedDict):
        apiBaseUrl: str
        channelApiBaseUrl: str
        webSocketUrl: str
        csrfToken: str
        audienceToken: str
    relive: Relive
    frontendId: int

class SupplierType(Enum):
    USER = "user"
class SupplierAccountType(Enum):
    PREMIUM = "premium"
class ProgramSupplier(TypedDict):
    supplierType: SupplierType
    accountType: SupplierAccountType
    programProviderId: str
    name: str
    level: str
    pageUrl: str
    introduction: str

class ProgramStatus(TypedDict):
    ONAIR = "ON_AIR"
    ENDED = "ENDED"
class MediaServerType(Enum):
    DMC = "DMC"
    DLIVE = "DLIVE"

class Program(TypedDict):
    status: ProgramStatus
    mediaServerType: MediaServerType
    supplier: ProgramSupplier
    nicoliveProgramId: str
    title: str
    description: str
    watchPageUrl: str
    openTime: int
    beginTime: int
    vposBaseTime: int
    endTime: int
    scheduledEndTime: int
    isPrivate: bool
    isTest: bool
    isFollowerOnly: bool
    isNicoadEnabled: bool
    isGiftEnabled: bool
    isChasePlayEnabled: bool
    isTimeshiftDownloadEnabled: bool
    isPremiumAppealBannerEnabled: bool
    isRecommendEnabled: bool
    isEmotionEnabled: bool

class ProgramData(TypedDict):
    site: Site
    stream: Stream
    program: Program
# END PROGRAM DATA TYPES

# WEBSOCKET TYPES
class WSResponseType(Enum):
    PING = 'ping'
    STREAM = 'stream'

class StreamCookies(TypedDict):
    name: str
    value: str
    domain: str
    path: str

class StreamData(TypedDict):
    uri: str
    cookies: list[StreamCookies]

class Stream(TypedDict):
    type: WSResponseType.STREAM
    data: StreamData

class Ping(TypedDict):
    type: WSResponseType.PING

WSResponse = Union[
    Ping,
    Stream,
]
# END WEBSOCKET TYPES
