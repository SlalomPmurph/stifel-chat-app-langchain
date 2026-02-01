# React Query Integration Guide

## Overview

This application uses **TanStack Query (React Query)** for server state management instead of direct Axios calls. This provides:

- ✅ Automatic caching and background updates
- ✅ Request deduplication
- ✅ Optimistic updates
- ✅ Built-in loading and error states
- ✅ Automatic retry logic
- ✅ DevTools for debugging

## Architecture

```
API Layer (Axios) → Custom Hooks (React Query) → Components
```

## File Structure

```
frontend/src/
├── services/              # API call functions (using Axios)
│   ├── api.js            # Axios instance
│   ├── chatService.js    # Chat API calls
│   ├── customerService.js # Customer API calls
│   └── chartService.js   # Chart API calls
├── hooks/                # React Query custom hooks
│   ├── useChatQueries.js     # Chat queries & mutations
│   ├── useCustomerQueries.js # Customer queries
│   └── useChartQueries.js    # Chart mutations
└── App.js                # QueryClientProvider setup
```

## Configuration

### QueryClient Setup (App.js)

```javascript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false, // Don't refetch on window focus
      retry: 1,                     // Retry failed requests once
      staleTime: 1000 * 60 * 5,    // Data fresh for 5 minutes
    },
  },
});
```

## Custom Hooks

### Chat Hooks (`useChatQueries.js`)

#### useCreateSession
Creates a new chat session.

```javascript
import { useCreateSession } from '../hooks/useChatQueries';

const MyComponent = () => {
  const createSession = useCreateSession();
  
  const handleCreate = async () => {
    try {
      const data = await createSession.mutateAsync('advisor-123');
      console.log('Session created:', data.session_id);
    } catch (error) {
      console.error('Failed to create session:', error);
    }
  };
  
  return (
    <button onClick={handleCreate} disabled={createSession.isPending}>
      {createSession.isPending ? 'Creating...' : 'Create Session'}
    </button>
  );
};
```

**Available states:**
- `isPending` - Mutation is in progress
- `isError` - Mutation failed
- `isSuccess` - Mutation succeeded
- `error` - Error object if failed
- `data` - Response data if successful

#### useSendMessage
Sends a chat message.

```javascript
import { useSendMessage } from '../hooks/useChatQueries';

const MyComponent = () => {
  const sendMessage = useSendMessage();
  
  const handleSend = async () => {
    try {
      const response = await sendMessage.mutateAsync({
        message: 'Hello!',
        advisorId: 'advisor-123',
        sessionId: 'session-456',
      });
      console.log('Response:', response.response);
    } catch (error) {
      console.error('Failed to send:', error);
    }
  };
  
  return (
    <button onClick={handleSend} disabled={sendMessage.isPending}>
      Send
    </button>
  );
};
```

**Features:**
- Automatically invalidates chat history on success
- Returns response with message and optional chart data

#### useChatHistory
Fetches chat history for a session.

```javascript
import { useChatHistory } from '../hooks/useChatQueries';

const MyComponent = ({ sessionId }) => {
  const { data, isLoading, error, refetch } = useChatHistory(sessionId);
  
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return (
    <div>
      {data?.messages.map(msg => (
        <div key={msg.id}>{msg.content}</div>
      ))}
      <button onClick={refetch}>Refresh</button>
    </div>
  );
};
```

**Available states:**
- `data` - The fetched data
- `isLoading` - Initial loading state
- `isFetching` - Any fetch (including background)
- `isError` - Query failed
- `error` - Error object
- `refetch()` - Manually refetch

### Customer Hooks (`useCustomerQueries.js`)

#### useCustomers
Fetches all customers for an advisor.

```javascript
import { useCustomers } from '../hooks/useCustomerQueries';

const CustomerList = ({ advisorId }) => {
  const { data: customers, isLoading, error } = useCustomers(advisorId);
  
  if (isLoading) return <div>Loading customers...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return (
    <ul>
      {customers?.map(customer => (
        <li key={customer.id}>{customer.name}</li>
      ))}
    </ul>
  );
};
```

**Features:**
- Automatically enabled when advisorId exists
- Cached for 10 minutes
- Invalidated when customer data changes

#### useCustomer
Fetches details for a specific customer.

```javascript
import { useCustomer } from '../hooks/useCustomerQueries';

const CustomerDetail = ({ customerId }) => {
  const { data: customer, isLoading } = useCustomer(customerId);
  
  if (isLoading) return <div>Loading...</div>;
  
  return (
    <div>
      <h2>{customer?.name}</h2>
      <p>Balance: ${customer?.balance}</p>
    </div>
  );
};
```

### Chart Hooks (`useChartQueries.js`)

#### useGenerateChart
Generates chart data.

```javascript
import { useGenerateChart } from '../hooks/useChartQueries';

const ChartGenerator = () => {
  const generateChart = useGenerateChart();
  
  const handleGenerate = async () => {
    try {
      const chartData = await generateChart.mutateAsync({
        dataType: 'accounts',
        filters: { advisorId: 'advisor-123' },
        chartType: 'bar',
      });
      console.log('Chart:', chartData);
    } catch (error) {
      console.error('Failed:', error);
    }
  };
  
  return (
    <button onClick={handleGenerate}>
      Generate Chart
    </button>
  );
};
```

