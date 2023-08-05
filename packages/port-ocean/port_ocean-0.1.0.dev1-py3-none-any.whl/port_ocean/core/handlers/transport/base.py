from abc import abstractmethod
from typing import List

from port_ocean.clients.port.types import UserAgentType
from port_ocean.core.base import BaseWithContext
from port_ocean.core.models import Entity
from port_ocean.types import EntityDiff


class BaseTransport(BaseWithContext):
    DEFAULT_USER_AGENT_TYPE = UserAgentType.exporter

    @abstractmethod
    async def update_diff(
        self,
        entities: EntityDiff,
        user_agent: UserAgentType | None = None,
    ) -> None:
        pass

    @abstractmethod
    async def upsert(
        self, entities: List[Entity], user_agent_type: UserAgentType
    ) -> None:
        pass

    @abstractmethod
    async def delete(
        self, entities: List[Entity], user_agent_type: UserAgentType
    ) -> None:
        pass

    @abstractmethod
    async def delete_diff(
        self, entities: List[Entity], user_agent: UserAgentType
    ) -> None:
        pass
