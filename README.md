<!--
SPDX-FileCopyrightText: Copyright (c) 2025. All rights reserved.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# PowerPoint Jira Automator

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub Release](https://img.shields.io/github/v/release/Alexis-CAPON/jira-automator)](https://github.com/Alexis-CAPON/jira-automator/releases/latest)

| **[Deployment](deploy/jira-automator/README.md)** |

PowerPoint Jira Automator is a script designed to automate Jira operations such as creating, updating, and removing features from an epic using a PowerPoint VISA as a referential document. This enables teams to efficiently manage their Jira workflows based on structured VISA presentations.

### Key Features

- **Automated Epic Management** – Create, update, and delete features under an epic based on VISA slides.
- **PowerPoint Parsing** – Extract structured information from PowerPoint VISA to define Jira tasks.
- **Jira API Integration** – Connect seamlessly with Jira Cloud or Jira Server using REST APIs.
- **Customizable Workflow Rules** – Define business logic for Jira automation directly from your VISA documents.
- **Docker & AWS Deployable** – Easily run the automation in local or cloud environments.

## Installation

### Prerequisites

Ensure you have:

- **Python 3.8+**
- **pip**
- **Docker**
- **Jira API Token**
- **OpenAI API**

### BEFORE STARTING

This is a template for a AWS lambda deployment. You can take the code and modify it if you want to use it for another way.
You will need to link this AWS Lambda to your API Gateway.

You will find a powerpoint template in the github, modify it as you wish.
Before deploying to production you need to add your AWS secrey and modify them in the template.yaml

### Setup

```bash
# Clone the repository
git clone https://github.com/Alexis-CAPON/jira-automator.git
cd jira-updater

# Build the image
sam build --use-container

# Test the image if you want
sam local invoke -e events/event.json -n env.json JiraUpdaterFunction

# Deploy it
sam deploy
```

## Test Configuration

To test the application, it requires environment variables to be set for Jira authentication and other configurations.
Create a `env.json` file in the 'jira-update' directory with the following values:

```json
{
  "JiraUpdaterFunction": {
    "JIRA_BASE_URL": "",
    "JIRA_TOKEN": "",
    "OPENAI_API": ""
  }
}
```

## License

PowerPoint Jira Automator is released under the [Apache 2.0 License](http://www.apache.org/licenses/LICENSE-2.0).

## Support

Create a ticket if you need help.
