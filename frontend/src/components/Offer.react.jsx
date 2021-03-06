import React from 'react';

import moment from 'moment';
import {Card, Button} from 'belle';

import Radium from 'radium';

@Radium
export default class Offer extends React.Component {
  static propTypes = {
    offer: React.PropTypes.object.isRequired
  }

  render() {
    const {offer} = this.props;
    return (
      <Card>
        <section style={styles.card}>
          <h1 style={styles.screenName}>{offer.user.name} (@{offer.user.screen_name})</h1>
          {offer.created_at && <h5 style={styles.createdAt}>{moment.unix(offer.created_at).fromNow()}</h5>}
          <p
            style={styles.text}
            dangerouslySetInnerHTML={{__html: offer.text}}
          />
          <a target="_blank" href={`https://twitter.com/@${offer.user.screen_name}/status/${offer.id}`}>Prendre contact?</a>
        </section>
      </Card>
    );
  }
}

const styles = {
  card: {
    display: 'flex',
    flexFlow: 'column wrap'
  },
  text: {
    maxWidth: '500px'
  },
  screenName: {
    textAlign: 'right',
    fontSize: '18px'
  },
  createdAt: {
    textAlign: 'right'
  }
}
