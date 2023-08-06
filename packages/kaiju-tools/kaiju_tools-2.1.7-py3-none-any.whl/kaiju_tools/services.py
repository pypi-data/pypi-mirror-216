from kaiju_tools.app import *  # noqa: legacy
from kaiju_tools.rpc import JSONRPCServer, AbstractRPCCompatible  # noqa: legacy
from kaiju_tools.http import RPCClientService, HTTPService
from kaiju_tools.sessions import SessionService, LoginService, AuthenticationService

service_class_registry.register_class(LoggingService)
service_class_registry.register_class(Scheduler)
service_class_registry.register_class(SessionService)
service_class_registry.register_class(LoginService)
service_class_registry.register_class(AuthenticationService)
service_class_registry.register_class(JSONRPCServer)
service_class_registry.register_class(HTTPService)
service_class_registry.register_class(RPCClientService)
