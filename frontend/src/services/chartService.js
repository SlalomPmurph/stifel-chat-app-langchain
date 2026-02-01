import api from './api';

export const chartService = {
  // Generate chart data
  generateChart: async ({ dataType, filters, chartType }) => {
    const response = await api.post('/api/v1/charts/generate', {
      data_type: dataType,
      filters,
      chart_type: chartType,
    });
    return response.data;
  },
};

export default chartService;

