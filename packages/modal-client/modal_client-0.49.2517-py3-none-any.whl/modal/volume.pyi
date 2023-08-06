import __main__
import modal.object
import typing_extensions

class _VolumeHandle(modal.object._Handle):
    async def commit(self):
        ...

    async def reload(self):
        ...


class VolumeHandle(modal.object.Handle):
    def __init__(self):
        ...

    class __commit_spec(typing_extensions.Protocol):
        def __call__(self):
            ...

        async def aio(self, *args, **kwargs):
            ...

    commit: __commit_spec

    class __reload_spec(typing_extensions.Protocol):
        def __call__(self):
            ...

        async def aio(self, *args, **kwargs):
            ...

    reload: __reload_spec


class _Volume(modal.object._Provider[_VolumeHandle]):
    def __init__(self) -> None:
        ...


class Volume(modal.object.Provider[VolumeHandle]):
    def __init__(self) -> None:
        ...
