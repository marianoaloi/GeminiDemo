In my workstation using a RTX 2060 12GB, and JAX .

The line 

```
gemma_lm = keras_nlp.models.GemmaCausalLM.from_preset("gemma_2b_en")
```

finish with error 

```
Traceback (most recent call last):
  File "/opt/maloi/ml/Gemma_KerasNLP/index.py", line 12, in <module>
    gemma_lm = keras_nlp.models.GemmaCausalLM.from_preset("gemma_2b_en")
  [my venv]/keras_nlp/src/models/task.py", line 258, in from_preset
    return super(cls, calling_cls).from_preset(*args, **kwargs)
  [my venv]/keras_nlp/src/models/task.py", line 258, in from_preset
    return super(cls, calling_cls).from_preset(*args, **kwargs)
  [my venv]/keras_nlp/src/models/task.py", line 227, in from_preset
    backbone = load_from_preset(
  [my venv]/keras_nlp/src/utils/preset_utils.py", line 192, in load_from_preset
    layer.load_weights(weights_path)
  [my venv]/keras/src/utils/traceback_utils.py", line 123, in error_handler
    raise e.with_traceback(filtered_tb) from None
  [my venv]/keras_nlp/src/layers/modeling/reversible_embedding.py", line 144, in load_own_variables
    self.embeddings.assign(store["0"])
KeyError: '0'
```
