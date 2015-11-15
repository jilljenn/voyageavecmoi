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

  render() {
    const {currentFilter, offers, onLoadMore, isInfiniteLoading} = this.props;
    return (
      <section>
        <Infinite
          elementHeight={200}
          containerHeight={650}
          infiniteLoadBeginOffset={200}
          onInfiniteLoad={onLoadMore}
          loadingSpinnerDelegate={this.getSpinner()}
          isInfiniteLoading={isInfiniteLoading}>
          {_.map(currentFilter ? _.filter(offers, offer => _.capitalize(offer.text).includes(_.capitalize(currentFilter))) : offers, offer => {
            return (
              <Offer
                key={offer.id}
                offer={offer}
              />
            );
          })}
        </Infinite>
      </section>
    );
  }
}

const styles = {
  loader: {
    color: '#4DAF7C'
  }
}
