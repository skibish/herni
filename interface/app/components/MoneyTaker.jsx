import React from 'react';

class MoneyTaker extends React.Component {
  constructor(props) {
    super(props);

    this.handleClick = this.handleClick.bind(this);
    this.handleBuy = this.handleBuy.bind(this);
  }

  state = {value: 0}

  handleClick(event) {
    let newValue = parseInt(this.state.value) + parseInt(event.target.firstChild.nodeValue);
    this.setState({value: newValue});
  }

  handleBuy() {
    this.setState({value: 0});
    this.props.onBuyClick();
  }

  render() {
    var value = this.state.value;
    return (
      <div className="moneyTaker panel panel-default">
        <div className="panel-heading">Input</div>
        <div className="panel-body">
          <div className="input-group">
            <input type="text" className="form-control" value={value} readOnly/>
            <div className="input-group-btn">
              <button className="coinFive btn btn-default" onClick={this.handleClick}>5</button>
              <button className="coinTen btn btn-default" onClick={this.handleClick}>10</button>
              <button className="coinTwenty btn btn-default" onClick={this.handleClick}>20</button>
              <button className="submitMoney btn btn-success" disabled={!this.props.isBuyButtonEnabled} onClick={this.handleBuy}>Buy!</button>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default MoneyTaker;
