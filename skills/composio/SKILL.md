---
name: composio
description: >
  Discover and connect to hundreds of third-party services through Composio's
  integration gateway. Trigger on Composio, "connect to a new tool", "find a
  tool for X", "integrate with [service]", or when a SaaS integration is needed
  that Claude doesn't have a dedicated connector for.
metadata:
  version: "2.0.0"
  category: operations
---

# Composio Operations

Discover, connect, and execute actions across hundreds of third-party SaaS services through Composio's universal integration gateway. Use Composio as the fallback when a dedicated MCP connector does not exist for the target service.

## When to Use Composio

Composio is the integration layer of last resort. Before using it:
1. Check if a dedicated MCP connector exists (Slack, Gmail, Google Drive, Monday.com, Buffer, Canva, etc.)
2. If a dedicated connector exists, use it — dedicated connectors are more reliable and better documented
3. Use Composio only when no dedicated connector covers the target service

Good Composio use cases at CTH:
- HubSpot CRM lookups when the dedicated integration is not configured
- Airtable data access for one-off projects
- Zendesk ticket management
- Trello board operations
- Mailchimp campaign management
- Any SaaS service the user needs to connect to ad-hoc

## Standard Workflow

### Step 1: Discover Available Tools

1. Call `COMPOSIO_SEARCH_TOOLS` with keywords describing the service or action
2. Review the returned tool list — each tool represents a specific action on a specific service
3. Note the tool names and their descriptions for the next steps

Search tips:
- Search by service name: "hubspot", "airtable", "zendesk"
- Search by action type: "create contact", "send email", "list records"
- Combine service and action: "hubspot create deal"

### Step 2: Check Connection Status

1. Call `COMPOSIO_MANAGE_CONNECTIONS` to see existing connections
2. Check if the target service already has an active connection
3. If connected, proceed to execution
4. If not connected, initiate the connection flow

### Step 3: Connect a New Service

If no connection exists for the target service:

1. Call `COMPOSIO_MANAGE_CONNECTIONS` to initiate OAuth or API key authentication
2. Guide the user through the authentication flow:
   - For OAuth: direct the user to the authorization URL and wait for callback
   - For API key: ask the user to provide their API key for the service
3. Call `COMPOSIO_WAIT_FOR_CONNECTIONS` to wait for the auth flow to complete
4. Verify the connection is active before proceeding

### Step 4: Execute Actions

1. Call `COMPOSIO_GET_TOOL_SCHEMAS` to get the exact parameters for the target action
2. Prepare the required parameters based on the schema
3. Call `COMPOSIO_MULTI_EXECUTE_TOOL` with the tool name and parameters
4. Handle the response — check for errors and extract the relevant data

## Tool Discovery Patterns

### Exploring a Service

When the user wants to know what is possible with a service:
1. Search for the service name to see all available actions
2. Group actions by category (CRUD, search, manage)
3. Present the capabilities to the user
4. Let them choose which actions to proceed with

### Finding the Right Action

When the user describes what they want to do:
1. Search with action-oriented keywords
2. If the first search is too broad, refine with service + action terms
3. Read the tool descriptions carefully — similar-sounding tools may have different behaviors
4. Verify the tool schema to confirm it does what is expected

## Advanced Features

### Remote Execution

Use `COMPOSIO_REMOTE_BASH_TOOL` for executing shell commands on Composio's remote environment when needed for complex integrations.

Use `COMPOSIO_REMOTE_WORKBENCH` for interactive development and testing of integration workflows.

### Batch Operations

Use `COMPOSIO_MULTI_EXECUTE_TOOL` for executing multiple actions in sequence:
- Combine related operations into a single call
- Handle dependencies between actions (e.g., create a contact, then add to a list)
- Process results from each action before proceeding to the next

## Connection Management

### Active Connections

Regularly check connection status before executing actions. Connections can expire or be revoked:
- OAuth tokens may expire — re-authenticate if needed
- API keys may be rotated — update if actions start failing
- Service permissions may change — verify access levels

### Multiple Accounts

Some services allow multiple connected accounts. When this occurs:
- List all connections for the service
- Ask the user which account to use
- Specify the connection ID in subsequent operations

## Error Handling

### Authentication Errors

If an action fails with an auth error:
1. Check the connection status
2. If expired, guide the user through re-authentication
3. Retry the action after re-connecting

### Permission Errors

If an action fails with a permission error:
1. Verify the connected account has the necessary permissions on the target service
2. Some actions require admin-level access — inform the user
3. Suggest alternative actions that may work with current permissions

### Rate Limiting

Composio may enforce rate limits per service:
- Space out bulk operations
- Implement retry logic with exponential backoff
- For large data pulls, paginate and process in batches

## Rules

- Always check for a dedicated MCP connector before falling back to Composio
- Verify connection status before every execution session — do not assume connections persist
- Handle authentication errors gracefully — guide the user through re-auth rather than failing silently
- Read tool schemas before executing — parameter formats vary by service
- For sensitive operations (delete, bulk update), confirm with the user before executing

## Troubleshooting

- **Tool not found**: Broaden search terms. The tool name may not match the expected convention. Try searching by service name alone.
- **Connection failed**: Check if the service requires specific OAuth scopes or permissions. Verify the authorization URL is accessible.
- **Action returned empty results**: Verify the parameters match the schema exactly. Check that the connected account has data in the target service.
- **Timeout on execution**: Some service APIs are slow. Increase timeout if possible, or break the operation into smaller chunks.

For Composio tool categories and connection patterns, see references/.
