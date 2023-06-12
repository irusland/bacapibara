import uuid

from pydantic import BaseSettings
import numpy as np
import torch
from transformers import GPT2Tokenizer
from tritonclient.http import InferenceServerClient, InferInput
import torch.nn.functional as F


class TritonClientSettings(BaseSettings):
    url: str = 'localhost:8123'
    verbose: bool = True
    model_name: str = "onnx_gpt2_lm"
    model_version: str = "1"
    tokenizer_name: str = 'gpt2'
    batch_size: int = 1


class TritonClient:
    def __init__(self, triton_client_settings: TritonClientSettings):
        self._settings = triton_client_settings
        self._client = InferenceServerClient(url=self._settings.url, verbose=self._settings.verbose)
        self._tokenizer = GPT2Tokenizer.from_pretrained(self._settings.tokenizer_name)
        print(self._client.get_model_config(self._settings.model_name))

    def auto_complete(self, text: str, length: int = 30) -> str:
        tokens = np.array(self._tokenizer.encode(text))
        context = torch.tensor(tokens, dtype=torch.long).unsqueeze(0).repeat(self._settings.batch_size, 1).unsqueeze(0)
        output = context

        request_id = uuid.uuid4().hex

        for i in range(length):
            input_ids_data = np.array(output).astype(np.int64)
            inputs = []
            inputs.append(InferInput('input1', input_ids_data.shape, "INT64"))
            inputs[0].set_data_from_numpy(input_ids_data)

            outputs = []
            # outputs.append(InferRequestedOutput('output1', [-1,2], "FP32"))

            results = self._client.infer(
                self._settings.model_name,
                inputs,
                request_id=request_id,
                outputs=outputs,
                model_version=self._settings.model_version
            )
            outputs = torch.tensor(results.as_numpy('output1'))
            # ------------------------------------
            logits = outputs[0]
            logits = logits[:, -1, :]
            log_probs = F.softmax(logits, dim=-1)
            _, prev = torch.topk(logits, k=1, dim=-1)
            prev = prev.unsqueeze(0)
            output = torch.cat((output, prev), dim=2)

        # output = output[:, len(tokens):].tolist()
        output = output.squeeze(0).tolist()
        generated = 0
        print(output)
        for i in range(self._settings.batch_size):
            generated += 1
            text = self._tokenizer.decode(output[i])
            return text
