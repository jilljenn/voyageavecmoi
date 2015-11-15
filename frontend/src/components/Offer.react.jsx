import React from 'react';

import {Card, Button} from 'belle';

import Radium from 'radium';

@Radium
export default class Offer extends React.Component {
  static propTypes = {
    offer: React.PropTypes.object.isRequired
  }

  render() {
    return (
      <Card>
        <p style={styles.text}>{this.props.offer.text}</p>
        <Button primary>Prendre contact?</Button>
      </Card>
    );
  }
}

const styles = {
  text: {
    maxWidth: '500px'
  }
}
