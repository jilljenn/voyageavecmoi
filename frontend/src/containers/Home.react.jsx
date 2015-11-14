import React from 'react';

import OfferList from 'components/OfferList.react';

import {connect} from 'react-redux';
import {fetchOffers} from 'actions/OffersActions';

function mapStateToProps(state) {
  return {
    offers: state.offers.items,
    isLoading: state.offers.isFetching
  };
}

function mapDispatchToProps(dispatch) {
  return {
    fetch: () => dispatch(fetchOffers())
  }
}

class Home extends React.Component {
  static propTypes = {
    offers: React.PropTypes.array.isRequired,
    dispatch: React.PropTypes.func.isRequired,
    isLoading: React.PropTypes.bool.isRequired,
    fetch: React.PropTypes.func.isRequired
  }

  componentWillMount() {
    this.props.fetch();
  }

  render() {
    const {dispatch, offers, isLoading} = this.props;

    return (
      <article>
        <h1>Listes des offres de transport:</h1>
        <OfferList
          offers={offers}
        />
      </article>
    );
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Home);
