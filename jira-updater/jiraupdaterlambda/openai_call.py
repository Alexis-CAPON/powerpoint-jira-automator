from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API"))


def openAICall(userInput):
    response = client.responses.create(
    model="gpt-4o",
    input=[
        {
        "role": "system",
        "content": [
            {
            "type": "input_text",
            "text": "You are provided with extracted data from a PowerPoint presentation. The data consists of three parts:\n\n1. **config** - configuration, where it contain the visa url link:\n- **VISA**\n\n2. **functionalities** – a list of feature dictionaries, where each feature contains the following fields:  \n   - **Numéro**  \n   - **ID Jira**  \n   - **Nom**  \n   - **Hypothèses de bénéfices**  \n   - **Critères d’acceptance**  \n   - **Sizing SI (PI)**  \n\n3. **scopes** – a list of scope dictionaries, where each dictionary contains:  \n   - **Numéro**  \n   - **Scopes**  \n   - **Applications**  \n   - **Referents**  \n   - **Impacts / Architecture**\n\nThe **Impacts / Architecture** field in each scope entry is a text string in this format:  \nImpacts: 10, 11  \nArchitectures: 12, 13\n\nwhere the numbers represent slide numbers that should be converted into PNG images. Image references will be used in the final Jira issue description.\n\nYour task is to produce a JSON output that lists, for each feature (matched by its **Numéro**), all modifications required for Jira update. For each feature, include:\n- The **Numéro** and **Nom** (which will serve as the Jira summary).\n- A fully formatted **Description** field that follows this template:\n\n{panel:title=Objectif de la demande // Request goal|titleBGColor=#7768c7}\n * Besoin : <Insert what you understand of the need of the functionnality>\n{panel}\n{panel:title=Hypothèses de bénéfice // Profit hypothesis|titleBGColor=#7768c7}\n * [Insert each Hypothèses de bénéfices]\n{panel}\n{panel:title=Critères d'acceptance  // Acceptance criteria|titleBGColor=#7768c7}\n * [Insert each Critères d’acceptance]\n{panel}\n{panel:title=Images Architecture|titleBGColor=#7768c7}\n [For each slide number from the corresponding scope’s “Architectures” (e.g., for slide 12, insert: !<Numéro>_architecture_slide12.png|thumbnail!)]\n{panel}\n{panel:title=Images Impact|titleBGColor=#7768c7}\n [For each slide number from the corresponding scope’s “Impacts” (e.g., for slide 10, insert: !<Numéro>_impact_slide10.png|thumbnail!)]\n{panel}\n{panel:title=Lien vers la documentation // Link to the libraries|titleBGColor=#7768c7}\n[Insert VISA link here]\n{panel}\n{panel:title=Référents du Train // ART's Referents|titleBGColor=#7768c7}\nEpic Owner : [Insert Epic Owner]\nRelais RTE: [Insert RTE]\nRessource U&P: [Insert U&P]\n{panel}\n\n\nIn your output JSON, for each feature, replace the placeholders with actual values from the extracted data:\n- Use the feature’s **Hypothèses de bénéfices** and **Critères d’acceptance** fields in the description.\n- For the images section, use the **Numéro** of the feature along with the slide numbers parsed from the **Impacts / Architecture** field of the matching scope entry (matching by **Numéro**). For example, if a feature with **Numéro** \"E69F02\" has impacts on slides 10 and 11, include:\n  - !E69F02_impact_slide10.png!\n  - !E69F02_impact_slide11.png!\n- Do the same for the Architectures images.\n\nFinally, output the complete list of modifications (each feature with its summary and the fully formatted description) in JSON format. Assume that the current Jira data is not available; just produce the modifications based solely on the extracted data.\n\ncustomfield_13600 is for Applications field\ncustomfield_14506 is for Scopes field\n\n\nYour final JSON output should have an array of features where each feature is represented as:\n{\n  \"Numéro\": \"<feature number>\",\n  \"jiraID\": \"<ID Jira field>\",\n  \"summary\": \"<Nom field>\",\n  \"Description\": \"<fully formatted description with all placeholders replaced>\",\n  \"customfield_13600\": \"<list of Applications>\",\n  \"customfield_14506\": \"<list of Scopes>\",\n}"
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "input_text",
            "text": f"{userInput}"
            }
        ]
        }
    ],
    text={
        "format": {
        "type": "text"
        }
    },
    reasoning={},
    tools=[],
    temperature=1,
    max_output_tokens=5112,
    top_p=1,
    stream=False,
    store=False
    )
    return response.output[0].content[0].text

