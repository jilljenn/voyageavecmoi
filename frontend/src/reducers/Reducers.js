import {combineReducers} from 'redux';

import offer from './OffersReducer.js';

function offers(state = {}, action) {
  switch (action.type) {
    case REQUEST_OFFERS:
    case RECEIVE_OFFERS:
    case INVALIDATE_OFFERS:
      return _.assign({}, state, {
        offers: offer(state.offer, action)
      });
    default:
      return state;
  }
}

const travelApp = combineReducers({
  offers
});

export default travelApp;
