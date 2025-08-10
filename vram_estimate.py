# Python memory estimation calculation
def estimate_vram_usage(params_billion, quantization_bits=4, context_length=4096):
    """
    Estimate VRAM usage for Ollama models

    Args:
        params_billion: Model parameters in billions
        quantization_bits: Quantization level (4, 8, 16)
        context_length: Maximum context window

    Returns:
        Estimated VRAM usage in GB
    """
    # Base model size
    model_size_gb = (params_billion * quantization_bits) / 8

    # KV cache size (varies by architecture)
    kv_cache_size_gb = (context_length * params_billion * 0.125) / 1024

    # Operating overhead
    overhead_gb = 1.5

    total_vram = model_size_gb + kv_cache_size_gb + overhead_gb
    return round(total_vram, 2)

# Example calculations for popular models
models = {
    "deepseek-r1:8b": 8,
    "llama3.3:70b": 70,
    "qwen2.5:32b": 32,
    "gemma2:27b": 27
}

for model, params in models.items():
    vram_q4 = estimate_vram_usage(params, 4)
    vram_q8 = estimate_vram_usage(params, 8)
    print(f"{model}: {vram_q4}GB (Q4) | {vram_q8}GB (Q8)")