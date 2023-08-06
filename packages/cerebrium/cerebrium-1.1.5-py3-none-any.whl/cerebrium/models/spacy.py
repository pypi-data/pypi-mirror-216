from cerebrium.models.base import BaseModel


class SpacyModel(BaseModel):
    def predict(self, input: str) -> any:
        return self.model(input)
