import api from './api';

export const customerService = {
  // Get all customers for an advisor
  getCustomers: async (advisorId) => {
    const response = await api.get('/api/v1/customers', {
      params: { advisor_id: advisorId },
    });
    return response.data;
  },

  // Get specific customer details
  getCustomerById: async (customerId) => {
    const response = await api.get(`/api/v1/customers/${customerId}`);
    return response.data;
  },
};

export default customerService;

