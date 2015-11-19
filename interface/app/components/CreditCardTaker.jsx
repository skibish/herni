import React from 'react';

class CreditCardTaker extends React.Component {
  constructor(props) {
    super(props);

  }

  render() {

    let inlineStyle = {marginBottom: '10px'}

    return (
      <div className="moneyTaker panel panel-default">
        <div className="panel-heading">Credit Card Input</div>
        <div className="panel-body">
          <div className="input-group" style={inlineStyle}>
            <input type="text" className="form-control"/>
            <span className="input-group-addon">CC</span>
          </div>
          <div className="input-group" style={inlineStyle}>
            <input type="text" className="form-control"/>
            <span className="input-group-addon">PIN</span>
          </div>
          <button className="submitMoney btn btn-success" disabled={!this.props.isBuyButtonEnabled}>Buy!</button>
        </div>
      </div>
    );
  }
}

export default CreditCardTaker;
