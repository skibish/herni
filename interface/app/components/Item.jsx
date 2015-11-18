import React from 'react';

class Item extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="item panel panel-default">
        <div className="panel-heading"><span className="name">{this.props.name}</span>{' '}<span className="price">${this.props.price}</span></div>
        <div className="panel-body">{this.props.count}</div>
        <div className="panel-footer">
          <button className="btn btn-default pull-right" disabled={!this.props.isSelectable} onClick={this.props.onSelectClick}>Select</button>
          <div className="clearfix"></div>
        </div>
      </div>
    );
  }
}

export default Item;
