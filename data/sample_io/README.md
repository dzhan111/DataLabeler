# Quality Control
## Explanation:
The quality control module consists of two phases: the first is feeding a multimodal the input image and making it generate keywords, and the second is feeding these keywords plus the worker's transcription to an LLM, then that LLM decides if that fits the quality control standards (YES/NO). The voice recording also has to contain 80 words at minimum after transcription.

## Sample I/O:
Sample input:
[First image](./image1.jpg)

Sample output:

Sample input:
[Second image](./image2.jpg)

Sample output:

Sample input:
[Third image](./image3.jpg)

Sample output:

Sample input:
[Fourth image](./image4.jpg)

Sample output:

# Aggregation Sample I/O
## Explanation:
The aggregation module takes in n transcriptions and outputs a summarized dense caption.

## Sample I/O:
Sample input:
[First image](./image1.jpg)

Sample output:

Sample input:
[Second image](./image2.jpg)

Sample output:

Sample input:
[Third image](./image3.jpg)

Sample output:

Sample input:
[Fourth image](./image4.jpg)

Sample output:

