import typing as t

if t.TYPE_CHECKING:
    from unchained.core import Unchained

from unchained.protocol import OrmModel


class ModelsCenter:
    def __init__(
        self,
        unchained: "Unchained",
        models: t.List[t.Type[OrmModel]] | None = None,
    ) -> None:
        self.unchained = unchained
        self.models = models

    def add_model(self, model: t.Type[OrmModel]) -> None:
        if self.models is None:
            self.models = []
        self.models.append(model)
