import moment from 'moment';
import axios from 'axios';

export const REQUEST_CITIES = 'REQUEST_CITIES';
export function requestCities() {
  return {
    type: REQUEST_CITIES
  };
}

export const RECEIVE_CITIES = 'RECEIVE_CITIES';
export function receiveCities(cities) {
  return {
    type: RECEIVE_CITIES,
    cities,
    receivedAt: moment()
  };
}

export function fetchCities() {
  return dispatch => {
    dispatch(requestCities());
    return axios.get('/api/cities')
      .then(resp => dispatch(receiveCities(resp.data)));
  }
}
