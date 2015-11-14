import React from 'react';

import {TextInput} from 'belle';
import _ from 'lodash';

export default class OfferFilter extends React.Component {
  static propTypes = {
    onFilterUpdate: React.PropTypes.func.isRequired
  }

  updateFilter({value}) {
    _.debounce(() => {
      this.props.onFilterUpdate(value);
    }, 500)();
  }

  render() {
    return (
      <TextInput
        onUpdate={::this.updateFilter}
        placeholder="Filtrez par le contenu du tweet"
      />
    );
  }
}
