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

*Transcription 1:*There are two teams that are in the middle of a tackle. One of the teams is wearing white with yellow helmets with a B on the side of their helmets. The other team is black with red accents. It appears that the black team is running the ball while the white team is trying to tackle them. There are four black players, one of which is running the ball. Three others are trying to push the white players off and there are six white players attempting to tackle the black player who is running the ball. The black player is holding the ball in his left hand and they appear to be around center field. It is a sunny day and the turf is grass. The runner running back appears to have Jordan Brand gloves and the visible numbers for the two white players who are how they're back facing the camera on R32 and 11.


*Transcription 2:*  This image is a very high quality resolution image of what seems to be a football game between two teams. There's one team has white jerseys with green numbers and they also have white pants with green and yellow stripes. This team has yellow helmets with a logo that looks like a B in white. The other team is dressed mostly in black with their pants having red and white stripes. This seems to be a not an NFL football game as the logos don't seem to match. It seems to be either a high school or a college game. This football game is taking place on a turf as evidenced by the green floor. There doesn't seem to be bleachers but there seems to be crowd at the gate. In the far back around there's a security guard who are in cowboy hat and this is taking place during the day.


*Transcription 3:*  Many players are currently involved in a football play. One person is holding the ball. They are wearing a black jersey with red stripes, and their helmet is gray. They are carrying the ball into a group of players wearing white that are trying to stop him from moving any further. The players wearing white also have yellow stripes on their pants and are wearing green socks. Their uniform is mainly white and green, and their helmet is yellow. In the background, there are trees, and it looks like they are playing on a turf ground. It also looks like there are five white players on the white team, and four players on the black team currently in the image, and the referee is standing behind them with his head sticking out. There is an audience watching in the background, but they are out of focus.

**Sample QC output:**
1. Keywords: Football, Tackle, High School,Defense, Players, Uniforms, Action, Field, Teamwork, Competition
   
2.a. Transcription 1 contains 8 out of 10 keywords (and 154 total words), so the model would output <`YES`> and therefore <`PASS`> the quality control test.

2.b. Transcription 2 contains 9 out of 10 keywords (and 161 total words), so the model would output <`YES`> and therefore <`PASS`> the quality control test.

2.c. Transcription 3 contains 8 out of 10 keywords (and 169 total words), so the model would output <`YES`> and therefore <`PASS`> the quality control test.

**Sample aggregation output:**
There are two teams in the middle of a tackle, with the Black and Red team, primarily dressed in black jerseys with red accents on their pants featuring red and white stripes, attempting to advance the ball. Their gray helmets are adorned with no visible logo. Their opponents, the White team, are clad in white jerseys with green numbers, paired with white pants featuring green and yellow stripes, and yellow helmets with a white logo resembling a letter B on the side. It appears that the Black and Red team is running with the ball, with six White team players trying to tackle them. Four Black and Red team players are attempting to push off their White team counterparts. The runner is holding the ball in his left hand and seems to be around the 50-yard line area. He is wearing Jordan Brand gloves. The visible numbers for the White team players with their backs to the camera are R32 and 11. The game is being played on a sunny day, with the turf field covered in grass. There is a security guard wearing a cowboy hat standing near the gate, which is in close proximity to the tree line. The referee is positioned behind the players, and there is a crowd gathered near the gate, watching the game.
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
