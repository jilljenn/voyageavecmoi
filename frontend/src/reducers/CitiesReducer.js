import {REQUEST_CITIES, RECEIVE_CITIES} from 'actions/CitiesActions';
import _ from 'lodash';

const initialState = {
  isFetching: true,
  items: []
}

export default function reduce(state = initialState, action) {
  switch (action.type) {
    case REQUEST_CITIES:
      return _.assign({}, state, {
        isFetching: true
      });
    case RECEIVE_CITIES:
      return _.assign({}, state, {
        isFetching: false,
        items: action.cities,
        lastUpdated: action.receivedAt
      });
    default:
      return state;
  }
}
