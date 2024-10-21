async function fetchAgentConversationData(agentId, startDate, endDate) {
  // Validate the agentId
  console.log(`%c Fetching Agent Conversations metrics`, 'color: #2196f3')
  console.table({ agentId, startDate, endDate });
 
  // set the dat  in ' ${startDate}:00.000Z' format
  //const now = new Date();
  const startOfMonth = `${startDate}:00.000Z` //new Date(now.getFullYear(), now.getMonth(), 1).toISOString();

  const endOfMonth = `${endDate}:00.000Z` //new Date(now.getFullYear(), now.getMonth() + 1, 0, 23, 59, 59).toISOString();

  const apiUrl = `https://vaultmarkets.freshchat.com/v2/metrics/historical?metric=conversation_metrics.resolved_interactions&start=${startOfMonth}&end=${endOfMonth}&filter_by=agent%3D${agentId}&group_by=agent`;

  // Prepare headers, retrieving the token from environment variables for security
  const headers = {
    'Accept': 'application/json',
    'Authorization': `Bearer eyJraWQiOiJjdXN0b20tb2F1dGgta2V5aWQiLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmcmVzaGNoYXQiLCJzdWIiOiIyNWQ0ZDViZS1kNDUyLTRjMTktOTRmZi1kYzI5MTE0NTZjODAiLCJjbGllbnRJZCI6ImZjLTBiMjNkZTZkLTM4YTYtNGJiMi1iMWE3LWJmNzBiODU3YTBmNiIsInNjb3BlIjoiYWdlbnQ6cmVhZCBhZ2VudDpjcmVhdGUgYWdlbnQ6dXBkYXRlIGFnZW50OmRlbGV0ZSBjb252ZXJzYXRpb246Y3JlYXRlIGNvbnZlcnNhdGlvbjpyZWFkIGNvbnZlcnNhdGlvbjp1cGRhdGUgbWVzc2FnZTpjcmVhdGUgbWVzc2FnZTpnZXQgYmlsbGluZzp1cGRhdGUgcmVwb3J0czpmZXRjaCByZXBvcnRzOmV4dHJhY3QgcmVwb3J0czpyZWFkIHJlcG9ydHM6ZXh0cmFjdDpyZWFkIGRhc2hib2FyZDpyZWFkIHVzZXI6cmVhZCB1c2VyOmNyZWF0ZSB1c2VyOnVwZGF0ZSB1c2VyOmRlbGV0ZSBvdXRib3VuZG1lc3NhZ2U6c2VuZCBvdXRib3VuZG1lc3NhZ2U6Z2V0IG1lc3NhZ2luZy1jaGFubmVsczptZXNzYWdlOnNlbmQgbWVzc2FnaW5nLWNoYW5uZWxzOm1lc3NhZ2U6Z2V0IG1lc3NhZ2luZy1jaGFubmVsczp0ZW1wbGF0ZTpjcmVhdGUgbWVzc2FnaW5nLWNoYW5uZWxzOnRlbXBsYXRlOmdldCBmaWx0ZXJpbmJveDpyZWFkIGZpbHRlcmluYm94OmNvdW50OnJlYWQgcm9sZTpyZWFkIGltYWdlOnVwbG9hZCIsImlzcyI6ImZyZXNoY2hhdCIsInR5cCI6IkJlYXJlciIsImV4cCI6MTk0MTUzMjgyNCwiaWF0IjoxNjI2MDAwMDI0LCJqdGkiOiIzYTI5OWE1Ni02NzFhLTRjOTEtYmQyMi1iMWIzM2JkZjE3YzUifQ.BPO3ofWd8eJF6NHGfp_Jf_APVwJonVpJRzIG5JdxOCA`, // Ensure you set this in your environment
    'Content-Type': 'application/json',
  };

  try {
    const response = await fetch(apiUrl, { headers });

    // Check if the response is successful
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API request failed with status ${response.status}: ${errorText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching agent conversation data:', error);
    throw error; // Re-throw the error after logging
  }
}

export { fetchAgentConversationData };