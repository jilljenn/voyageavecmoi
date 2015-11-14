import React from 'react';

import Offer from 'components/Offer.react';

import _ from 'lodash';

export default class OfferList extends React.Component {
  static propTypes = {
    offers: React.PropTypes.array.isRequired,
    currentFilter: React.PropTypes.string
  }

  render() {
    const {currentFilter, offers} = this.props;
    return (
      <section>
        {_.map(currentFilter ? _.filter(offers, offer => _.capitalize(offer.text).includes(_.capitalize(currentFilter))) : offers, offer => {
          return (
            <Offer
              key={offer.id}
              offer={offer}
            />
          );
        })}
      </section>
    );
  }
}
