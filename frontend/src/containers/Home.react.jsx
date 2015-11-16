import React from 'react';

import OfferList from 'components/OfferList.react';
import OfferFilter from 'components/OfferFilter.react';

import {connect} from 'react-redux';
import {fetchOffers, fetchOffersByCity, fetchMoreOffers, filterOffer} from 'actions/OffersActions';
import {fetchCities} from 'actions/CitiesActions';

import Halogen from 'halogen';
import Radium from 'radium';

function mapStateToProps(state) {
  return {
    offers: state.offers.items,
    cities: state.cities.items,
    isLoading: state.offers.isFetching || state.cities.isFetching,
    currentCity: state.offers.currentCity,
    currentFilter: state.offers.currentFilter,
    error: state.error
  };
}

function mapDispatchToProps(dispatch) {
  return {
    fetchOffers: () => dispatch(fetchOffers()),
    fetchCities: () => dispatch(fetchCities()),
    fetchCity: city => dispatch(fetchOffersByCity(city)),
    fetchMore: start => dispatch(fetchMoreOffers(start)),
    filter: text => dispatch(filterOffer(text))
  }
}

@Radium
class Home extends React.Component {
  static propTypes = {
    dispatch: React.PropTypes.func,
    fetchOffers: React.PropTypes.func.isRequired,
    fetchCities: React.PropTypes.func.isRequired,
    fetchCity: React.PropTypes.func.isRequired,
    fetchMore: React.PropTypes.func.isRequired,
    filter: React.PropTypes.func.isRequired,
    offers: React.PropTypes.array.isRequired,
    cities: React.PropTypes.array.isRequired,
    error: React.PropTypes.object.isRequired,
    isLoading: React.PropTypes.bool,
    currentCity: React.PropTypes.string,
    currentFilter: React.PropTypes.string,
  }

  componentWillMount() {
    this.props.fetchCities();
    this.props.fetchOffers();
  }

  render() {
    const {dispatch, offers, cities, error,
      currentFilter, currentCity, isLoading} = this.props;

    return (
      <article style={styles.article}>
        <h1 style={styles.title}>Listes des offres de transport</h1>
        {isLoading &&
          <section style={styles.loader.section}>
            <Halogen.GridLoader color={styles.loader.color} />
          </section>
        }
        {error.failed &&
          <section style={styles.error.section}>
            <h2 style={styles.error.title}>
              Une erreur est survenue: {error.message}
              Essayez peut-être de recharger la page!
            </h2>
          </section>
        }
        <section>
          <OfferFilter
            onFilterUpdate={text => this.props.filter(text)}
            onCityUpdate={city => this.props.fetchCity(city)}
            cities={cities}
            currentCity={currentCity}
          />
          <OfferList
            offers={offers}
            currentFilter={currentFilter}
            onLoadMore={() => this.props.fetchMore(offers.length)}
            isInfiniteLoading={isLoading}
          />
        </section>
      </article>
    );
  }
}

const styles = {
  article: {
    display: 'flex',
    flexFlow: 'column nowrap',
    margin: 'auto'
  },
  title: {
    margin: 'auto auto 20px auto',
    fontSize: '42px'
  },
  loader: {
    section: {
      margin: 'auto'
    },
    color: '#4DAF7C'
  },
  error: {
    title: {
      fontSize: '24px',
      margin: 'auto'
    },
    section: {
      display: 'flex'
    }
  }
};

export default connect(mapStateToProps, mapDispatchToProps)(Home);
