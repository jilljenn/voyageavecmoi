import {FILTER_OFFER, INVALIDATE_OFFERS, REQUEST_OFFERS, RECEIVE_OFFERS} from 'actions/OffersActions';
import _ from 'lodash';

const initialState = {
  isFetching: true,
  didInvalidate: false,
  items: []
}

export default function reduce(state = initialState, action) {
  switch (action.type) {
    case REQUEST_OFFERS:
      return _.assign({}, state, {
        isFetching: true,
        didInvalidate: false
      });
    case RECEIVE_OFFERS:
      return _.assign({}, state, {
        isFetching: false,
        didInvalidate: false,
        items: action.offers,
        lastUpdated: action.receivedAt
      });
    case INVALIDATE_OFFERS:
      return _.assign({}, state, {
        didInvalidate: true
      });
    case FILTER_OFFER:
      return _.assign({}, state, {
        currentFilter: action.text
      });
    default:
      return state;
  }
}
