import React from 'react';

import Offer from 'components/Offer.react';

export default class OfferList extends React.Component {
  static propTypes = {
    offers: React.PropTypes.array.isRequired
  }

  render() {
    return (
      <section>
        {_.map(this.props.offers, offer => {
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
