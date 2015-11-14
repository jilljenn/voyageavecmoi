import React from 'react';

export default class Offer extends React.Component {
  static propTypes = {
    offer: React.PropTypes.object.isRequired
  }

  render() {
    return (
      <section>
        <p>{this.props.offer.text}</p>
        <button>Incorrect?</button>
      </section>
    );
  }
}
