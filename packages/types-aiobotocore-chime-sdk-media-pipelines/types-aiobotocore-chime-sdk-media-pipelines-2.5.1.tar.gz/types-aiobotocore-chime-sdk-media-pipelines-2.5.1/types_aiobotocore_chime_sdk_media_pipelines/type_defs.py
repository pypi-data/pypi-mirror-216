"""
Type annotations for chime-sdk-media-pipelines service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_chime_sdk_media_pipelines/type_defs/)

Usage::

    ```python
    from types_aiobotocore_chime_sdk_media_pipelines.type_defs import PostCallAnalyticsSettingsTypeDef

    data: PostCallAnalyticsSettingsTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ArtifactsConcatenationStateType,
    ArtifactsStateType,
    AudioChannelsOptionType,
    AudioMuxTypeType,
    CallAnalyticsLanguageCodeType,
    ContentRedactionOutputType,
    ContentShareLayoutOptionType,
    FragmentSelectorTypeType,
    LiveConnectorMuxTypeType,
    MediaInsightsPipelineConfigurationElementTypeType,
    MediaPipelineStatusType,
    MediaPipelineStatusUpdateType,
    PartialResultsStabilityType,
    ParticipantRoleType,
    PresenterPositionType,
    RealTimeAlertRuleTypeType,
    RecordingFileFormatType,
    ResolutionOptionType,
    VocabularyFilterMethodType,
    VoiceAnalyticsConfigurationStatusType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "PostCallAnalyticsSettingsTypeDef",
    "AmazonTranscribeProcessorConfigurationTypeDef",
    "AudioConcatenationConfigurationTypeDef",
    "CompositedVideoConcatenationConfigurationTypeDef",
    "ContentConcatenationConfigurationTypeDef",
    "DataChannelConcatenationConfigurationTypeDef",
    "MeetingEventsConcatenationConfigurationTypeDef",
    "TranscriptionMessagesConcatenationConfigurationTypeDef",
    "VideoConcatenationConfigurationTypeDef",
    "AudioArtifactsConfigurationTypeDef",
    "ContentArtifactsConfigurationTypeDef",
    "VideoArtifactsConfigurationTypeDef",
    "ChannelDefinitionTypeDef",
    "S3BucketSinkConfigurationTypeDef",
    "TagTypeDef",
    "S3RecordingSinkRuntimeConfigurationTypeDef",
    "DeleteMediaCapturePipelineRequestRequestTypeDef",
    "DeleteMediaInsightsPipelineConfigurationRequestRequestTypeDef",
    "DeleteMediaPipelineRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "TimestampRangeTypeDef",
    "GetMediaCapturePipelineRequestRequestTypeDef",
    "GetMediaInsightsPipelineConfigurationRequestRequestTypeDef",
    "GetMediaPipelineRequestRequestTypeDef",
    "PresenterOnlyConfigurationTypeDef",
    "IssueDetectionConfigurationTypeDef",
    "KeywordMatchConfigurationTypeDef",
    "KinesisDataStreamSinkConfigurationTypeDef",
    "RecordingStreamConfigurationTypeDef",
    "LambdaFunctionSinkConfigurationTypeDef",
    "ListMediaCapturePipelinesRequestRequestTypeDef",
    "MediaCapturePipelineSummaryTypeDef",
    "ListMediaInsightsPipelineConfigurationsRequestRequestTypeDef",
    "MediaInsightsPipelineConfigurationSummaryTypeDef",
    "ListMediaPipelinesRequestRequestTypeDef",
    "MediaPipelineSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "LiveConnectorRTMPConfigurationTypeDef",
    "S3RecordingSinkConfigurationTypeDef",
    "SnsTopicSinkConfigurationTypeDef",
    "SqsQueueSinkConfigurationTypeDef",
    "VoiceAnalyticsProcessorConfigurationTypeDef",
    "SentimentConfigurationTypeDef",
    "ResponseMetadataTypeDef",
    "SelectedVideoStreamsTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateMediaInsightsPipelineStatusRequestRequestTypeDef",
    "AmazonTranscribeCallAnalyticsProcessorConfigurationTypeDef",
    "ArtifactsConcatenationConfigurationTypeDef",
    "StreamChannelDefinitionTypeDef",
    "ConcatenationSinkTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "FragmentSelectorTypeDef",
    "GridViewConfigurationTypeDef",
    "ListMediaCapturePipelinesResponseTypeDef",
    "ListMediaInsightsPipelineConfigurationsResponseTypeDef",
    "ListMediaPipelinesResponseTypeDef",
    "LiveConnectorSinkConfigurationTypeDef",
    "RealTimeAlertRuleTypeDef",
    "SourceConfigurationTypeDef",
    "MediaInsightsPipelineConfigurationElementTypeDef",
    "ChimeSdkMeetingConcatenationConfigurationTypeDef",
    "StreamConfigurationTypeDef",
    "KinesisVideoStreamRecordingSourceRuntimeConfigurationTypeDef",
    "CompositedVideoArtifactsConfigurationTypeDef",
    "RealTimeAlertConfigurationTypeDef",
    "MediaCapturePipelineSourceConfigurationTypeDef",
    "KinesisVideoStreamSourceRuntimeConfigurationTypeDef",
    "ArtifactsConfigurationTypeDef",
    "ChimeSdkMeetingLiveConnectorConfigurationTypeDef",
    "CreateMediaInsightsPipelineConfigurationRequestRequestTypeDef",
    "MediaInsightsPipelineConfigurationTypeDef",
    "UpdateMediaInsightsPipelineConfigurationRequestRequestTypeDef",
    "ConcatenationSourceTypeDef",
    "CreateMediaInsightsPipelineRequestRequestTypeDef",
    "MediaInsightsPipelineTypeDef",
    "ChimeSdkMeetingConfigurationTypeDef",
    "LiveConnectorSourceConfigurationTypeDef",
    "CreateMediaInsightsPipelineConfigurationResponseTypeDef",
    "GetMediaInsightsPipelineConfigurationResponseTypeDef",
    "UpdateMediaInsightsPipelineConfigurationResponseTypeDef",
    "CreateMediaConcatenationPipelineRequestRequestTypeDef",
    "MediaConcatenationPipelineTypeDef",
    "CreateMediaInsightsPipelineResponseTypeDef",
    "CreateMediaCapturePipelineRequestRequestTypeDef",
    "MediaCapturePipelineTypeDef",
    "CreateMediaLiveConnectorPipelineRequestRequestTypeDef",
    "MediaLiveConnectorPipelineTypeDef",
    "CreateMediaConcatenationPipelineResponseTypeDef",
    "CreateMediaCapturePipelineResponseTypeDef",
    "GetMediaCapturePipelineResponseTypeDef",
    "CreateMediaLiveConnectorPipelineResponseTypeDef",
    "MediaPipelineTypeDef",
    "GetMediaPipelineResponseTypeDef",
)

_RequiredPostCallAnalyticsSettingsTypeDef = TypedDict(
    "_RequiredPostCallAnalyticsSettingsTypeDef",
    {
        "OutputLocation": str,
        "DataAccessRoleArn": str,
    },
)
_OptionalPostCallAnalyticsSettingsTypeDef = TypedDict(
    "_OptionalPostCallAnalyticsSettingsTypeDef",
    {
        "ContentRedactionOutput": ContentRedactionOutputType,
        "OutputEncryptionKMSKeyId": str,
    },
    total=False,
)


class PostCallAnalyticsSettingsTypeDef(
    _RequiredPostCallAnalyticsSettingsTypeDef, _OptionalPostCallAnalyticsSettingsTypeDef
):
    pass


_RequiredAmazonTranscribeProcessorConfigurationTypeDef = TypedDict(
    "_RequiredAmazonTranscribeProcessorConfigurationTypeDef",
    {
        "LanguageCode": CallAnalyticsLanguageCodeType,
    },
)
_OptionalAmazonTranscribeProcessorConfigurationTypeDef = TypedDict(
    "_OptionalAmazonTranscribeProcessorConfigurationTypeDef",
    {
        "VocabularyName": str,
        "VocabularyFilterName": str,
        "VocabularyFilterMethod": VocabularyFilterMethodType,
        "ShowSpeakerLabel": bool,
        "EnablePartialResultsStabilization": bool,
        "PartialResultsStability": PartialResultsStabilityType,
        "ContentIdentificationType": Literal["PII"],
        "ContentRedactionType": Literal["PII"],
        "PiiEntityTypes": str,
        "LanguageModelName": str,
        "FilterPartialResults": bool,
    },
    total=False,
)


class AmazonTranscribeProcessorConfigurationTypeDef(
    _RequiredAmazonTranscribeProcessorConfigurationTypeDef,
    _OptionalAmazonTranscribeProcessorConfigurationTypeDef,
):
    pass


AudioConcatenationConfigurationTypeDef = TypedDict(
    "AudioConcatenationConfigurationTypeDef",
    {
        "State": Literal["Enabled"],
    },
)

CompositedVideoConcatenationConfigurationTypeDef = TypedDict(
    "CompositedVideoConcatenationConfigurationTypeDef",
    {
        "State": ArtifactsConcatenationStateType,
    },
)

ContentConcatenationConfigurationTypeDef = TypedDict(
    "ContentConcatenationConfigurationTypeDef",
    {
        "State": ArtifactsConcatenationStateType,
    },
)

DataChannelConcatenationConfigurationTypeDef = TypedDict(
    "DataChannelConcatenationConfigurationTypeDef",
    {
        "State": ArtifactsConcatenationStateType,
    },
)

MeetingEventsConcatenationConfigurationTypeDef = TypedDict(
    "MeetingEventsConcatenationConfigurationTypeDef",
    {
        "State": ArtifactsConcatenationStateType,
    },
)

TranscriptionMessagesConcatenationConfigurationTypeDef = TypedDict(
    "TranscriptionMessagesConcatenationConfigurationTypeDef",
    {
        "State": ArtifactsConcatenationStateType,
    },
)

VideoConcatenationConfigurationTypeDef = TypedDict(
    "VideoConcatenationConfigurationTypeDef",
    {
        "State": ArtifactsConcatenationStateType,
    },
)

AudioArtifactsConfigurationTypeDef = TypedDict(
    "AudioArtifactsConfigurationTypeDef",
    {
        "MuxType": AudioMuxTypeType,
    },
)

_RequiredContentArtifactsConfigurationTypeDef = TypedDict(
    "_RequiredContentArtifactsConfigurationTypeDef",
    {
        "State": ArtifactsStateType,
    },
)
_OptionalContentArtifactsConfigurationTypeDef = TypedDict(
    "_OptionalContentArtifactsConfigurationTypeDef",
    {
        "MuxType": Literal["ContentOnly"],
    },
    total=False,
)


class ContentArtifactsConfigurationTypeDef(
    _RequiredContentArtifactsConfigurationTypeDef, _OptionalContentArtifactsConfigurationTypeDef
):
    pass


_RequiredVideoArtifactsConfigurationTypeDef = TypedDict(
    "_RequiredVideoArtifactsConfigurationTypeDef",
    {
        "State": ArtifactsStateType,
    },
)
_OptionalVideoArtifactsConfigurationTypeDef = TypedDict(
    "_OptionalVideoArtifactsConfigurationTypeDef",
    {
        "MuxType": Literal["VideoOnly"],
    },
    total=False,
)


class VideoArtifactsConfigurationTypeDef(
    _RequiredVideoArtifactsConfigurationTypeDef, _OptionalVideoArtifactsConfigurationTypeDef
):
    pass


_RequiredChannelDefinitionTypeDef = TypedDict(
    "_RequiredChannelDefinitionTypeDef",
    {
        "ChannelId": int,
    },
)
_OptionalChannelDefinitionTypeDef = TypedDict(
    "_OptionalChannelDefinitionTypeDef",
    {
        "ParticipantRole": ParticipantRoleType,
    },
    total=False,
)


class ChannelDefinitionTypeDef(
    _RequiredChannelDefinitionTypeDef, _OptionalChannelDefinitionTypeDef
):
    pass


S3BucketSinkConfigurationTypeDef = TypedDict(
    "S3BucketSinkConfigurationTypeDef",
    {
        "Destination": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

S3RecordingSinkRuntimeConfigurationTypeDef = TypedDict(
    "S3RecordingSinkRuntimeConfigurationTypeDef",
    {
        "Destination": str,
        "RecordingFileFormat": RecordingFileFormatType,
    },
)

DeleteMediaCapturePipelineRequestRequestTypeDef = TypedDict(
    "DeleteMediaCapturePipelineRequestRequestTypeDef",
    {
        "MediaPipelineId": str,
    },
)

DeleteMediaInsightsPipelineConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteMediaInsightsPipelineConfigurationRequestRequestTypeDef",
    {
        "Identifier": str,
    },
)

DeleteMediaPipelineRequestRequestTypeDef = TypedDict(
    "DeleteMediaPipelineRequestRequestTypeDef",
    {
        "MediaPipelineId": str,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TimestampRangeTypeDef = TypedDict(
    "TimestampRangeTypeDef",
    {
        "StartTimestamp": Union[datetime, str],
        "EndTimestamp": Union[datetime, str],
    },
)

GetMediaCapturePipelineRequestRequestTypeDef = TypedDict(
    "GetMediaCapturePipelineRequestRequestTypeDef",
    {
        "MediaPipelineId": str,
    },
)

GetMediaInsightsPipelineConfigurationRequestRequestTypeDef = TypedDict(
    "GetMediaInsightsPipelineConfigurationRequestRequestTypeDef",
    {
        "Identifier": str,
    },
)

GetMediaPipelineRequestRequestTypeDef = TypedDict(
    "GetMediaPipelineRequestRequestTypeDef",
    {
        "MediaPipelineId": str,
    },
)

PresenterOnlyConfigurationTypeDef = TypedDict(
    "PresenterOnlyConfigurationTypeDef",
    {
        "PresenterPosition": PresenterPositionType,
    },
    total=False,
)

IssueDetectionConfigurationTypeDef = TypedDict(
    "IssueDetectionConfigurationTypeDef",
    {
        "RuleName": str,
    },
)

_RequiredKeywordMatchConfigurationTypeDef = TypedDict(
    "_RequiredKeywordMatchConfigurationTypeDef",
    {
        "RuleName": str,
        "Keywords": Sequence[str],
    },
)
_OptionalKeywordMatchConfigurationTypeDef = TypedDict(
    "_OptionalKeywordMatchConfigurationTypeDef",
    {
        "Negate": bool,
    },
    total=False,
)


class KeywordMatchConfigurationTypeDef(
    _RequiredKeywordMatchConfigurationTypeDef, _OptionalKeywordMatchConfigurationTypeDef
):
    pass


KinesisDataStreamSinkConfigurationTypeDef = TypedDict(
    "KinesisDataStreamSinkConfigurationTypeDef",
    {
        "InsightsTarget": str,
    },
    total=False,
)

RecordingStreamConfigurationTypeDef = TypedDict(
    "RecordingStreamConfigurationTypeDef",
    {
        "StreamArn": str,
    },
    total=False,
)

LambdaFunctionSinkConfigurationTypeDef = TypedDict(
    "LambdaFunctionSinkConfigurationTypeDef",
    {
        "InsightsTarget": str,
    },
    total=False,
)

ListMediaCapturePipelinesRequestRequestTypeDef = TypedDict(
    "ListMediaCapturePipelinesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

MediaCapturePipelineSummaryTypeDef = TypedDict(
    "MediaCapturePipelineSummaryTypeDef",
    {
        "MediaPipelineId": str,
        "MediaPipelineArn": str,
    },
    total=False,
)

ListMediaInsightsPipelineConfigurationsRequestRequestTypeDef = TypedDict(
    "ListMediaInsightsPipelineConfigurationsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

MediaInsightsPipelineConfigurationSummaryTypeDef = TypedDict(
    "MediaInsightsPipelineConfigurationSummaryTypeDef",
    {
        "MediaInsightsPipelineConfigurationName": str,
        "MediaInsightsPipelineConfigurationId": str,
        "MediaInsightsPipelineConfigurationArn": str,
    },
    total=False,
)

ListMediaPipelinesRequestRequestTypeDef = TypedDict(
    "ListMediaPipelinesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

MediaPipelineSummaryTypeDef = TypedDict(
    "MediaPipelineSummaryTypeDef",
    {
        "MediaPipelineId": str,
        "MediaPipelineArn": str,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

_RequiredLiveConnectorRTMPConfigurationTypeDef = TypedDict(
    "_RequiredLiveConnectorRTMPConfigurationTypeDef",
    {
        "Url": str,
    },
)
_OptionalLiveConnectorRTMPConfigurationTypeDef = TypedDict(
    "_OptionalLiveConnectorRTMPConfigurationTypeDef",
    {
        "AudioChannels": AudioChannelsOptionType,
        "AudioSampleRate": str,
    },
    total=False,
)


class LiveConnectorRTMPConfigurationTypeDef(
    _RequiredLiveConnectorRTMPConfigurationTypeDef, _OptionalLiveConnectorRTMPConfigurationTypeDef
):
    pass


S3RecordingSinkConfigurationTypeDef = TypedDict(
    "S3RecordingSinkConfigurationTypeDef",
    {
        "Destination": str,
        "RecordingFileFormat": RecordingFileFormatType,
    },
    total=False,
)

SnsTopicSinkConfigurationTypeDef = TypedDict(
    "SnsTopicSinkConfigurationTypeDef",
    {
        "InsightsTarget": str,
    },
    total=False,
)

SqsQueueSinkConfigurationTypeDef = TypedDict(
    "SqsQueueSinkConfigurationTypeDef",
    {
        "InsightsTarget": str,
    },
    total=False,
)

VoiceAnalyticsProcessorConfigurationTypeDef = TypedDict(
    "VoiceAnalyticsProcessorConfigurationTypeDef",
    {
        "SpeakerSearchStatus": VoiceAnalyticsConfigurationStatusType,
        "VoiceToneAnalysisStatus": VoiceAnalyticsConfigurationStatusType,
    },
    total=False,
)

SentimentConfigurationTypeDef = TypedDict(
    "SentimentConfigurationTypeDef",
    {
        "RuleName": str,
        "SentimentType": Literal["NEGATIVE"],
        "TimePeriod": int,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

SelectedVideoStreamsTypeDef = TypedDict(
    "SelectedVideoStreamsTypeDef",
    {
        "AttendeeIds": Sequence[str],
        "ExternalUserIds": Sequence[str],
    },
    total=False,
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

UpdateMediaInsightsPipelineStatusRequestRequestTypeDef = TypedDict(
    "UpdateMediaInsightsPipelineStatusRequestRequestTypeDef",
    {
        "Identifier": str,
        "UpdateStatus": MediaPipelineStatusUpdateType,
    },
)

_RequiredAmazonTranscribeCallAnalyticsProcessorConfigurationTypeDef = TypedDict(
    "_RequiredAmazonTranscribeCallAnalyticsProcessorConfigurationTypeDef",
    {
        "LanguageCode": CallAnalyticsLanguageCodeType,
    },
)
_OptionalAmazonTranscribeCallAnalyticsProcessorConfigurationTypeDef = TypedDict(
    "_OptionalAmazonTranscribeCallAnalyticsProcessorConfigurationTypeDef",
    {
        "VocabularyName": str,
        "VocabularyFilterName": str,
        "VocabularyFilterMethod": VocabularyFilterMethodType,
        "LanguageModelName": str,
        "EnablePartialResultsStabilization": bool,
        "PartialResultsStability": PartialResultsStabilityType,
        "ContentIdentificationType": Literal["PII"],
        "ContentRedactionType": Literal["PII"],
        "PiiEntityTypes": str,
        "FilterPartialResults": bool,
        "PostCallAnalyticsSettings": PostCallAnalyticsSettingsTypeDef,
        "CallAnalyticsStreamCategories": Sequence[str],
    },
    total=False,
)


class AmazonTranscribeCallAnalyticsProcessorConfigurationTypeDef(
    _RequiredAmazonTranscribeCallAnalyticsProcessorConfigurationTypeDef,
    _OptionalAmazonTranscribeCallAnalyticsProcessorConfigurationTypeDef,
):
    pass


ArtifactsConcatenationConfigurationTypeDef = TypedDict(
    "ArtifactsConcatenationConfigurationTypeDef",
    {
        "Audio": AudioConcatenationConfigurationTypeDef,
        "Video": VideoConcatenationConfigurationTypeDef,
        "Content": ContentConcatenationConfigurationTypeDef,
        "DataChannel": DataChannelConcatenationConfigurationTypeDef,
        "TranscriptionMessages": TranscriptionMessagesConcatenationConfigurationTypeDef,
        "MeetingEvents": MeetingEventsConcatenationConfigurationTypeDef,
        "CompositedVideo": CompositedVideoConcatenationConfigurationTypeDef,
    },
)

_RequiredStreamChannelDefinitionTypeDef = TypedDict(
    "_RequiredStreamChannelDefinitionTypeDef",
    {
        "NumberOfChannels": int,
    },
)
_OptionalStreamChannelDefinitionTypeDef = TypedDict(
    "_OptionalStreamChannelDefinitionTypeDef",
    {
        "ChannelDefinitions": Sequence[ChannelDefinitionTypeDef],
    },
    total=False,
)


class StreamChannelDefinitionTypeDef(
    _RequiredStreamChannelDefinitionTypeDef, _OptionalStreamChannelDefinitionTypeDef
):
    pass


ConcatenationSinkTypeDef = TypedDict(
    "ConcatenationSinkTypeDef",
    {
        "Type": Literal["S3Bucket"],
        "S3BucketSinkConfiguration": S3BucketSinkConfigurationTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

FragmentSelectorTypeDef = TypedDict(
    "FragmentSelectorTypeDef",
    {
        "FragmentSelectorType": FragmentSelectorTypeType,
        "TimestampRange": TimestampRangeTypeDef,
    },
)

_RequiredGridViewConfigurationTypeDef = TypedDict(
    "_RequiredGridViewConfigurationTypeDef",
    {
        "ContentShareLayout": ContentShareLayoutOptionType,
    },
)
_OptionalGridViewConfigurationTypeDef = TypedDict(
    "_OptionalGridViewConfigurationTypeDef",
    {
        "PresenterOnlyConfiguration": PresenterOnlyConfigurationTypeDef,
    },
    total=False,
)


class GridViewConfigurationTypeDef(
    _RequiredGridViewConfigurationTypeDef, _OptionalGridViewConfigurationTypeDef
):
    pass


ListMediaCapturePipelinesResponseTypeDef = TypedDict(
    "ListMediaCapturePipelinesResponseTypeDef",
    {
        "MediaCapturePipelines": List[MediaCapturePipelineSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMediaInsightsPipelineConfigurationsResponseTypeDef = TypedDict(
    "ListMediaInsightsPipelineConfigurationsResponseTypeDef",
    {
        "MediaInsightsPipelineConfigurations": List[
            MediaInsightsPipelineConfigurationSummaryTypeDef
        ],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMediaPipelinesResponseTypeDef = TypedDict(
    "ListMediaPipelinesResponseTypeDef",
    {
        "MediaPipelines": List[MediaPipelineSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LiveConnectorSinkConfigurationTypeDef = TypedDict(
    "LiveConnectorSinkConfigurationTypeDef",
    {
        "SinkType": Literal["RTMP"],
        "RTMPConfiguration": LiveConnectorRTMPConfigurationTypeDef,
    },
)

_RequiredRealTimeAlertRuleTypeDef = TypedDict(
    "_RequiredRealTimeAlertRuleTypeDef",
    {
        "Type": RealTimeAlertRuleTypeType,
    },
)
_OptionalRealTimeAlertRuleTypeDef = TypedDict(
    "_OptionalRealTimeAlertRuleTypeDef",
    {
        "KeywordMatchConfiguration": KeywordMatchConfigurationTypeDef,
        "SentimentConfiguration": SentimentConfigurationTypeDef,
        "IssueDetectionConfiguration": IssueDetectionConfigurationTypeDef,
    },
    total=False,
)


class RealTimeAlertRuleTypeDef(
    _RequiredRealTimeAlertRuleTypeDef, _OptionalRealTimeAlertRuleTypeDef
):
    pass


SourceConfigurationTypeDef = TypedDict(
    "SourceConfigurationTypeDef",
    {
        "SelectedVideoStreams": SelectedVideoStreamsTypeDef,
    },
    total=False,
)

_RequiredMediaInsightsPipelineConfigurationElementTypeDef = TypedDict(
    "_RequiredMediaInsightsPipelineConfigurationElementTypeDef",
    {
        "Type": MediaInsightsPipelineConfigurationElementTypeType,
    },
)
_OptionalMediaInsightsPipelineConfigurationElementTypeDef = TypedDict(
    "_OptionalMediaInsightsPipelineConfigurationElementTypeDef",
    {
        "AmazonTranscribeCallAnalyticsProcessorConfiguration": (
            AmazonTranscribeCallAnalyticsProcessorConfigurationTypeDef
        ),
        "AmazonTranscribeProcessorConfiguration": AmazonTranscribeProcessorConfigurationTypeDef,
        "KinesisDataStreamSinkConfiguration": KinesisDataStreamSinkConfigurationTypeDef,
        "S3RecordingSinkConfiguration": S3RecordingSinkConfigurationTypeDef,
        "VoiceAnalyticsProcessorConfiguration": VoiceAnalyticsProcessorConfigurationTypeDef,
        "LambdaFunctionSinkConfiguration": LambdaFunctionSinkConfigurationTypeDef,
        "SqsQueueSinkConfiguration": SqsQueueSinkConfigurationTypeDef,
        "SnsTopicSinkConfiguration": SnsTopicSinkConfigurationTypeDef,
    },
    total=False,
)


class MediaInsightsPipelineConfigurationElementTypeDef(
    _RequiredMediaInsightsPipelineConfigurationElementTypeDef,
    _OptionalMediaInsightsPipelineConfigurationElementTypeDef,
):
    pass


ChimeSdkMeetingConcatenationConfigurationTypeDef = TypedDict(
    "ChimeSdkMeetingConcatenationConfigurationTypeDef",
    {
        "ArtifactsConfiguration": ArtifactsConcatenationConfigurationTypeDef,
    },
)

_RequiredStreamConfigurationTypeDef = TypedDict(
    "_RequiredStreamConfigurationTypeDef",
    {
        "StreamArn": str,
        "StreamChannelDefinition": StreamChannelDefinitionTypeDef,
    },
)
_OptionalStreamConfigurationTypeDef = TypedDict(
    "_OptionalStreamConfigurationTypeDef",
    {
        "FragmentNumber": str,
    },
    total=False,
)


class StreamConfigurationTypeDef(
    _RequiredStreamConfigurationTypeDef, _OptionalStreamConfigurationTypeDef
):
    pass


KinesisVideoStreamRecordingSourceRuntimeConfigurationTypeDef = TypedDict(
    "KinesisVideoStreamRecordingSourceRuntimeConfigurationTypeDef",
    {
        "Streams": Sequence[RecordingStreamConfigurationTypeDef],
        "FragmentSelector": FragmentSelectorTypeDef,
    },
)

_RequiredCompositedVideoArtifactsConfigurationTypeDef = TypedDict(
    "_RequiredCompositedVideoArtifactsConfigurationTypeDef",
    {
        "GridViewConfiguration": GridViewConfigurationTypeDef,
    },
)
_OptionalCompositedVideoArtifactsConfigurationTypeDef = TypedDict(
    "_OptionalCompositedVideoArtifactsConfigurationTypeDef",
    {
        "Layout": Literal["GridView"],
        "Resolution": ResolutionOptionType,
    },
    total=False,
)


class CompositedVideoArtifactsConfigurationTypeDef(
    _RequiredCompositedVideoArtifactsConfigurationTypeDef,
    _OptionalCompositedVideoArtifactsConfigurationTypeDef,
):
    pass


RealTimeAlertConfigurationTypeDef = TypedDict(
    "RealTimeAlertConfigurationTypeDef",
    {
        "Disabled": bool,
        "Rules": Sequence[RealTimeAlertRuleTypeDef],
    },
    total=False,
)

MediaCapturePipelineSourceConfigurationTypeDef = TypedDict(
    "MediaCapturePipelineSourceConfigurationTypeDef",
    {
        "MediaPipelineArn": str,
        "ChimeSdkMeetingConfiguration": ChimeSdkMeetingConcatenationConfigurationTypeDef,
    },
)

KinesisVideoStreamSourceRuntimeConfigurationTypeDef = TypedDict(
    "KinesisVideoStreamSourceRuntimeConfigurationTypeDef",
    {
        "Streams": Sequence[StreamConfigurationTypeDef],
        "MediaEncoding": Literal["pcm"],
        "MediaSampleRate": int,
    },
)

_RequiredArtifactsConfigurationTypeDef = TypedDict(
    "_RequiredArtifactsConfigurationTypeDef",
    {
        "Audio": AudioArtifactsConfigurationTypeDef,
        "Video": VideoArtifactsConfigurationTypeDef,
        "Content": ContentArtifactsConfigurationTypeDef,
    },
)
_OptionalArtifactsConfigurationTypeDef = TypedDict(
    "_OptionalArtifactsConfigurationTypeDef",
    {
        "CompositedVideo": CompositedVideoArtifactsConfigurationTypeDef,
    },
    total=False,
)


class ArtifactsConfigurationTypeDef(
    _RequiredArtifactsConfigurationTypeDef, _OptionalArtifactsConfigurationTypeDef
):
    pass


_RequiredChimeSdkMeetingLiveConnectorConfigurationTypeDef = TypedDict(
    "_RequiredChimeSdkMeetingLiveConnectorConfigurationTypeDef",
    {
        "Arn": str,
        "MuxType": LiveConnectorMuxTypeType,
    },
)
_OptionalChimeSdkMeetingLiveConnectorConfigurationTypeDef = TypedDict(
    "_OptionalChimeSdkMeetingLiveConnectorConfigurationTypeDef",
    {
        "CompositedVideo": CompositedVideoArtifactsConfigurationTypeDef,
        "SourceConfiguration": SourceConfigurationTypeDef,
    },
    total=False,
)


class ChimeSdkMeetingLiveConnectorConfigurationTypeDef(
    _RequiredChimeSdkMeetingLiveConnectorConfigurationTypeDef,
    _OptionalChimeSdkMeetingLiveConnectorConfigurationTypeDef,
):
    pass


_RequiredCreateMediaInsightsPipelineConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMediaInsightsPipelineConfigurationRequestRequestTypeDef",
    {
        "MediaInsightsPipelineConfigurationName": str,
        "ResourceAccessRoleArn": str,
        "Elements": Sequence[MediaInsightsPipelineConfigurationElementTypeDef],
    },
)
_OptionalCreateMediaInsightsPipelineConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMediaInsightsPipelineConfigurationRequestRequestTypeDef",
    {
        "RealTimeAlertConfiguration": RealTimeAlertConfigurationTypeDef,
        "Tags": Sequence[TagTypeDef],
        "ClientRequestToken": str,
    },
    total=False,
)


class CreateMediaInsightsPipelineConfigurationRequestRequestTypeDef(
    _RequiredCreateMediaInsightsPipelineConfigurationRequestRequestTypeDef,
    _OptionalCreateMediaInsightsPipelineConfigurationRequestRequestTypeDef,
):
    pass


MediaInsightsPipelineConfigurationTypeDef = TypedDict(
    "MediaInsightsPipelineConfigurationTypeDef",
    {
        "MediaInsightsPipelineConfigurationName": str,
        "MediaInsightsPipelineConfigurationArn": str,
        "ResourceAccessRoleArn": str,
        "RealTimeAlertConfiguration": RealTimeAlertConfigurationTypeDef,
        "Elements": List[MediaInsightsPipelineConfigurationElementTypeDef],
        "MediaInsightsPipelineConfigurationId": str,
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
    },
    total=False,
)

_RequiredUpdateMediaInsightsPipelineConfigurationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateMediaInsightsPipelineConfigurationRequestRequestTypeDef",
    {
        "Identifier": str,
        "ResourceAccessRoleArn": str,
        "Elements": Sequence[MediaInsightsPipelineConfigurationElementTypeDef],
    },
)
_OptionalUpdateMediaInsightsPipelineConfigurationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateMediaInsightsPipelineConfigurationRequestRequestTypeDef",
    {
        "RealTimeAlertConfiguration": RealTimeAlertConfigurationTypeDef,
    },
    total=False,
)


class UpdateMediaInsightsPipelineConfigurationRequestRequestTypeDef(
    _RequiredUpdateMediaInsightsPipelineConfigurationRequestRequestTypeDef,
    _OptionalUpdateMediaInsightsPipelineConfigurationRequestRequestTypeDef,
):
    pass


ConcatenationSourceTypeDef = TypedDict(
    "ConcatenationSourceTypeDef",
    {
        "Type": Literal["MediaCapturePipeline"],
        "MediaCapturePipelineSourceConfiguration": MediaCapturePipelineSourceConfigurationTypeDef,
    },
)

_RequiredCreateMediaInsightsPipelineRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMediaInsightsPipelineRequestRequestTypeDef",
    {
        "MediaInsightsPipelineConfigurationArn": str,
    },
)
_OptionalCreateMediaInsightsPipelineRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMediaInsightsPipelineRequestRequestTypeDef",
    {
        "KinesisVideoStreamSourceRuntimeConfiguration": (
            KinesisVideoStreamSourceRuntimeConfigurationTypeDef
        ),
        "MediaInsightsRuntimeMetadata": Mapping[str, str],
        "KinesisVideoStreamRecordingSourceRuntimeConfiguration": (
            KinesisVideoStreamRecordingSourceRuntimeConfigurationTypeDef
        ),
        "S3RecordingSinkRuntimeConfiguration": S3RecordingSinkRuntimeConfigurationTypeDef,
        "Tags": Sequence[TagTypeDef],
        "ClientRequestToken": str,
    },
    total=False,
)


class CreateMediaInsightsPipelineRequestRequestTypeDef(
    _RequiredCreateMediaInsightsPipelineRequestRequestTypeDef,
    _OptionalCreateMediaInsightsPipelineRequestRequestTypeDef,
):
    pass


MediaInsightsPipelineTypeDef = TypedDict(
    "MediaInsightsPipelineTypeDef",
    {
        "MediaPipelineId": str,
        "MediaPipelineArn": str,
        "MediaInsightsPipelineConfigurationArn": str,
        "Status": MediaPipelineStatusType,
        "KinesisVideoStreamSourceRuntimeConfiguration": (
            KinesisVideoStreamSourceRuntimeConfigurationTypeDef
        ),
        "MediaInsightsRuntimeMetadata": Dict[str, str],
        "KinesisVideoStreamRecordingSourceRuntimeConfiguration": (
            KinesisVideoStreamRecordingSourceRuntimeConfigurationTypeDef
        ),
        "S3RecordingSinkRuntimeConfiguration": S3RecordingSinkRuntimeConfigurationTypeDef,
        "CreatedTimestamp": datetime,
    },
    total=False,
)

ChimeSdkMeetingConfigurationTypeDef = TypedDict(
    "ChimeSdkMeetingConfigurationTypeDef",
    {
        "SourceConfiguration": SourceConfigurationTypeDef,
        "ArtifactsConfiguration": ArtifactsConfigurationTypeDef,
    },
    total=False,
)

LiveConnectorSourceConfigurationTypeDef = TypedDict(
    "LiveConnectorSourceConfigurationTypeDef",
    {
        "SourceType": Literal["ChimeSdkMeeting"],
        "ChimeSdkMeetingLiveConnectorConfiguration": (
            ChimeSdkMeetingLiveConnectorConfigurationTypeDef
        ),
    },
)

CreateMediaInsightsPipelineConfigurationResponseTypeDef = TypedDict(
    "CreateMediaInsightsPipelineConfigurationResponseTypeDef",
    {
        "MediaInsightsPipelineConfiguration": MediaInsightsPipelineConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetMediaInsightsPipelineConfigurationResponseTypeDef = TypedDict(
    "GetMediaInsightsPipelineConfigurationResponseTypeDef",
    {
        "MediaInsightsPipelineConfiguration": MediaInsightsPipelineConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateMediaInsightsPipelineConfigurationResponseTypeDef = TypedDict(
    "UpdateMediaInsightsPipelineConfigurationResponseTypeDef",
    {
        "MediaInsightsPipelineConfiguration": MediaInsightsPipelineConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateMediaConcatenationPipelineRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMediaConcatenationPipelineRequestRequestTypeDef",
    {
        "Sources": Sequence[ConcatenationSourceTypeDef],
        "Sinks": Sequence[ConcatenationSinkTypeDef],
    },
)
_OptionalCreateMediaConcatenationPipelineRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMediaConcatenationPipelineRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateMediaConcatenationPipelineRequestRequestTypeDef(
    _RequiredCreateMediaConcatenationPipelineRequestRequestTypeDef,
    _OptionalCreateMediaConcatenationPipelineRequestRequestTypeDef,
):
    pass


MediaConcatenationPipelineTypeDef = TypedDict(
    "MediaConcatenationPipelineTypeDef",
    {
        "MediaPipelineId": str,
        "MediaPipelineArn": str,
        "Sources": List[ConcatenationSourceTypeDef],
        "Sinks": List[ConcatenationSinkTypeDef],
        "Status": MediaPipelineStatusType,
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
    },
    total=False,
)

CreateMediaInsightsPipelineResponseTypeDef = TypedDict(
    "CreateMediaInsightsPipelineResponseTypeDef",
    {
        "MediaInsightsPipeline": MediaInsightsPipelineTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateMediaCapturePipelineRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMediaCapturePipelineRequestRequestTypeDef",
    {
        "SourceType": Literal["ChimeSdkMeeting"],
        "SourceArn": str,
        "SinkType": Literal["S3Bucket"],
        "SinkArn": str,
    },
)
_OptionalCreateMediaCapturePipelineRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMediaCapturePipelineRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "ChimeSdkMeetingConfiguration": ChimeSdkMeetingConfigurationTypeDef,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateMediaCapturePipelineRequestRequestTypeDef(
    _RequiredCreateMediaCapturePipelineRequestRequestTypeDef,
    _OptionalCreateMediaCapturePipelineRequestRequestTypeDef,
):
    pass


MediaCapturePipelineTypeDef = TypedDict(
    "MediaCapturePipelineTypeDef",
    {
        "MediaPipelineId": str,
        "MediaPipelineArn": str,
        "SourceType": Literal["ChimeSdkMeeting"],
        "SourceArn": str,
        "Status": MediaPipelineStatusType,
        "SinkType": Literal["S3Bucket"],
        "SinkArn": str,
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
        "ChimeSdkMeetingConfiguration": ChimeSdkMeetingConfigurationTypeDef,
    },
    total=False,
)

_RequiredCreateMediaLiveConnectorPipelineRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMediaLiveConnectorPipelineRequestRequestTypeDef",
    {
        "Sources": Sequence[LiveConnectorSourceConfigurationTypeDef],
        "Sinks": Sequence[LiveConnectorSinkConfigurationTypeDef],
    },
)
_OptionalCreateMediaLiveConnectorPipelineRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMediaLiveConnectorPipelineRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateMediaLiveConnectorPipelineRequestRequestTypeDef(
    _RequiredCreateMediaLiveConnectorPipelineRequestRequestTypeDef,
    _OptionalCreateMediaLiveConnectorPipelineRequestRequestTypeDef,
):
    pass


MediaLiveConnectorPipelineTypeDef = TypedDict(
    "MediaLiveConnectorPipelineTypeDef",
    {
        "Sources": List[LiveConnectorSourceConfigurationTypeDef],
        "Sinks": List[LiveConnectorSinkConfigurationTypeDef],
        "MediaPipelineId": str,
        "MediaPipelineArn": str,
        "Status": MediaPipelineStatusType,
        "CreatedTimestamp": datetime,
        "UpdatedTimestamp": datetime,
    },
    total=False,
)

CreateMediaConcatenationPipelineResponseTypeDef = TypedDict(
    "CreateMediaConcatenationPipelineResponseTypeDef",
    {
        "MediaConcatenationPipeline": MediaConcatenationPipelineTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateMediaCapturePipelineResponseTypeDef = TypedDict(
    "CreateMediaCapturePipelineResponseTypeDef",
    {
        "MediaCapturePipeline": MediaCapturePipelineTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetMediaCapturePipelineResponseTypeDef = TypedDict(
    "GetMediaCapturePipelineResponseTypeDef",
    {
        "MediaCapturePipeline": MediaCapturePipelineTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateMediaLiveConnectorPipelineResponseTypeDef = TypedDict(
    "CreateMediaLiveConnectorPipelineResponseTypeDef",
    {
        "MediaLiveConnectorPipeline": MediaLiveConnectorPipelineTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

MediaPipelineTypeDef = TypedDict(
    "MediaPipelineTypeDef",
    {
        "MediaCapturePipeline": MediaCapturePipelineTypeDef,
        "MediaLiveConnectorPipeline": MediaLiveConnectorPipelineTypeDef,
        "MediaConcatenationPipeline": MediaConcatenationPipelineTypeDef,
        "MediaInsightsPipeline": MediaInsightsPipelineTypeDef,
    },
    total=False,
)

GetMediaPipelineResponseTypeDef = TypedDict(
    "GetMediaPipelineResponseTypeDef",
    {
        "MediaPipeline": MediaPipelineTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
