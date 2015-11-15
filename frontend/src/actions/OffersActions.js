import moment from 'moment';
import axios from 'axios';

export const REQUEST_OFFERS = 'REQUEST_OFFERS';
export function requestOffers() {
  return {
    type: REQUEST_OFFERS
  };
}

export const REQUEST_OFFERS_BY_CITY = 'REQUEST_OFFERS_BY_CITY';
export function requestOffersByCity(city) {
  return {
    type: REQUEST_OFFERS_BY_CITY,
    city
  }
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

export const MERGE_NEW_OFFERS = 'MERGE_NEW_OFFERS';
export function mergeNewOffers(offers) {
  return {
    type: MERGE_NEW_OFFERS,
    offers
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

export function fetchOffers() {
  return (dispatch, getState) => {
    dispatch(requestOffers());
    return axios.get('/api/offers')
      .then(resp => dispatch(receiveOffers(resp.data)));
  }
}

export function fetchOffersByCity(city) {
  if (city === '') {
    return fetchOffers();
  }

  return dispatch => {
    dispatch(requestOffersByCity(city));
    return axios.get(`/api/offers/${city}`)
      .then(resp => dispatch(receiveOffers(resp.data)));
  }
}

export function fetchMoreOffers(start) {
  return (dispatch, getState) => {
    const state = getState();
    let promise = null;

    if (state.currentCity !== '') {
      dispatch(requestOffersByCity(state.currentCity))
      promise = axios.get(`/api/offers/${city}`, {
        params: {
          page: start
        }
      });
    } else {
      dispatch(requestOffers());
      promise = axios.get('/api/offers', {
        params: {
          page: start
        }
      });
    }

    return promise.then(resp => dispatch(mergeNewOffers(resp.data)));
  }
}

export const FILTER_OFFER = 'FILTER_OFFER';
export function filterOffer(text) {
  return {
    type: FILTER_OFFER,
    text
  }
}
