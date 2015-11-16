import {API_ERROR} from 'actions/ErrorsActions';
import _ from 'lodash';

const initialState = {
  message: null,
  failed: false
}

function reduceAPIError(state, error) {
  if (error.status === 500 || error.status === 404) {
    return _.assign({}, state, {
      message: 'Un bug est arrivé, on est dessus!',
      failed: true
    });
  } else if (error.status === 400) {
    return _.assign({}, state, {
      message: 'Il semblerait que vous ayez fait une petite bêtise... ?',
      failed: true
    });
  }
}

export default function reduce(state = initialState, action) {
  switch (action.type) {
    case API_ERROR:
      return reduceAPIError(state, action.error);
    default:
      return state;
  }
}
