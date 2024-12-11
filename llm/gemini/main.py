import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
import os

def generate():
    vertexai.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location=os.getenv("GOOGLE_CLOUD_LOCATION"))
    model = GenerativeModel(
        "gemini-1.5-flash-002",
    )
    responses = model.generate_content(
        [text1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    for response in responses:
        print(response.text, end="")

text1 = """Act as a panel of 3 experts on screenwriting. The panel will brainstorm ideas for a movie script. Each expert will share 1 step of their thinking with the group, then everyone goes to the next step, etc. If, at any point, one of the experts realizes their answer is not optimal or disagrees with the other two, then they leave. DO NOT DISPLAY THE EXPERTS\' DISCUSSION. Only output the final answer.

Goal: Based on the user\'s ideas, create a \"Save the Cat\" beat sheet that explains the storyline for a box-office hit movie in detail. Include a list of major characters.

Follow these rules carefully:
* Use a bulleted outline with Markdown for the plot points.
* Separate each section with a heading.
* Each plot point must have a scene description that includes actions and environment.
* Use a Markdown table for the characters.
* Each character must have an archetype, appearance description, a brief backstory, and a personality description.
* The descriptions must not be longer than 250 words.
* Adhere strictly to the word count constraint by utilizing this Python code, where the variable `text` refers to your output draft: `word_count = len(text.split())` Repeatedly revise your draft until it fits within the word count limit before generating the final output.
* DO NOT ACCESS THE INTERNET. The script must be completely original.

User Input:
I want to tell a heart-wrenching story about an urban coyote pack that lives in the leftover wild spaces squeezed between the American suburbs. The movie should make the viewer care about the environment and have compassion for animals sometimes seen as pests, but the emotional theme should be more about being strengthened by our relationships and dealing with the inevitable cycle of change. The main characters should be a family of coyotes, but supporting characters can be other urban wildlife such as raccoons, foxes, squirrels, or even stray cats and dogs. The animals cannot understand human speech, so do not include any scenes about talking to humans."""

generation_config = {
    "max_output_tokens": 1024,
    "temperature": 0.2,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]

generate()