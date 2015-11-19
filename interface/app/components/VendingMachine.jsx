import React from 'react';
import ReactDom from 'react-dom';
import ItemList from './ItemList.jsx';
import MoneyTaker from './MoneyTaker.jsx';
import Message from './Message.jsx';
import Header from './Header.jsx';
import $ from 'jquery';

class VendingMachine extends React.Component {
  constructor(props) {
    super(props);

    this.handleItemSelection = this.handleItemSelection.bind(this);
    this.sendMoneyRequest = this.sendMoneyRequest.bind(this);
    this.handleBuyButtonClick = this.handleBuyButtonClick.bind(this);
  }

  state = {
    products: [],
    isBuyButtonEnabled: false,
    selectedItemId: 0,
    activeCredit: 0,
    message: ''
}

  // load product list
  loadProductListRequest() {
    $.ajax({
      url: '/api/product_list',
      dataType: 'json',
      cache: false,
      success: function (data) {
        this.setState({products: data.products})
      }.bind(this)
    });
  }

  // send moeny into the vending machine
  sendMoneyRequest(amount) {
    $.ajax({
      url: '/api/balance_refill',
      method: "POST",
      data: JSON.stringify({credit: parseFloat(amount)}),
      dataType: "json",
      contentType: "application/json; charset=utf-8",
      success: function (data) {
        let credit = Math.round(data.credit * 100) / 100;
        this.setState({activeCredit: credit})
      }.bind(this)
    });
  }

  // purchase something
  purchaseItemRequest() {
    $.ajax({
      url: '/api/purchase',
      method: 'POST',
      data: JSON.stringify({slot: this.state.selectedItemId, payment: 'cash', payment_details: {}}),
      dataType: "json",
      contentType: "application/json; charset=utf-8",
      success: function (data) {
        let credit = Math.round(data.credit * 100) / 100;
        this.setState({activeCredit: credit, message: data.result});
      }.bind(this)
    });
  }

  // when component is loaded, get product list
  componentDidMount() {
    this.loadProductListRequest();
  }

  // when item is selected enabled buy button
  handleItemSelection(id) {
    this.setState({isBuyButtonEnabled: true, selectedItemId: id});
  }

  // after purchase, disable button
  handleBuyButtonClick() {
    // after purchase, download product list
    $.when(this.purchaseItemRequest()).then(() => {
      this.loadProductListRequest();
    });
    this.setState({isBuyButtonEnabled: false});
  }

  render() {
    let text = this.state.message;
    let messageBox = ' ';

    if (text !== '') {
      let style = (text == 'success') ? 'alert alert-success' : 'alert alert-warning';
      messageBox = <Message message={text} classes={style} />;
    }

    return (
      <div className="vendingMachine container-fluid">
        <Header />
        <div className="row">
          <div className="col-md-8">
            <ItemList products={this.state.products} onItemSelection={this.handleItemSelection} />
          </div>
          <div className="col-md-4">
            <MoneyTaker
              isBuyButtonEnabled={this.state.isBuyButtonEnabled}
              activeCredit={this.state.activeCredit}
              onMoneyAddition={this.sendMoneyRequest}
              onBuyClick={this.handleBuyButtonClick} />
              {messageBox}
          </div>
        </div>
      </div>
    );
  }
}

export default VendingMachine;
