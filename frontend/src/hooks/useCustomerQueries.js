import { useQuery } from '@tanstack/react-query';
import customerService from '../services/customerService';

// Query keys
export const customerKeys = {
  all: ['customers'],
  lists: () => [...customerKeys.all, 'list'],
  list: (advisorId) => [...customerKeys.lists(), advisorId],
  details: () => [...customerKeys.all, 'detail'],
  detail: (customerId) => [...customerKeys.details(), customerId],
};

// Hook to get all customers for an advisor
export const useCustomers = (advisorId, options = {}) => {
  return useQuery({
    queryKey: customerKeys.list(advisorId),
    queryFn: () => customerService.getCustomers(advisorId),
    enabled: !!advisorId,
    staleTime: 1000 * 60 * 10, // Consider data fresh for 10 minutes
    ...options,
  });
};

// Hook to get customer details
export const useCustomer = (customerId, options = {}) => {
  return useQuery({
    queryKey: customerKeys.detail(customerId),
    queryFn: () => customerService.getCustomerById(customerId),
    enabled: !!customerId,
    staleTime: 1000 * 60 * 10,
    ...options,
  });
};

