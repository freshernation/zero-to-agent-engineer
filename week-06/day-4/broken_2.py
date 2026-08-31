# Should print:  Cost: $0.000225
#
# 50 input tokens at $3.00/M  = $0.00015
# 5 output tokens at $15.00/M = $0.000075
# total                       = $0.000225

INPUT_PER_MILLION = 3.00
OUTPUT_PER_MILLION = 15.00

input_tokens = 50
output_tokens = 5

cost = (
    input_tokens / 1_000_000 * INPUT_PER_MILLION
    + output_tokens / 1_000_000 * INPUT_PER_MILLION
)

print(f"Cost: ${cost:.6f}")
