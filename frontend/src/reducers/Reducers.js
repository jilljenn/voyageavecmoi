import {combineReducers} from 'redux';

import _ from 'lodash';

import offers from './OffersReducer.js';
import cities from './CitiesReducer.js';

const travelApp = combineReducers({
  offers,
  cities
});

export default travelApp;
