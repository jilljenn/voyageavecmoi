import {combineReducers} from 'redux';
import {FILTER_OFFER, INVALIDATE_OFFERS, REQUEST_OFFERS, RECEIVE_OFFERS} from 'actions/OffersActions';

import _ from 'lodash';

import offers from './OffersReducer.js';

const travelApp = combineReducers({
  offers
});

export default travelApp;
