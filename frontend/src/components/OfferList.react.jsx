import React from 'react';

import Offer from 'components/Offer.react';
import Infinite from 'react-infinite';
import Halogen from 'halogen';
import Radium from 'radium';

import _ from 'lodash';

@Radium
export default class OfferList extends React.Component {
  static propTypes = {
    offers: React.PropTypes.array.isRequired,
    onLoadMore: React.PropTypes.func.isRequired,
    isInfiniteLoading: React.PropTypes.bool.isRequired,
    currentFilter: React.PropTypes.string
  }

  getSpinner() {
    return (
      <Halogen.PulseLoader color={styles.loader.color} />
    );
  }

  filterText(text, filter) {
    const matcher = new RegExp('\\b' + filter, 'i');
    return !!text.match(matcher);
  }

  render() {
    const {currentFilter, offers, onLoadMore, isInfiniteLoading} = this.props;
    return (
      <section>
        {_.map(currentFilter ? _.filter(offers, offer => this.filterText(offer.text, currentFilter)) : offers, offer => {
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

const styles = {
  loader: {
    color: '#4DAF7C'
  }
}
