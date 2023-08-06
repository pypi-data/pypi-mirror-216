#
#  Copyright (c) 2018-2022 Renesas Inc.
#  Copyright (c) 2018-2022 EPAM Systems Inc.
#


class OnUnitError(Exception):
    pass


class UserCredentialsError(OnUnitError):
    pass


class DeviceRegisterError(OnUnitError):
    pass


class DeviceDeregisterError(OnUnitError):
    pass


class UnitError(OnUnitError):
    pass


class GrpcUnimplemented(OnUnitError):
    pass


class CloudAccessError(OnUnitError):
    pass


class AosProvError(OnUnitError):
    pass
