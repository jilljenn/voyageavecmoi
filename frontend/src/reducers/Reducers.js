import {combineReducers} from 'redux';

import _ from 'lodash';

import offers from './OffersReducer.js';
import cities from './CitiesReducer.js';
import error from './ErrorReducer.js';

const travelApp = combineReducers({
  offers,
  cities,
  error
});

export default travelApp;
