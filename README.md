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

| **[Guides](docs/guides)** | **[Architecture and Features](docs/architecture.md)** | **[APIs](lib/bindings/python/README.md)** | **[Deployment](deploy/jira-automator/README.md)** |

PowerPoint Jira Automator is a tool designed to automate Jira operations such as creating, updating, and removing features from an epic using a PowerPoint VISA as a referential document. This enables teams to efficiently manage their Jira workflows based on structured VISA presentations.

### Key Features

- **Automated Epic Management** – Create, update, and delete features under an epic based on VISA slides.
- **PowerPoint Parsing** – Extract structured information from PowerPoint VISA to define Jira tasks.
- **Jira API Integration** – Connect seamlessly with Jira Cloud or Jira Server using REST APIs.
- **Customizable Workflow Rules** – Define business logic for Jira automation directly from your VISA documents.
- **Docker & AWS Deployable** – Easily run the automation in local or cloud environments.

## Installation

### Prerequisites

Ensure you have the following installed:

- **Python 3.8+**
- **pip**
- **Docker (optional for deployment)**
- **Jira API Token** (for authentication)

### Setup

```bash
# Clone the repository
git clone https://github.com/Alexis-CAPON/jira-automator.git
cd jira-automator

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

The application requires environment variables to be set for Jira authentication and other configurations.
Create a `.env` file in the root directory with the following values:

```env
JIRA_BASE_URL=https://yourcompany.atlassian.net
JIRA_TOKEN=your_api_token
OPENAI_API=your_token
```

## Running Locally

You can run the PowerPoint Jira Automator locally using the command:

```bash
python main.py --visa /path/to/visa.pptx --epic EPIC-123
```

### Example Usage

```bash
python main.py --visa feature-roadmap.pptx --epic ENG-456
```

## Docker Deployment

Build and run the application using Docker:

```bash
# Build the Docker image
docker build -t jira-automator .

# Run the container
docker run --env-file .env -v /path/to/visa/files:/data jira-automator --visa /data/visa.pptx --epic EPIC-789
```

## AWS SAM Deployment

To deploy on AWS Lambda using AWS SAM:

```bash
cd deploy/aws-sam
sam build
sam deploy --guided
```

## API Reference

The PowerPoint Jira Automator also provides an API for integration with CI/CD pipelines. Refer to the [API documentation](docs/api.md) for details.

## License

PowerPoint Jira Automator is released under the [Apache 2.0 License](http://www.apache.org/licenses/LICENSE-2.0).

## Contributing

We welcome contributions! Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting issues, features, or pull requests.

## Support

Create a ticket if you need help.
