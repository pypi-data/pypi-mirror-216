from onnxruntime import InferenceSession

from cerebrium.models.base import BaseModel


class OnnxModel(BaseModel):
    def __init__(self, model: InferenceSession):
        super().__init__(model)
        self.output_names = [output.name for output in self.model.get_outputs()]

    def predict(self, onnx_input: dict) -> list:
        res = self.model.run(self.output_names, onnx_input)
        return res[0].tolist()
