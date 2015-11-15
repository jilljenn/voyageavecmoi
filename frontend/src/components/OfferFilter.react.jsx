import React from 'react';

import {TextInput, ComboBox, Option} from 'belle';
import Radium from 'radium';

import _ from 'lodash';


@Radium
export default class OfferFilter extends React.Component {
  static propTypes = {
    cities: React.PropTypes.array.isRequired,
    currentCity: React.PropTypes.string,
    onFilterUpdate: React.PropTypes.func.isRequired,
    onCityUpdate: React.PropTypes.func.isRequired
  }

  updateFilter({value}) {
    _.debounce(() => {
      this.props.onFilterUpdate(value);
    }, 1000)();
  }

  updateCity({value}) {
    _.debounce(() => {
      this.props.onCityUpdate(value);
    }, 1000)();
  }

  render() {
    const {cities} = this.props;
    return (
      <section style={styles.filters}>
        {cities.length > 0 &&
          <ComboBox
            wrapperStyle={styles.cityBox}
            onUpdate={::this.updateCity}
            defaultValue={this.props.currentCity}
            placeholder="Choisissez une ville">
            {_.map(cities, city => {
              return (
                <Option
                  key={city}
                  value={city}
                >
                  {city}
                </Option>
              );
            })}
          </ComboBox>}
        <TextInput
          onUpdate={::this.updateFilter}
          placeholder="Filtrez par le contenu du tweet"
        />
      </section>
    );
  }
}

const styles = {
  filters: {
    display: 'flex'
  },
  cityBox: {
    paddingRight: '15px'
  }
};
