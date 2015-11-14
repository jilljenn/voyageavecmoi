import React from 'react';

import OfferList from 'components/OfferList.react';
import OfferFilter from 'components/OfferFilter.react';

import {connect} from 'react-redux';
import {fetchOffers, filterOffer} from 'actions/OffersActions';

import Radium from 'radium';

function mapStateToProps(state) {
  return {
    offers: state.offers.items,
    isLoading: state.offers.isFetching,
    currentFilter: state.offers.currentFilter
  };
}

function mapDispatchToProps(dispatch) {
  return {
    fetch: () => dispatch(fetchOffers()),
    filter: text => dispatch(filterOffer(text))
  }
}

@Radium
class Home extends React.Component {
  static propTypes = {
    dispatch: React.PropTypes.func,
    fetch: React.PropTypes.func.isRequired,
    filter: React.PropTypes.func.isRequired,
    offers: React.PropTypes.array.isRequired,
    isLoading: React.PropTypes.bool,
    currentFilter: React.PropTypes.string
  }

  componentWillMount() {
    this.props.fetch();
  }

  render() {
    const {dispatch, offers, currentFilter, isLoading} = this.props;

    return (
      <article style={styles.article}>
        <h1 style={styles.title}>Listes des offres de transport:</h1>
        <OfferFilter onFilterUpdate={text => this.props.filter(text)} />
        <OfferList
          offers={offers}
          currentFilter={currentFilter}
        />
      </article>
    );
  }
}

const styles = {
  article: {
    display: 'flex',
    flexFlow: 'column nowrap'
  },
  title: {
    margin: 'auto'
  }
};

export default connect(mapStateToProps, mapDispatchToProps)(Home);
