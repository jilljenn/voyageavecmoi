import moment from 'moment';
import axios from 'axios';

export const REQUEST_OFFERS = 'REQUEST_OFFERS';
export function requestOffers() {
  return {
    type: REQUEST_OFFERS
  };
}

export const RECEIVE_OFFERS = 'RECEIVE_OFFERS';
export function receiveOffers(offers) {
  return {
    type: RECEIVE_OFFERS,
    offers,
    receivedAt: moment()
  };
}

export const INVALIDATE_OFFERS = 'INVALIDATE_OFFERS';
export function invalidateOffers() {
  return {
    type: INVALIDATE_OFFERS
  }
}

export function fetchOffers() {
  return dispatch => {
    dispatch(requestOffers());
    return axios.get('/api/offers')
      .then(resp => dispatch(receiveOffers(resp.data)));
  }
}

function shouldFetchOffers(state) {
  const offers = state.offers;
  if (!offers) {
    return true;
  } else if (offers.isFetching) {
    return false;
  } else {
    return offers.didInvalidate;
  }
}

export function fetchOffersIfNeeded() {
  return (dispatch, getState) => {
    if (shouldFetchOffers(getState()) {
      return dispatch(fetchOffers());
    } else {
      return Promise.resolve();
    }
  }
}