## Query Keys

React Query uses query keys for caching and invalidation.

### Chat Keys
```javascript
chatKeys.all              // ['chat']
chatKeys.sessions()       // ['chat', 'sessions']
chatKeys.session(id)      // ['chat', 'session', id]
chatKeys.history(id)      // ['chat', 'history', id]
```

### Customer Keys
```javascript
customerKeys.all          // ['customers']
customerKeys.lists()      // ['customers', 'list']
customerKeys.list(id)     // ['customers', 'list', id]
customerKeys.details()    // ['customers', 'detail']
customerKeys.detail(id)   // ['customers', 'detail', id]
```

## Error Handling

### Component-Level
```javascript
const { data, error, isError } = useCustomers(advisorId);

if (isError) {
  return <Alert severity="error">{error.message}</Alert>;
}
```

### Mutation-Level
```javascript
const mutation = useSendMessage();

const handleSubmit = async () => {
  try {
    await mutation.mutateAsync(data);
  } catch (error) {
    // Handle error
    console.error(error);
  }
};

// Or use callbacks
mutation.mutate(data, {
  onSuccess: (data) => {
    console.log('Success:', data);
  },
  onError: (error) => {
    console.error('Error:', error);
  },
});
```

## Cache Invalidation

Invalidate queries when data changes:

```javascript
import { useQueryClient } from '@tanstack/react-query';
import { customerKeys } from '../hooks/useCustomerQueries';

const MyComponent = () => {
  const queryClient = useQueryClient();
  
  const handleUpdate = async () => {
    // Update customer...
    
    // Invalidate customers list
    await queryClient.invalidateQueries({ 
      queryKey: customerKeys.lists() 
    });
    
    // Or invalidate specific customer
    await queryClient.invalidateQueries({ 
      queryKey: customerKeys.detail(customerId) 
    });
  };
};
```

## Optimistic Updates

Update UI immediately before server responds:

```javascript
const queryClient = useQueryClient();

const mutation = useMutation({
  mutationFn: updateCustomer,
  onMutate: async (newData) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: customerKeys.detail(id) });
    
    // Snapshot current value
    const previous = queryClient.getQueryData(customerKeys.detail(id));
    
    // Optimistically update
    queryClient.setQueryData(customerKeys.detail(id), newData);
    
    // Return context with snapshot
    return { previous };
  },
  onError: (err, newData, context) => {
    // Rollback on error
    queryClient.setQueryData(
      customerKeys.detail(id), 
      context.previous
    );
  },
  onSettled: () => {
    // Refetch after success or error
    queryClient.invalidateQueries({ queryKey: customerKeys.detail(id) });
  },
});
```

## React Query DevTools

Access DevTools in development:
1. Look for the React Query icon in the bottom-right corner
2. Click to open the DevTools panel
3. View all queries, their status, and cached data
4. Manually trigger refetches or invalidations

## Best Practices

### 1. Use Specific Query Keys
```javascript
// Good
customerKeys.detail(customerId)

// Bad
['customer', customerId]
```

### 2. Handle Loading States
```javascript
if (isLoading) return <Skeleton />;
if (error) return <ErrorMessage error={error} />;
```

### 3. Use Enabled Option
```javascript
// Only fetch when ID exists
const { data } = useCustomer(customerId, {
  enabled: !!customerId,
});
```

### 4. Set Appropriate Stale Times
```javascript
// Frequently changing data
staleTime: 1000 * 30  // 30 seconds

// Rarely changing data
staleTime: 1000 * 60 * 10  // 10 minutes
```

### 5. Async/Await with Mutations
```javascript
// Good - handles errors properly
try {
  const data = await mutation.mutateAsync(payload);
  // Use data
} catch (error) {
  // Handle error
}

// Also good - callback style
mutation.mutate(payload, {
  onSuccess: (data) => {},
  onError: (error) => {},
});
```

## Migration from Axios

### Before (Direct Axios)
```javascript
const [data, setData] = useState(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);

useEffect(() => {
  const fetchData = async () => {
    setLoading(true);
    try {
      const result = await api.get('/endpoint');
      setData(result.data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };
  fetchData();
}, []);
```

### After (React Query)
```javascript
const { data, isLoading, error } = useQuery({
  queryKey: ['endpoint'],
  queryFn: () => api.get('/endpoint').then(res => res.data),
});
```

## Troubleshooting

### Query Not Refetching
- Check `staleTime` - data may still be fresh
- Check `enabled` option - query may be disabled
- Use DevTools to inspect query status

### Data Not Updating
- Verify cache invalidation after mutations
- Check query keys match exactly
- Use DevTools to see cache state

### Too Many Requests
- Increase `staleTime` to reduce refetches
- Set `refetchOnWindowFocus: false`
- Use `refetchOnMount: false` if appropriate

## Resources

- [TanStack Query Docs](https://tanstack.com/query/latest)
- [React Query DevTools](https://tanstack.com/query/latest/docs/react/devtools)
- [Query Keys Guide](https://tanstack.com/query/latest/docs/react/guides/query-keys)

---

**Happy Querying!** 🚀

