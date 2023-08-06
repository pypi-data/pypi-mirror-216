from typing import Dict, List, Union

from cerebrium.models.base import BaseModel


class HFPipeline(BaseModel):
    def predict(self, input: Union[Dict, List]) -> list:
        if isinstance(input, dict):
            print("input: ", input)
            data = input["data"]
            params = input.get("parameters", {})
        else:
            data = input
            params = {}
        res = self.model(data, **params)
        return res
