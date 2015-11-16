export const API_ERROR = 'API_ERROR';
export function apiError(error) {
  return {
    type: API_ERROR,
    error
  };
}
