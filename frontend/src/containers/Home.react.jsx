import React from 'react';

import {connect} from 'react-redux';

import {voteIncorrect, fetchOffers} from 'actions/OffersActions';

@connect(state => {
  return {
    offers: state.offers.items,
    isLoading: state.offers.isFetching
  }
})
export default class Home extends React.Component {
  static propTypes = {
    offers: React.PropTypes.array.isRequired,
    isLoading: React.PropTypes.bool.isRequired
  }

  componentDidMount() {
    this.props.dispatch(fetchOffers());
  }

  render() {
    const {dispatch, offers, isLoading} = this.props;

    return (
      <article>
        <h1>Listes des offres de transport:</h1>
        <OfferList
          onIncorrectVoted={id => dispatch(voteIncorrect(id))}
          offers={offers}
        />
      </article>
    );
  }
}
