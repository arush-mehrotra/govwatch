// API service for GovWatch
const API_BASE_URL = 'https://govwatch.onrender.com';

// Function to search contracts with streaming response
export async function searchContractsStream(query: string): Promise<ReadableStream<Uint8Array> | null> {
  console.log(`Sending request to ${API_BASE_URL}/contracts/search with query:`, query);
  
  try {
    const response = await fetch(`${API_BASE_URL}/contracts/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
      mode: 'cors',
    });

    console.log('Search response status:', response.status);
    
    if (!response.ok) {
      const errorText = await response.text().catch(() => 'No error details available');
      console.error('API error response:', errorText);
      throw new Error(`API error: ${response.status} - ${errorText}`);
    }

    // For non-streaming API, convert the response to a stream
    const data = await response.json();
    console.log('Search response data:', data);
    
    // Create a readable stream from the result
    const { readable, writable } = new TransformStream();
    const writer = writable.getWriter();
    
    // Write the answer to the stream
    const answer = data.answer || "No answer provided";
    
    // Add sources information if available
    let responseText = answer;
    if (data.sources && data.sources.length > 0) {
      responseText += "\n\n--- Sources ---\n";
      data.sources.forEach((source: any, index: number) => {
        responseText += `\n${index + 1}. ${source.contract_url || 'Unknown source'} (${source.date || 'Unknown date'})`;
        if (source.section) {
          responseText += ` - ${source.section}`;
        }
      });
    }
    
    writer.write(new TextEncoder().encode(responseText));
    writer.close();
    
    return readable;
  } catch (error) {
    console.error('Error searching contracts:', error);
    
    // Enhanced error handling with specific messages
    if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
      throw new Error('Could not connect to the search service. The backend might be unavailable or CORS might be blocking the request.');
    }
    
    // For other errors, rethrow
    throw error;
  }
}

// Function to search contracts with regular response
export async function searchContracts(query: string): Promise<any> {
  console.log(`Sending request to ${API_BASE_URL}/contracts/search with query:`, query);
  
  try {
    const response = await fetch(`${API_BASE_URL}/contracts/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
      mode: 'cors',
    });

    console.log('Search response status:', response.status);
    
    if (!response.ok) {
      const errorText = await response.text().catch(() => 'No error details available');
      console.error('API error response:', errorText);
      throw new Error(`API error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    console.log('Search response data:', data);
    return data;
  } catch (error) {
    console.error('Error searching contracts:', error);
    
    // Enhanced error handling with specific messages
    if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
      throw new Error('Could not connect to the search service. The backend might be unavailable or CORS might be blocking the request.');
    }
    
    // For other errors, rethrow
    throw error;
  }
} 