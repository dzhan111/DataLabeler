# Sample Inputs and Outputs 
## Quality Control Module Explanation:
The quality control module consists of two phases: the first is feeding a multimodal the input image and making it generate keywords (labeled as 1. in the output), and the second is feeding these keywords plus the worker's transcription to an LLM, then that LLM decides if that fits the quality control standards (`YES/NO` depending on if it contains 2 out of the 10 keywords, but the exact number of keywords is subject to change later) (labeled as 2. in the output). The voice recording also has to contain 80 words at minimum after transcription.

## Aggregation Module Explanation:
The aggregation module takes in n transcriptions and outputs a summarized dense caption.


## Sample I/O:
**Sample input:**

![First image](./image1.jpeg)

*Transcription 1:* 

*Transcription 2:* 

*Transcription 3:* 

**Sample QC output:**
1. Keywords:
   
2.a. Transcription 1 contains X out of Y keywords (and Z total words), so the model would output <`YES/NO`> and therefore <`PASS/FAIL`> the quality control test.

2.b. Transcription 2 contains X out of Y keywords (and Z total words), so the model would output <`YES/NO`> and therefore <`PASS/FAIL`> the quality control test.

2.c. Transcription 3 contains X out of Y keywords (and Z total words), so the model would output <`YES/NO`> and therefore <`PASS/FAIL`> the quality control test.

**Sample aggregation output:**

---
**Sample input:**

![Second image](./image2.jpg)

*Transcription 1:* "There is a woman standing in the middle of a field in front of a back scape of a city. It appears to be wheat. The color of the wheat is golden. The woman is holding a stick standing in the statue like a position. She is wearing a blouse with vertical stripes and a blue pair of bottoms. She has frizzy hair and she is looking to the right. The city in the background is very gray and there are many tall buildings all rectangular shaped. She is holding a staff which is a straight staff."

*Transcription 2:* "This photo seems to be some woman on some sort of wheat or hay field. It's a beige or yellow color. The field dominates the foreground and the mid-ground and the woman seems to be in the foreground. She seems to be wearing a pink and white striped color shirt with blue pants. She seems to be holding a long stick in her left hand. She seems to be a white woman with brown hair. In the background there is a city. It seems to be blurred into the fog. There's some construction in the very far background. In the mid-ground there's some more visible construction. They seem to be building new buildings. City seems to be New York-esque, very foggy. It seems unusual that the woman is in the foreground with all this hay with this city background."

*Transcription 3:* "In this photo, we can see a woman in a wheat field. She is wearing a blue skirt and a white, coloured t-shirt that has coloured stripes. We can see her carrying a stick that seems like a wheat harvesting pool in her left hand and standing in a firm pose. She is looking at the wheat field as if she is determined to either harvest or protect the field. In the background, we can see a bunch of buildings in what scenes the women had in New York. The photo seems to be old given the quality of the photo. And the other doesn't seem to be sunny, it seems like it's cloudy and kind of ominous. We can see a bunch of digging happening in the background once used to be a construction site. And we can see the buildings varying in sizes and shapes. Some of the buildings seem to be blue, some of the buildings seem to be white, and we can see what seemed to be the twin towers in the background."

**Sample QC output:**
1. Keywords: `Wheat, Woman, Stick, Blouse, Blue, Skyscrapers, Skirt, Buildings, Manhattan, Field`

2.a. Transcription 1 contains 7 out of 10 keywords (and 97 total words), so the model would output `YES` and therefore pass the quality control test.
  
2.b. Transcription 2 contains 7 out of 10 keywords (and 139 total words), so the model would output `YES` and therefore pass the quality control test.
  
2.c. Transcription 3 contains 7 out of 10 keywords (and 177 total words), so the model would output `YES` and therefore pass the quality control test.

**Sample aggregation output:**

"A woman stands tall in the center of a golden wheat field, her figure evoking a sense of stillness. Behind her, the wheat stretches out as far as the eye can see. She wears a blouse with vertical stripes, paired with a blue pair of pants, and her frizzy hair falls in loose waves around her face. Her gaze is fixed on the right as she holds a straight staff in her hand. In the background, a gray and foreboding cityscape rises, its rectangular and varying-sized buildings looming above the fog. The contrast between the natural and urban environments is striking, with the woman's rustic attire and the staff she holds suggesting a deep connection to the land. Yet, the city's encroaching presence, marked by the sounds of construction in the distance, serves as a reminder that this balance is tenuous at best. The overall atmosphere is one of unease and foreboding, with the cloudy skies and muted color palette adding to the sense of tension. Despite the ominous tone, the woman's determined expression and the quiet dignity with which she stands suggests a sense of resilience in the face of change. Her presence serves as a poignant reminder of the fragility of the natural world and the importance of preserving it in the face of urban progress."


---
**Sample input:**

![Third image](./image3.jpg)

*Transcription 1:* 

*Transcription 2:* 

*Transcription 3:* 

**Sample QC output:**
1. Keywords:
   
2.a. Transcription 1 contains X out of Y keywords (and Z total words), so the model would output <`YES/NO`> and therefore <`PASS/FAIL`> the quality control test.

2.b. Transcription 2 contains X out of Y keywords (and Z total words), so the model would output <`YES/NO`> and therefore <`PASS/FAIL`> the quality control test.

2.c. Transcription 3 contains X out of Y keywords (and Z total words), so the model would output <`YES/NO`> and therefore <`PASS/FAIL`> the quality control test.

**Sample aggregation output:**

---
**Sample input:**

![Fourth image](./image4.jpg)

*Transcription 1:* 

*Transcription 2:* 

*Transcription 3:* 

**Sample QC output:**
1. Keywords:
   
2.a. Transcription 1 contains X out of Y keywords (and Z total words), so the model would output <`YES/NO`> and therefore <`PASS/FAIL`> the quality control test.

2.b. Transcription 2 contains X out of Y keywords (and Z total words), so the model would output <`YES/NO`> and therefore <`PASS/FAIL`> the quality control test.

2.c. Transcription 3 contains X out of Y keywords (and Z total words), so the model would output <`YES/NO`> and therefore <`PASS/FAIL`> the quality control test.

**Sample aggregation output:**

---
