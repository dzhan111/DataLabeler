# Quality Control
## Explanation:
The quality control module consists of two phases: the first is feeding a multimodal the input image and making it generate keywords, and the second is feeding these keywords plus the worker's transcription to an LLM, then that LLM decides if that fits the quality control standards (YES/NO). The voice recording also has to contain 80 words at minimum after transcription.

## Sample I/O:
Sample input:
[First image](./image1.png)

Sample output:

Sample input:

Sample output:

Sample input:

Sample output:

# Aggregation Sample I/O
## Explanation:
The aggregation module takes in n transcriptions and outputs a summarized dense caption.

## Sample I/O:
Sample input:

Sample output:

Sample input:

Sample output:

Sample input:

Sample output:
