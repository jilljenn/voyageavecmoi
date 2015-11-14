import {REQUEST_OFFERS, RECEIVE_OFFERS} from 'actions/OffersActions';
import _ from 'lodash';

export default function reduce(state = {
  isFetching: true,
  didInvalidate: false,
  items: []
}, action) {
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
        lastUpdated: actions.receivedAt
      });
    case INVALIDATE_OFFERS:
      return _.assign({}, state, {
        didInvalidate: true
      });
    default:
      return state;
  }
}
