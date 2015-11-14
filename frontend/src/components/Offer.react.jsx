import React from 'react';

import {Card, Button} from 'belle';

export default class Offer extends React.Component {
  static propTypes = {
    offer: React.PropTypes.object.isRequired
  }

  render() {
    return (
      <Card>
        <p>{this.props.offer.text}</p>
        <Button>Incorrect?</Button>
      </Card>
    );
  }
}
