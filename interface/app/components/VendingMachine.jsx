import React from 'react';
import ReactDom from 'react-dom';
import ItemList from './ItemList.jsx';
import MoneyTaker from './MoneyTaker.jsx';

class VendingMachine extends React.Component {
  constructor(props) {
    super(props);

    this.handleItemSelection = this.handleItemSelection.bind(this);
    this.turnOffBuyButton = this.turnOffBuyButton.bind(this);
  }

  state = {
    data: {
      products: [
        {
          slot: 12,
          name: "Cookies",
          price: 80,
          count: 13
        },
        {
          slot: 13,
          name: "Candies",
          price: 75,
          count: 5
        },
        {
          slot: 14,
          name: "Poison",
          price: 50,
          count: 0
        },
        {
          slot: 15,
          name: "Puson",
          price: 50,
          count: 0
        },
        {
          slot: 16,
          name: "Pason",
          price: 50,
          count: 0
        },
        {
        	slot: 17,
        	name: "Pison",
        	price: 50,
        	count: 0
        },
  	]
  },
  isBuyButtonEnabled: false
}

  handleItemSelection() {
    this.setState({isBuyButtonEnabled: true});
  }

  turnOffBuyButton() {
    this.setState({isBuyButtonEnabled: false});
  }

  render() {
    return (
      <div className="vendingMachine container-fluid">
        <div className="row">
          <div className="col-md-8">
            <ItemList products={this.state.data.products} onItemSelection={this.handleItemSelection} />
          </div>
          <div className="col-md-4">
            <MoneyTaker isBuyButtonEnabled={this.state.isBuyButtonEnabled} onBuyClick={this.turnOffBuyButton} />
          </div>
        </div>
      </div>
    );
  }
}

export default VendingMachine;
