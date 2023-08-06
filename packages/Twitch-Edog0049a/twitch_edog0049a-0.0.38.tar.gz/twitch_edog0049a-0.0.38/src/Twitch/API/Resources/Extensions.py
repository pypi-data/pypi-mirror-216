from Twitch.API.Resources.__imports import *

class GetExtensionConfigurationSegmentRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.GET
        scope = None
        authorization = Utils.AuthRequired.JTW
        endPoint ="/extensions/configurations"
        def __init__(self,extension_id: str, segment: str, broadcaster_id: Optional[str]=None) -> None:
            self.extension_id = extension_id        
            self.segment = segment
            self.broadcaster_id = broadcaster_id
            super().__init__()

class GetExtensionConfigurationSegmentItem:
    broadcaster_id: str
    segment: str
    version: str
    content: str 

class GetExtensionConfigurationSegmentResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(GetExtensionConfigurationSegmentItem)

class SetExtensionConfigurationSegmentRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.PUT
        scope = None
        authorization = Utils.AuthRequired.JTW
        endPoint ="/extensions/configurations"
        def __init__(self, extension_id: str, segment: str, broadcaster_id: Optional[str]=None, content: Optional[str]=None, version: Optional[str]=None) -> None:
            self.extension_id = extension_id
            self.segment = segment
            self.broadcaster_id = broadcaster_id
            self.content = content
            self.version = version
            super().__init__()
    

class SetExtensionConfigurationSegmentResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__(None)

class SetExtensionRequiredConfigurationRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.POST
        scope = Scope.Channel.Manage.Redemptions
        authorization = Utils.AuthRequired.USER
        endPoint ="//channel_points//custom_rewards"
    

class SetExtensionRequiredConfigurationResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__()

class SendExtensionPubSubMessageRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.POST
        scope = Scope.Channel.Manage.Redemptions
        authorization = Utils.AuthRequired.USER
        endPoint ="//channel_points//custom_rewards"
    

class SendExtensionPubSubMessageResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__()

class GetExtensionLiveChannelsRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.POST
        scope = Scope.Channel.Manage.Redemptions
        authorization = Utils.AuthRequired.USER
        endPoint ="//channel_points//custom_rewards"
    

class GetExtensionLiveChannelsResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__()

class GetExtensionSecretsRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.POST
        scope = Scope.Channel.Manage.Redemptions
        authorization = Utils.AuthRequired.USER
        endPoint ="//channel_points//custom_rewards"
    

class GetExtensionSecretsResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__()

class CreateExtensionSecretRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.POST
        scope = Scope.Channel.Manage.Redemptions
        authorization = Utils.AuthRequired.USER
        endPoint ="//channel_points//custom_rewards"
    

class CreateExtensionSecretResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__()

class SendExtensionChatMessageRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.POST
        scope = Scope.Channel.Manage.Redemptions
        authorization = Utils.AuthRequired.USER
        endPoint ="//channel_points//custom_rewards"
    

class SendExtensionChatMessageResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__()

class GetExtensionsRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.POST
        scope = Scope.Channel.Manage.Redemptions
        authorization = Utils.AuthRequired.USER
        endPoint ="//channel_points//custom_rewards"
    

class GetExtensionsResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__()

class GetReleasedExtensionsRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.POST
        scope = Scope.Channel.Manage.Redemptions
        authorization = Utils.AuthRequired.USER
        endPoint ="//channel_points//custom_rewards"
    

class GetReleasedExtensionsResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__()

class GetExtensionBitsProductsRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.POST
        scope = Scope.Channel.Manage.Redemptions
        authorization = Utils.AuthRequired.USER
        endPoint ="//channel_points//custom_rewards"
    

class GetExtensionBitsProductsResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__()

class UpdateExtensionBitsProductRequest(Utils.RequestBaseClass):
        requestType = Utils.HTTPMethod.POST
        scope = Scope.Channel.Manage.Redemptions
        authorization = Utils.AuthRequired.USER
        endPoint ="//channel_points//custom_rewards"
    

class UpdateExtensionBitsProductResponse(Utils.ResponseBaseClass):
        def __init__(self) -> None:
            super().__init__()