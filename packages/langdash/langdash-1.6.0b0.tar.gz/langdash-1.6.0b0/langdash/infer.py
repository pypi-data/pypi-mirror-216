from dataclasses import dataclass


@dataclass
class InferArgs:
  """
  Data class for inference arguments.
  
  Attributes:
    min_new_tokens:
      Minimum number of new tokens to generate.
      If this is set, the `end` argument passed to the session's infer method
       will be interpreted as *a single token*. Special tokens count as an end token.
    max_new_tokens: Maximum number of new tokens to generate
    temperature: Temperature
    top_k: Top-K parameter. If set, generation defaults to top-K. Works with top_p
    top_p: Top-P parameter
    typical_mass: Mass parameter. If set, generation will use typical sampling
    max_rep_ctx: Maximum number of tokens to look back for repetition penalty
    rep_penalty: Repetition penalty, applied to logits for every repeated token
  """
  min_new_tokens: int = 0
  max_new_tokens: int = 512
  temperature: float = 1.0
  top_k: int = 0
  top_p: float = 0.
  typical_mass: float = 0.
  max_rep_ctx: int = 64
  rep_penalty: float = 1.0

  def __post_init__(self):
    assert self.min_new_tokens >= 0
    assert self.max_new_tokens >= 0
    assert 0.0 <= self.temperature <= 10.0
    assert 0 <= self.top_k
    assert 0.0 <= self.top_p <= 1.0
    assert 0.0 <= self.typical_mass <= 1.0
    assert 0 <= self.max_rep_ctx
    assert 0.0 <= self.rep_penalty <= 10.0
