import requests
import json
import os

def update_jira_from_extracted_data(extracted_data, epic_key, jira_base_url, jira_token):
    """
    Updates Jira issues based on the extracted data (a list of features).
    
    The function:
      - Retrieves all issues in the epic with label "Train".
      - Deletes those issues whose Jira key is not present in the input extracted_data ("Numéro").
      - Creates new issues for features whose "Numéro" is not already present in Jira.
      - Updates existing issues (matched by Jira key == extracted_data["Numéro"]) with the info from extracted_data.
      
    Each feature in extracted_data is expected to be a dictionary with keys:
      - "Numéro", "summary", "Description", "customfield_13600", "customfield_14506"
    
    Args:
        extracted_data (list): List of feature dictionaries extracted from the PPT.
        epic_key (str): The Jira epic key.
        jira_base_url (str): The base URL of your Jira instance.
        jira_token (str): API token for Jira.
        project_key (str): The Jira project key.
        
    Returns:
        dict: A dictionary with counts for created, updated, deleted issues and total issues in the epic after updates.
    """



    def transform_applications(applications):
        """
        Transforms a comma-separated string or a list of strings into a list of dictionaries with a "value" key.
        
        For example:
        - "Acoustic, PF Data" becomes:
            [
                {"value": "Acoustic"},
                {"value": "PF Data"}
            ]
        - ["Acoustic", "PF Data"] becomes:
            [
                {"value": "Acoustic"},
                {"value": "PF Data"}
            ]
        """
        if not applications:
            return []
        
        # If it's a list, treat it as list of strings.
        if isinstance(applications, list):
            items = [str(item).strip() for item in applications if str(item).strip()]
        else:
            # Assume it's a string and split by comma.
            items = [item.strip() for item in applications.split(",") if item.strip()]
        
        return [{"value": item} for item in items]
    
    def upload_attachment(session, jira_base_url, issue_key, file_path):
        """
        Deletes any existing attachment on the issue with the same filename,
        then uploads the file as an attachment.
        """
        file_name = os.path.basename(file_path)
        # Retrieve existing attachments for the issue.
        issue_url = f"{jira_base_url}/rest/api/2/issue/{issue_key}?fields=attachment"
        r = session.get(issue_url)
        r.raise_for_status()
        attachments = r.json()['fields'].get('attachment', [])
        for att in attachments:
            if att.get("filename") == file_name:
                att_id = att.get("id")
                del_url = f"{jira_base_url}/rest/api/2/attachment/{att_id}"
                del_resp = session.delete(del_url)
                del_resp.raise_for_status()
                print(f"Deleted existing attachment '{file_name}' (id {att_id}) from issue {issue_key}")
        # Now upload the new attachment using a separate session.
        upload_url = f"{jira_base_url}/rest/api/2/issue/{issue_key}/attachments"
        upload_session = requests.Session()
        # Set only the necessary headers for file upload.
        upload_session.headers.update({
            "Authorization": f"Bearer {jira_token}",
            "X-Atlassian-Token": "no-check"
        })
        with open(file_path, "rb") as f:
            files = {"file": f}
            resp = upload_session.post(upload_url, files=files)
        resp.raise_for_status()
        return resp.json()

    def _create_issue(session, jira_base_url, summary, description, applications, scopes, numero):
        create_url = f"{jira_base_url}/rest/api/2/issue"
        customfield_13600 = transform_applications(applications)
        customfield_14506 = transform_applications(scopes)
        issue_data = {
            "fields": {
                "project": {
                    "id": "15401"
                },
                "summary": f"{numero} - {summary}",
                "description": description,
                "issuetype": {"name": "Feature"},   # or "Feature", as appropriate
                "customfield_10016": epic_key,      # Epic Link field (adjust if needed)
                #"labels": [], #Add Train, LPM,
                "customfield_13600": customfield_13600, # Applications
                "customfield_14506": customfield_14506         # Scopes field
                # Optionally, if you need the Jira issue key to match the feature's "Numéro",
                # you might set it here via some custom mechanism if your workflow supports it.
            }
        }
        resp = session.post(create_url, json=issue_data)
        print("Creating new jira...")
        # In some Jira setups, the key is automatically generated and may not be settable.
        resp.raise_for_status()
        return resp.json()
    

    def _update_issue(session, jira_base_url, issue_key, summary, description, applications, scopes, numero):
        update_url = f"{jira_base_url}/rest/api/2/issue/{issue_key}"

        customfield_13600 = transform_applications(applications)
        customfield_14506 = transform_applications(scopes)
        update_data = {
            "fields": {
                "summary": f"{numero} - {summary}",
                "description": description,
                "customfield_13600": customfield_13600,
                "customfield_14506": customfield_14506
            }
        }
        resp = session.put(update_url, json=update_data)
        resp.raise_for_status()
        print("Updating Jira " + issue_key + " ...")
        return resp.json()

    def _delete_issue(session, jira_base_url, issue_key):
        delete_url = f"{jira_base_url}/rest/api/2/issue/{issue_key}"
        resp = session.delete(delete_url)
        resp.raise_for_status()
        return {"deleted": issue_key}
    
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {jira_token}",
        "Content-Type": "application/json"
    })

    # Retrieve existing issues in the epic that have label "Train"
    jql = f'"Epic Link" = "{epic_key}"' #AND labels = "Train"
    search_url = f"{jira_base_url}/rest/api/2/search"
    params = {"jql": jql, "fields": "summary"}
    response = session.get(search_url, params=params)
    existing_issues = response.json().get("issues", [])
    
    # Map existing issues by their key (which should correspond to extracted_data "jiraID")
    existing_by_num = {}
    for issue in existing_issues:
        # Jira key is assumed to be equal to the feature "jiraID"
        key = issue["key"]
        existing_by_num[key] = issue
    # Build a set of "Numéro" values from the input extracted data.
    input_numbers = {feature["jiraID"] for feature in extracted_data}

    created_count = 0
    updated_count = 0
    deleted_count = 0

        # We'll build a mapping: extracted jiraID -> {"jira_issue_key": ..., "Numero": ...}
    features_issue_map = {}

    """
    # Delete Jira issues that are not present in the extracted input.
    for jira_key in list(existing_by_num.keys()):
        if jira_key not in input_numbers:
            _delete_issue(session, jira_base_url, jira_key)
            deleted_count += 1
    """
    # For each feature in extracted_data, create new or update existing Jira issue.

    for feature in extracted_data:
        num = feature.get("jiraID")
        numero = feature.get("Numéro")
        summary = feature.get("summary")
        description = feature.get("Description")
        applications = feature.get("customfield_13600", "")
        scopes = feature.get("customfield_14506", "")
    

        if num in existing_by_num:
            try:
                _update_issue(session, jira_base_url, num, summary, description, applications, scopes, numero)
            except Exception as e:
                    print(f"Error updating {num} issue. {e}")
            features_issue_map[num] = numero
            updated_count += 1
        else:
            try:
                created_resp = _create_issue(session, jira_base_url, summary, description, applications, scopes, numero)
                new_key = created_resp.get("key")
                features_issue_map[new_key] = numero
                created_count += 1
            except Exception as e:
                print(f"Error creating {numero} issue. {e}")


    total_after = len(existing_issues) - deleted_count + created_count

    
    # Now upload attachments (images) to each Jira issue.
    for k, v in features_issue_map.items():
        # List all .png files in the output folder that start with the feature's "Numéro"
        for filename in os.listdir("/tmp/output"):
            if filename.lower().endswith(".png") and filename.startswith(v):
                file_path = os.path.join("/tmp/output", filename)
                try:
                    upload_attachment(session, jira_base_url, k, file_path)
                    print(f"Uploaded attachment {filename} to issue {k}")
                except Exception as e:
                    print(f"Failed to upload {filename} to issue {k}: {e}")
    
                    
    return {
        "created": created_count,
        "updated": updated_count,
        "deleted": deleted_count,
        "total_in_epic_after": total_after
    }
